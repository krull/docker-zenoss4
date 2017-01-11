##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from ZenPacks.zenoss.ZenJMX.interfaces import IJMXDataSourceInfo
from ZenPacks.zenoss.ZenJMX.datasources.JMXDataSource import JMXDataSource

def jmxProtocolVocabulary(context):
    return SimpleVocabulary.fromValues(JMXDataSource.protocolTypes)

class JMXDataSourceInfo(RRDDataSourceInfo):
    implements(IJMXDataSourceInfo)
    
    # JMX RMI REMOTING-JMX
    jmxPort = ProxyProperty('jmxPort')
    jmxProtocol = ProxyProperty('jmxProtocol')
    jmxRawService = ProxyProperty('jmxRawService')
    rmiContext = ProxyProperty('rmiContext')
    objectName = ProxyProperty('objectName')
    
    # Authentication
    authenticate = ProxyProperty('authenticate')
    username = ProxyProperty('username')
    password = ProxyProperty('password')
    attributeName = ProxyProperty('attributeName')
    attributePath = ProxyProperty('attributePath')
    # Operation
    operationName = ProxyProperty('operationName')
    operationParamValues = ProxyProperty('operationParamValues')
    operationParamTypes = ProxyProperty('operationParamTypes')
    
    @property
    def testable(self):
        """
        We can NOT test this datsource against a specific device
        """
        return False
