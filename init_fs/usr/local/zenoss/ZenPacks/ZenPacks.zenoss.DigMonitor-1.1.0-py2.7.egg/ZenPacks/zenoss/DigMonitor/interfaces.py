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


class IDigMonitorDataSourceInfo(IRRDDataSourceInfo):
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    dnsServer = schema.TextLine(title=_t(u'DNS Server'))
    recordName = schema.TextLine(title=_t(u'Record Name'))
    port = schema.Int(title=_t(u'Port'))
    recordType = schema.Choice(title=_t(u'Record Type'),
                               vocabulary="dnsMonitorRecordTypeVocabulary")
