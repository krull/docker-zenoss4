##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''IRCDMonitorDataSource.py

Defines datasource for IRCDMonitor
'''

import Products.ZenModel.RRDDataSource as RRDDataSource
import os.path
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine


class IRCDMonitorDataSource(ZenPackPersistence,RRDDataSource.RRDDataSource):

    IRCD_MONITOR = 'IRCDMonitor'
    ZENPACKID = 'ZenPacks.zenoss.IRCDMonitor'

    sourcetypes = (IRCD_MONITOR,)
    sourcetype = IRCD_MONITOR

    eventClass = '/Status/IRCD'

    hostname = '${dev/id}'
    port = 6667
    warning_num = 50
    critical_num = 100

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'warning_num', 'type':'int', 'mode':'w'},
        {'id':'critical_num', 'type':'int', 'mode':'w'},
        )

    _relations = RRDDataSource.RRDDataSource._relations + (
        )


    factory_type_information = (
    {
        'immediate_view' : 'editIRCDMonitorDataSource',
        'actions'        :
        (
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editIRCDMonitorDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.RRDDataSource.__init__(self, id, title, buildRelations)
        #self.addDataPoints()


    def getDescription(self):
        if self.sourcetype == self.IRCD_MONITOR:
            hostname = getattr(self, 'hostname', '')
            url = getattr(self, 'url', '')
            description = hostname + url
        else:
            description = RRDDataSource.RRDDataSource.getDescription(self)
        return description


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = ['check_ircd.py']
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.warning_num:
            parts.append('-w %s' % self.warning_num)
        if self.critical_num:
            parts.append('-c %s' % self.critical_num)
        cmd = ' '.join(parts)
        zpack = self.dmd.ZenPackManager.packs._getOb(self.ZENPACKID, None)
        if zpack is None:
            return ''
        cmd = zpack.path(
            "libexec",
            RRDDataSource.RRDDataSource.getCommand(self,context,cmd))
        return cmd


    def checkCommandPrefix(self, context, cmd):
        return cmd


    def addDataPoints(self):
        if not hasattr(self.datapoints, 'number'):
            self.manage_addRRDDataPoint('number')


    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self, REQUEST)
