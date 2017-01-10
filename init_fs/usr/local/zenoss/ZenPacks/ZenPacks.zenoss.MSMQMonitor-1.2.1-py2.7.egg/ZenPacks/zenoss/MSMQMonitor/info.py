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
from Products.Zuul.infos.component import ComponentInfo

from ZenPacks.zenoss.MSMQMonitor.interfaces import *


class MSMQQueueInfo(ComponentInfo):
    implements(IMSMQQueueInfo)

    queueName = ProxyProperty('queueName')
    messagesInQueueThreshold = ProxyProperty('messagesInQueueThreshold')
