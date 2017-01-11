##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''NtpMonitorDataSource.py

Defines datasource for NtpMonitor
'''

import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.Utils import binPath


class NtpMonitorDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.zenoss.NtpMonitor'
    NTP_MONITOR = 'NtpMonitor'
    
    parser = 'Nagios'

    sourcetypes = (NTP_MONITOR,)
    sourcetype = NTP_MONITOR

    timeout = 60
    eventClass = '/Status/Ntp'
        
    hostname = '${dev/id}'
    port = 123
    warning = ''
    critical = ''

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'warning', 'type':'string', 'mode':'w'},
        {'id':'critical', 'type':'string', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )
        
    _relations = RRDDataSource.RRDDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editNtpMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editNtpMonitorDataSource',
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
        if self.sourcetype == self.NTP_MONITOR:
            return self.hostname
        return RRDDataSource.RRDDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = [binPath('check_ntp_peer')]
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        elif context.manageIp:
            parts.append('-H %s' % context.manageIp)
        else:
            raise Exception("No host value for NTP check '%s'" % context.id)

        if self.timeout:
            parts.append('-t %s' % self.timeout)
        if self.warning:
            parts.append('-w %s' % self.warning)
        if self.critical:
            parts.append('-c %s' % self.critical)
        cmd = ' '.join(parts)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        if not hasattr(self.datapoints, 'offset'):
            self.manage_addRRDDataPoint('offset')

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self, REQUEST)
