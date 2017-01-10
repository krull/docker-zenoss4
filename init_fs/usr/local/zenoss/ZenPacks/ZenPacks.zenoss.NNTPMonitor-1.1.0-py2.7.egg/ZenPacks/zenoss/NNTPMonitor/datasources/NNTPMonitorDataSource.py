##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath

class NNTPMonitorDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):
    
    NNTP_MONITOR = 'NNTPMonitor'
    ZENPACKID = 'ZenPacks.zenoss.NNTPMonitor'
    
    sourcetypes = (NNTP_MONITOR,)
    sourcetype = NNTP_MONITOR

    eventClass = '/Status/NNTP'
        
    nntpServer = '${dev/id}'
    useSSL = False
    port = 119
    timeout = 60

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'nntpServer', 'type':'string', 'mode':'w'},
        {'id':'useSSL', 'type':'boolean', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )
        
    _relations = RRDDataSource.RRDDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editNNTPMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editNNTPMonitorDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.RRDDataSource.__init__(self, id, title, buildRelations)


    def getDescription(self):
        if self.sourcetype == self.NNTP_MONITOR:
            return self.nntpServer + str(self.port)
        return RRDDataSource.RRDDataSource.getDescription(self)


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        if self.useSSL:
            parts = [binPath('check_nntps')]
        else:
            parts = [binPath('check_nntp')]
        if self.nntpServer:
            parts.append('-H %s' % self.nntpServer)
        if self.port:
            parts.append('-p %d' % self.port)
        if self.timeout:
            parts.append('-t %d' % self.timeout)

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
