##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.infos import ProxyProperty
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implements
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.DigMonitor.interfaces import IDigMonitorDataSourceInfo
from ZenPacks.zenoss.DigMonitor.datasources.DigMonitorDataSource import DigMonitorDataSource

def recordTypeVocabulary(context):
    # somehow build items [(name, value)]
    return SimpleVocabulary.fromValues(DigMonitorDataSource.allRecordTypes)

class DigMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IDigMonitorDataSourceInfo)
    timeout = ProxyProperty('timeout')
    cycletime = ProxyProperty('cycletime')
    dnsServer = ProxyProperty('dnsServer')
    port = ProxyProperty('port')
    recordName = ProxyProperty('recordName')
    recordType = ProxyProperty('recordType')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
