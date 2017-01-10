##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals


# Add the msmqueues relation to all devices.
from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

Device._relations += (('msmqqueues', ToManyCont(ToOne,
    'ZenPacks.zenoss.MSMQMonitor.MSMQQueue', 'msmqserver')), )


from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    packZProperties = [
        ('zMSMQIgnoreQueues', '^tcp', 'string'),
        ]

    def install(self, app):
        ZenPackBase.install(self, app)
        self.rebuildRelations(app.zport.dmd)

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.rebuildRelations(app.zport.dmd)

    def remove(self, app, leaveObjects=False):
        Device._relations = tuple(
            [x for x in Device._relations if x[0] != 'msmqqueues'])
        self.rebuildRelations(app.zport.dmd)
        ZenPackBase.remove(self, app, leaveObjects)

    def rebuildRelations(self, dmd):
        for d in dmd.Devices.getSubDevices():
            d.buildRelations()
