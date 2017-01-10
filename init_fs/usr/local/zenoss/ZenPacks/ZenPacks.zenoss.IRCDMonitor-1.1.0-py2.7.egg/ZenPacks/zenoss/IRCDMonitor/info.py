##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.IRCDMonitor.interfaces import IIRCDMonitorDataSourceInfo


class IRCDMonitorDataSourceInfo(RRDDataSourceInfo):
    implements(IIRCDMonitorDataSourceInfo)
    cycletime = ProxyProperty('cycletime')
    hostname = ProxyProperty('hostname')
    port = ProxyProperty('port')
    warning_num = ProxyProperty('warning_num')
    critical_num = ProxyProperty('critical_num')

    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
