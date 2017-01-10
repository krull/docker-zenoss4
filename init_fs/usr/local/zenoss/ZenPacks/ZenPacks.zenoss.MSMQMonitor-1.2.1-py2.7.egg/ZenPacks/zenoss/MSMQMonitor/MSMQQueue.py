##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import sys
from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS
from Products.ZenUtils.Time import SaveMessage
from Products.ZenWidgets.interfaces import IMessageSender


class MSMQQueue(DeviceComponent, ManagedEntity):
    portal_type = meta_type = 'MSMQQueue'

    queueName = ''
    messagesInQueueThreshold = '10000'

    _properties = ManagedEntity._properties + (
        {'id':'queueName', 'type':'string', 'mode':'w'},
        {'id':'messagesInQueueThreshold', 'type':'string', 'mode':'w'},
        )

    _relations = (
        ('msmqserver', ToOne(ToManyCont, 'Products.ZenModel.Device',
            'msmqqueues')),
        )

    factory_type_information = (
        {
            'id'             : 'MSMQQueue',
            'meta_type'      : 'MSMQQueue',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'MSMQQueue_icon.gif',
            'product'        : 'MSMQMonitor',
            'immediate_view' : 'viewMSMQQueue',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewMSMQQueue'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS,)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW,)
                },
            )
          },
        )


    def viewName(self):
        return self.queueName
    name = primarySortKey = viewName


    def breadCrumbs(self, terminator='dmd'):
        crumbs = super(MSMQQueue, self).breadCrumbs(terminator)
        url = self.device().primaryAq().absolute_url_path() + "/msmqDetail"
        crumbs.insert(-1,(url,'MSMQ'))
        return crumbs


    def device(self):
        return self.msmqserver()


    def manage_editMSMQQueue(self, messagesInQueueThreshold=None, monitor=None,
        REQUEST=None):
        """
        Edit this MSMQQueue from the web.
        """
        if messagesInQueueThreshold is not None:
            self.messagesInQueueThreshold = messagesInQueueThreshold

        if monitor is not None:
            self.monitor = monitor

        self.index_object()

        if REQUEST:
            IMessageSender(self).sendToBrowser('Saved', SaveMessage())
            return self.callZenScreen(REQUEST)


    def isUserCreated(self):
        """
        Always returns true so the queue can be edited from its details screen.
        """
        return True


    def getMessagesInQueueThreshold(self):
        if self.messagesInQueueThreshold == '':
            return sys.maxint
        else:
            return float(self.messagesInQueueThreshold)


    def getMessagesInQueue(self, default=None):
        return self.cacheRRDValue('messagesInQueue')


    def getMessagesInQueueString(self):
        m = self.getMesagesInQueue()
        return m is None and "unknown" or m


InitializeClass(MSMQQueue)
