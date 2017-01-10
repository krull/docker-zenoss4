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


class IIRCDMonitorDataSourceInfo(IRRDDataSourceInfo):
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    hostname = schema.TextLine(title=_t(u'Host Name'),
                               group=_t(u'IRC'))
    warning_num = schema.Int(title=_t(u'Warning Count'),
                             group=_t(u'IRC'))
    port = schema.Int(title=_t(u'Port'),
                      group=_t(u'IRC'))
    critical_num = schema.Int(title=_t(u'Critical Count'),
                              group=_t(u'IRC'))
