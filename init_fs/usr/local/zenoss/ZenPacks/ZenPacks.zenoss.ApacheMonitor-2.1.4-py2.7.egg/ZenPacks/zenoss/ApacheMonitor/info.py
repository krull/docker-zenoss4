##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos.template import BasicDataSourceInfo
from ZenPacks.zenoss.ApacheMonitor.interfaces import IApacheMonitorDataSourceInfo


class ApacheMonitorDataSourceInfo(BasicDataSourceInfo):
    implements(IApacheMonitorDataSourceInfo)
    usessh = ProxyProperty('usessh')
    component = ProxyProperty('component')
    eventKey = ProxyProperty('eventKey')
    timeout = ProxyProperty('timeout')
    hostname = ProxyProperty('hostname')
    port = ProxyProperty('port')
    ssl = ProxyProperty('ssl')
    url = ProxyProperty('url')
    ngregex = ProxyProperty('ngregex')
    ngerror = ProxyProperty('ngerror')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
