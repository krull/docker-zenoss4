##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.interfaces import IRRDDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IDnsMonitorDataSourceInfo(IRRDDataSourceInfo):
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    hostname = schema.TextLine(title=_t(u'Host Name'))
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    dnsServer = schema.TextLine(title=_t(u'DNS Server'))
    expectedIpAddress = schema.TextLine(title=_t(u'Expected IP Adresss'))
