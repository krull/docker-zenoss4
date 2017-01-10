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
from ZenPacks.zenoss.HttpMonitor.interfaces import IHttpMonitorDataSourceInfo
from ZenPacks.zenoss.HttpMonitor.datasources.HttpMonitorDataSource import HttpMonitorDataSource

def httpMonitorRedirectVocabulary(context):
    return SimpleVocabulary.fromValues(HttpMonitorDataSource.onRedirectOptions)


class HttpMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IHttpMonitorDataSourceInfo)
    timeout = ProxyProperty('timeout')
    cycletime = ProxyProperty('cycletime')
    hostname = ProxyProperty('hostname')
    ipAddress = ProxyProperty('ipAddress')
    port = ProxyProperty('port')
    useSsl = ProxyProperty('useSsl')
    url = ProxyProperty('url')
    regex = ProxyProperty('regex')
    caseSensitive = ProxyProperty('caseSensitive')
    invert = ProxyProperty('invert')
    basicAuthUser = ProxyProperty('basicAuthUser')
    basicAuthPass = ProxyProperty('basicAuthPass')
    onRedirect = ProxyProperty('onRedirect')

    proxyAuthUser = ProxyProperty('proxyAuthUser')
    proxyAuthPassword = ProxyProperty('proxyAuthPassword')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
