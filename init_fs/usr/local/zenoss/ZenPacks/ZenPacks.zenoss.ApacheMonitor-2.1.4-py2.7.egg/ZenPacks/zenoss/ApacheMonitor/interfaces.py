##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.interfaces import IBasicDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IApacheMonitorDataSourceInfo(IBasicDataSourceInfo):
    component = schema.TextLine(title=_t(u'Component'))
    eventKey = schema.TextLine(title=_t(u'Event Key'))
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    hostname = schema.TextLine(title=_t(u'Apache Host'))
    usessh = schema.Bool(title=_t(u'Use SSH'))
    port = schema.Int(title=_t(u'Apache Port'))
    ssl = schema.Bool(title=_t(u'Use HTTPS?'))
    url = schema.TextLine(title=_t(u'Status URL'))
    ngerror = schema.TextLine(title=_t(u'Named Group Regex Error'))
    ngregex = schema.Text(title=_t(u'Named Group Regex'), xtype='twocolumntextarea')
