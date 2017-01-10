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


class IFtpMonitorDataSourceInfo(IRRDDataSourceInfo):
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    hostname = schema.TextLine(title=_t(u'Host Name'))
    port = schema.Int(title=_t(u'Port'))
    sendString = schema.TextLine(title=_t(u'Send String'))
    expectString = schema.TextLine(title=_t(u'Expect String'))
    quitString = schema.TextLine(title=_t(u'Quit String'))
    refuse = schema.Choice(title=_t(u'Refuse'),
                           vocabulary="ftpMonitorStatesVocabulary")
    mismatch = schema.Choice(title=_t(u'Mismatch'),
                             vocabulary="ftpMonitorStatesVocabulary")
    maxBytes = schema.TextLine(title=_t(u'Max Bytes'))
    delay = schema.TextLine(title=_t(u'Delay'))
    certificate = schema.Int(title=_t(u'Certificate (minimum days for which a certificate is valid)'))
    useSSL = schema.Bool(title=_t(u'Use SSL'))
    warning = schema.Int(title=_t(u'Warning Response Time (seconds)'))
    critical = schema.Int(title=_t(u'Critical Response Time (seconds)'))
