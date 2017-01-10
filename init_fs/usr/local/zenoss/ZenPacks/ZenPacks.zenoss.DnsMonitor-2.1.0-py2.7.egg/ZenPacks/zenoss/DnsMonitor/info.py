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
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.DnsMonitor.interfaces import IDnsMonitorDataSourceInfo


class DnsMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IDnsMonitorDataSourceInfo)
    timeout = ProxyProperty('timeout')
    cycletime = ProxyProperty('cycletime')
    hostname = ProxyProperty('hostname')
    dnsServer = ProxyProperty('dnsServer')
    expectedIpAddress = ProxyProperty('expectedIpAddress')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
