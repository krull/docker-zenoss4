##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack
import logging

class DiscoveryPlugins:
    version = Version(2, 0, 6)

    def migrate(self, pack):
        # Get a reference to the device class
        dmd = pack.dmd.primaryAq()
        devcls = dmd.Devices.Discovered
        # Only add plugins that aren't already there
        current = tuple(devcls.zCollectorPlugins)
        new = ('zenoss.wmi.IpInterfaceMap', 'zenoss.wmi.IpRouteMap')
        toadd = tuple(set(new) - set(current))
        newstate = current + toadd
        # Set the zProperty
        devcls.setZenProperty('zCollectorPlugins', newstate)
