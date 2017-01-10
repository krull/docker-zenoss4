##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''FtpMonitorDataSource.py

Defines datasource for FtpMonitor
'''

import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath

class FtpMonitorDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.zenoss.FtpMonitor'
    FTP_MONITOR = 'FtpMonitor'
    
    sourcetypes = (FTP_MONITOR,)
    sourcetype = FTP_MONITOR

    timeout = 60
    eventClass = '/Status/Ftp'
        
    hostname = '${dev/id}'
    port = 21
    sendString = ''
    expectString = ''
    quitString = ''
    refuse = 'crit'
    mismatch = 'warn'
    maxBytes = ''
    delay = ''  #test this
    certificate = ''
    useSSL = False  
    warning = ''
    critical = ''
    
    states = ('ok','warn','crit')

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'sendString', 'type':'string', 'mode':'w'},
        {'id':'expectString', 'type':'string', 'mode':'w'},
        {'id':'quitString', 'type':'string', 'mode':'w'},
        {'id':'refuse', 'type':'string', 'mode':'w'},
        {'id':'mismatch', 'type':'string', 'mode':'w'},
        {'id':'maxBytes', 'type':'string', 'mode':'w'},
        {'id':'delay', 'type':'string', 'mode':'w'},
        {'id':'useSSL', 'type':'boolean', 'mode':'w'},
        {'id':'warning', 'type':'string', 'mode':'w'},
        {'id':'critical', 'type':'string', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )
        
    _relations = RRDDataSource.RRDDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editFtpMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editFtpMonitorDataSource',
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
        if self.sourcetype == self.FTP_MONITOR:
            return self.hostname
        return RRDDataSource.RRDDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = [binPath('check_ftp')]
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.timeout:
            parts.append('-t %s' % self.timeout)
        if self.warning:
            parts.append('-w %s' % self.warning)
        if self.critical:
            parts.append('-c %s' % self.critical)
        if self.sendString:
            parts.append('-s %s' %  self.sendString)
        if self.expectString:
            parts.append('-e %s' % self.expectString)
        if self.quitString:
            parts.append('-q %s' % self.quitString)
        if self.refuse:
            parts.append('-r %s' % self.refuse)
        if self.mismatch:
            parts.append('-M %s' % self.mismatch)
        if self.maxBytes:
            parts.append('-m %s' % self.maxBytes)
        if self.delay:
            parts.append('-d %s' % self.delay)
        if self.certificate:
            parts.append('-D %s' % self.certificate)
        if self.useSSL:
            parts.append('-S %s' % self.useSSL)

        cmd = ' '.join(parts)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        if not hasattr(self.datapoints, 'time'):
            self.manage_addRRDDataPoint('time')

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self, REQUEST)
