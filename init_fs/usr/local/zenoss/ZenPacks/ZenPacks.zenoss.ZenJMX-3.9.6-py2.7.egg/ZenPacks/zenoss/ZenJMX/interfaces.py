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


class IJMXDataSourceInfo(IRRDDataSourceInfo):
    # Connection Info
    jmxPort = schema.TextLine(title=_t(u'Management Port'), group=_t(u'JMX Connection and Metadata Infomation'))
    jmxProtocol = schema.Choice(title=_t(u'Protocol'), group=_t(u'JMX Connection and Metadata Infomation'),
                                vocabulary='jmxProtocolVocabulary')
    jmxRawService = schema.TextLine(title=_t(u'Raw Service URL (advanced users only)'), group=_t(u'JMX Connection and Metadata Infomation'))
    rmiContext = schema.TextLine(title=_t(u'RMI Context (URL context when using RMI Protocol)'), group=_t(u'JMX Connection and Metadata Infomation'))
    objectName = schema.TextLine(title=_t(u'Object Name'), group=_t(u'JMX Connection and Metadata Infomation'))

    # Authentication
    username = schema.TextLine(title=_t(u'Username'), group=_t(u'JMX Remote Authentication Information'))
    authenticate = schema.TextLine(title=_t(u'Auth Enabled'), group=_t(u'JMX Remote Authentication Information'))
    password = schema.Password(title=_t(u'Password'), group=_t(u'JMX Remote Authentication Information'))
    
    # Operation
    attributeName = schema.TextLine(title=_t(u'Attribute Name'), group=_t(u'JMX Attribute and Operation Configuration'))
    attributePath = schema.TextLine(title=_t(u'Attribute Path'), group=_t(u'JMX Attribute and Operation Configuration'))
    operationParamValues = schema.TextLine(title=_t(u'Parameter Values'), group=_t(u'JMX Attribute and Operation Configuration'))
    operationName = schema.TextLine(title=_t(u'Operation Name'), group=_t(u'JMX Attribute and Operation Configuration'))
    operationParamTypes = schema.TextLine(title=_t(u'Parameter Types'), group=_t(u'JMX Attribute and Operation Configuration'))
