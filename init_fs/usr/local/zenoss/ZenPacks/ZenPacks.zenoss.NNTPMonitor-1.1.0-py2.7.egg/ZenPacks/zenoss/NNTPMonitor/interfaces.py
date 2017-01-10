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


class INNTPMonitorDataSourceInfo(IRRDDataSourceInfo):
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    timeout = schema.TextLine(title=_t(u'Timeout (seconds)'))
    nntpServer = schema.TextLine(title=_t(u'NNTP Server'), group=_t(u'NNTP'))
    useSSL = schema.Bool(title=_t(u'Use SSL?'), group=_t(u'NNTP'))
    port = schema.Int(title=_t(u'Port'), group=_t(u'NNTP'))
