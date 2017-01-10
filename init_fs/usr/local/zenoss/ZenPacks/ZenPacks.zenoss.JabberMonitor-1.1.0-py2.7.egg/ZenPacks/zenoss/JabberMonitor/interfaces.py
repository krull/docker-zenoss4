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


class IJabberMonitorDataSourceInfo(IRRDDataSourceInfo):
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    hostname = schema.TextLine(title=_t(u'Host Name'),
                               group=_t(u'Jabber'))
    port = schema.Int(title=_t(u'Port'),
                       group=_t(u'Jabber'))
    sendString = schema.TextLine(title=_t(u'Send String'),
                                 group=_t(u'Jabber'))
    expectString = schema.TextLine(title=_t(u'Expect String'),
                                   group=_t(u'Jabber'))
