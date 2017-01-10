##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.FtpMonitor.interfaces import IFtpMonitorDataSourceInfo
from ZenPacks.zenoss.FtpMonitor.datasources.FtpMonitorDataSource import FtpMonitorDataSource

def ftpMonitorStatesVocabulary(context):
    return SimpleVocabulary.fromValues(FtpMonitorDataSource.states)


class FtpMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IFtpMonitorDataSourceInfo)
    timeout = ProxyProperty('timeout')
    cycletime = ProxyProperty('cycletime')
    hostname = ProxyProperty('hostname')
    port = ProxyProperty('port')
    sendString = ProxyProperty('sendString')
    expectString = ProxyProperty('expectString')
    quitString = ProxyProperty('quitString')
    refuse = ProxyProperty('refuse')
    mismatch = ProxyProperty('mismatch')
    maxBytes = ProxyProperty('maxBytes')
    delay = ProxyProperty('delay')
    certificate = ProxyProperty('certificate')
    useSSL = ProxyProperty('useSSL')
    warning = ProxyProperty('warning')
    critical = ProxyProperty('critical')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
