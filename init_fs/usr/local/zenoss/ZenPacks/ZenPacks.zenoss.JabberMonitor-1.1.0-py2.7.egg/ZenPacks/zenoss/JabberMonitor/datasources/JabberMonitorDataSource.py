##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''JabberMonitorDataSource.py

Defines datasource for JabberMonitor
'''

import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath


def safeQuote( unsafeString ):
    return '"%s"' % "\\'".join( unsafeString.split('"') )


class JabberMonitorDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):
    
    JABBER_MONITOR = 'JabberMonitor'
    
    ZENPACKID = 'ZenPacks.zenoss.JabberMonitor'
    
    sourcetypes = (JABBER_MONITOR,)
    sourcetype = JABBER_MONITOR

    timeout = 60
    eventClass = '/Status/Jabber'
        
    hostname = '${dev/id}'
    port = 5223
    sendString = "<stream:stream to='${dev/id}' xmlns:stream='http://etherx.jabber.org/streams'>\n"
    expectString = "<stream"

    _properties = RRDDataSource.RRDDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'sendString', 'type':'string', 'mode':'w'},
        {'id':'expectString', 'type':'string', 'mode':'w'}
        )
        
    _relations = RRDDataSource.RRDDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editJabberMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editJabberMonitorDataSource',
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
        if self.sourcetype == self.JABBER_MONITOR:
            ipAddress = getattr(self, 'ipAddress', '')
            url = getattr(self, 'url', '')
            description = ipAddress + url
        else:
            description = RRDDataSource.RRDDataSource.getDescription(self)
        return description


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = [binPath('check_jabber')]
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.sendString:
            parts.append('-s %s ' % safeQuote( self.sendString ) )
        if self.expectString:
            parts.append('-e %s ' % safeQuote( self.expectString ) )
        cmd = ' '.join(parts)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd


    def checkCommandPrefix(self, context, cmd):
        return cmd


    def addDataPoints(self):
        if not self.datapoints._getOb('time', None):
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
