##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

# --------------------------------------------------
# The 2.1.x DellMonitor zenpack overrides the remove()
# method.  In 2.2 the ZenPack.remove() method
# gained a 3rd parameter and the code was not
# backwards compatible with older method sigs.
# This monkeypatch fixes that problem when user
# is upgrading to 2.2
def betterRemove(self, app, leaveObjects=False):
    self.cleanupOurPlugins(app.zport.dmd)
    ZenPackBase.remove(self, app, leaveObjects)
try:
    import Products.DellMonitor
    Products.DellMonitor.ZenPack.remove = betterRemove
except ImportError:
    pass
# --------------------------------------------------

class ZenPack(ZenPackBase):
    """ DellMonitor loader
    """

    def install(self, app):
        ZenPackBase.install(self, app)
        self.setupCollectorPlugins(app.zport.dmd)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.setupCollectorPlugins(app.zport.dmd)

    def remove(self, app, leaveObjects=False):
        self.cleanupOurPlugins(app.zport.dmd)
        ZenPackBase.remove(self, app, leaveObjects)


    def setupCollectorPlugins(self, dmd):
        self.cleanupOldPlugins(dmd)

        def addDellPlugins(obj):
            if obj.hasProperty('zCollectorPlugins'):
                newPlugins = []
                for plugin in obj.zCollectorPlugins:
                    newPlugins.append(plugin)
                    if plugin == 'zenoss.snmp.DeviceMap':
                        newPlugins.append('DellDeviceMap')
                    elif plugin == 'zenoss.snmp.CpuMap':
                        newPlugins.append('DellCPUMap')
                        newPlugins.append('DellPCIMap')
                obj.zCollectorPlugins = newPlugins

        if hasattr(dmd.Devices, 'Server'):
            addDellPlugins(dmd.Devices.Server)
            if hasattr(dmd.Devices.Server, 'Linux'):
                addDellPlugins(dmd.Devices.Server.Linux)
            if hasattr(dmd.Devices.Server, 'Windows'):
                addDellPlugins(dmd.Devices.Server.Windows)

    def cleanupCollectorPlugins(self, dmd, plugin_list):
        obj_list = [dmd.Devices] + dmd.Devices.getSubOrganizers() + \
                dmd.Devices.getSubDevices()

        for thing in obj_list:
            if not thing.hasProperty('zCollectorPlugins'): continue
            newPlugins = []
            for plugin in thing.zCollectorPlugins:
                if plugin in plugin_list:
                    continue
                newPlugins.append(plugin)
            thing.zCollectorPlugins = newPlugins

    def cleanupOurPlugins(self, dmd):
        self.cleanupCollectorPlugins(dmd, (
                'DellDeviceMap', 'DellCPUMap', 'DellPCIMap'))

    def cleanupOldPlugins(self, dmd):
        self.cleanupCollectorPlugins(dmd, (
                'zenoss.snmp.DellDeviceMap', 'zenoss.snmp.DellCPUMap',
                'zenoss.snmp.DellPCIMap'))
