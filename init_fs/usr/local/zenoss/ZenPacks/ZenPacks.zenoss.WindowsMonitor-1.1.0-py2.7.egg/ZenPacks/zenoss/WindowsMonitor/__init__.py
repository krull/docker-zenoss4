##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="WindowsMonitor ZenPack"

__import__('pkg_resources').declare_namespace(__name__)

import Globals
import logging
import os.path
from zope.event import notify
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.Zuul.interfaces import ICatalogTool
from Products.Zuul.catalog.events import IndexingEvent
from Products.ZenUtils.Utils import unused
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory

unused(Globals)

log = logging.getLogger("zen.windowsmonitor")


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

_discovery_plugins = ('zenoss.wmi.IpInterfaceMap', 'zenoss.wmi.IpRouteMap')

_PACK_Z_PROPS = [('zWinPerfCycleSeconds', 300, 'int'),
                 ('zWinPerfCyclesPerConnection', 5, 'int'),
                 ('zWinPerfTimeoutSeconds', 10, 'int'),
                 ('zWinEventlogClause', '', 'string'),
                 ('zWmiMonitorIgnore', True, 'boolean'),
                 ('zWinUser', '', 'string'),
                 ('zWinPassword', '', 'password'),
                 ('zWinEventlogMinSeverity', 2, 'int'),
                 ('zWinEventlog', False, 'boolean'),
                ]

for name, default_value, type_ in _PACK_Z_PROPS:
    setzPropertyCategory(name, 'Windows')

def _addPluginsToDiscovered(dmd):
    # Get a reference to the device class
    dmd = dmd.primaryAq()
    devcls = dmd.Devices.Discovered
    # Only add plugins that aren't already there
    current = tuple(devcls.zCollectorPlugins)
    new = _discovery_plugins
    toadd = tuple(set(new) - set(current))
    if not toadd: return
    newstate = current + toadd
    # Set the zProperty
    devcls.setZenProperty('zCollectorPlugins', newstate)

def _removePluginsFromDiscovered(dmd):
    # Get a reference to the device class
    dmd = dmd.primaryAq()
    devcls = dmd.Devices.Discovered
    current=tuple(devcls.zCollectorPlugins)
    # The intersection of the current plugins for this object
    # and the discovery plugins is what we want to remove
    toremove = tuple( set(current) & set(_discovery_plugins) )
    if not toremove: return
    newstate = tuple( set(current) - set(toremove) )
    devcls.setZenProperty('zCollectorPlugins',newstate)

class ZenPack(ZenPackBase):

    packZProperties =  _PACK_Z_PROPS

    def install(self, app):
        self._removePreviousZenPacks(self.dmd)
        ZenPackBase.install(self, app)
        _addPluginsToDiscovered(self.dmd)
        self.createZProperties(self.dmd.getPhysicalRoot())
        if not self.dmd.Devices.Discovered.hasProperty('zWmiMonitorIgnore'):
            self.dmd.Devices.Discovered.setZenProperty('zWmiMonitorIgnore', False)
        if not self.dmd.Devices.Server.Windows.hasProperty('zWmiMonitorIgnore'):
            self.dmd.Devices.Server.Windows.setZenProperty('zWmiMonitorIgnore', False)
        if not self.dmd.Devices.Server.Windows.hasProperty('zWinEventlog'):
            self.dmd.Devices.Server.Windows.setZenProperty('zWinEventlog', True)

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            self.removeZProperties(self.dmd.getPhysicalRoot())
            if self.dmd.Devices.Server.Windows.hasProperty('zWinEventlog'):
                self.dmd.Devices.Server.Windows.deleteZenProperty('zWinEventlog')
            if self.dmd.Devices.Server.Windows.hasProperty('zWmiMonitorIgnore'):
                self.dmd.Devices.Server.Windows.deleteZenProperty('zWmiMonitorIgnore')
            if self.dmd.Devices.Discovered.hasProperty('zWmiMonitorIgnore'):
                self.dmd.Devices.Discovered.deleteZenProperty('zWmiMonitorIgnore')
            _removePluginsFromDiscovered(self.dmd)
        ZenPackBase.remove(self, app, leaveObjects)

    def _removePreviousZenPacks(self, dmd):
        """
        Since this zenpack came from two WinModelerPlugins and ZenWinPerf
        we need to remove the packables from both of those zenpack as well
        as update the class for the WinPerfDataSources that came from ZenWinPerf
        """
        log.info("Removing Packables from previous zenpacks")
        self._movepacks(dmd)
        log.info("Migrating WinPerfDataSources to new class")
        self._migrateWinPerfDataSource(dmd)

    def _movepacks(self, dmd):
        """
        Take every pack relationship from WinModeler and ZenWinPerf and move it to this
        zenpack. This normally happens in ZenPackCmd.py when you have one zenpack replacing another.
        """
        packables = []
        try:
            modeler = dmd.ZenPackManager.packs._getOb('ZenPacks.zenoss.WinModelerPlugins')
            if modeler:
                for p in modeler.packables():
                    packables.append(p)
                    modeler.packables.removeRelation(p)
        except AttributeError:
            log.debug("ZenPacks.zenoss.WinModelerPlugins is not installed")
        try:
            zenwinperf = dmd.ZenPackManager.packs._getOb('ZenPacks.zenoss.ZenWinPerf')
            if zenwinperf:
                for p in zenwinperf.packables():
                    packables.append(p)
                    zenwinperf.packables.removeRelation(p)
        except AttributeError:
            log.debug("ZenPacks.zenoss.ZenWinPerf is not installed")
        # we do not need to readd the packable because that will be taken care of
        # in this zenpacks objects.xml
        return packables

    def _persistDataSource(self, datasource):
        """after switching the __class__ attribute, call this function to make the
        change permanent"""
        id = datasource.id
        from cStringIO import StringIO
        xml_file = StringIO()
        datasource.exportXml(xml_file)
        parent = datasource.getPrimaryParent()
        parent._delObject(datasource.id)
        from Products.ZenRelations.ImportRM import NoLoginImportRM
        xml_importer = NoLoginImportRM(parent)
        xml_file.seek(0)
        xml_importer.loadObjectFromXML(xml_file)
        xml_importer.processLinks()
        ds = parent._getOb(id)
        notify(IndexingEvent(ds))

    def _migrateWinPerfDataSource(self, dmd):
        from ZenPacks.zenoss.WindowsMonitor.datasources.WinPerfDataSource import WinPerfDataSource
        oldCls = "ZenPacks.zenoss.ZenWinPerf.datasources.WinPerfDataSource.WinPerfDataSource"
        results = ICatalogTool(dmd).search(oldCls)
        log.info("Converting %d datasources", results.total)
        for brain in results:
            obj = brain.getObject()
            obj.__class__ = WinPerfDataSource
            obj._p_changed = True
            self._persistDataSource(obj)
