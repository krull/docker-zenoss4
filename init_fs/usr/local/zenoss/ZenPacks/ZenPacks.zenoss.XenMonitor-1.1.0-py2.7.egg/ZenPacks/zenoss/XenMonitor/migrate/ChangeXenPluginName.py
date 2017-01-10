##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration
import logging
log = logging.getLogger('zenpack')

class ChangeXenPluginName(ZenPackMigration):
    version = Version(1, 0, 0)

    def migrate(self, pack):
        log.info( 'Renaming Xen plugin to zenoss.snmp.Xen')
        fromPluginName = 'Xen'
        toPluginName = 'zenoss.cmd.Xen'
        vhmDeviceClass = 'Virtual Machine Host'
        deviceClass = pack.dmd.Devices.Server._getOb(vhmDeviceClass).Xen
        collectorPlugins = list( deviceClass.zCollectorPlugins )
        newPluginList = []
        for plugin in collectorPlugins:
            if plugin == fromPluginName:
                newPluginList.append( toPluginName )
            else:
                newPluginList.append( plugin )
        if newPluginList != collectorPlugins:
            deviceClass.setZenProperty( 'zCollectorPlugins',
                                        tuple( newPluginList ) )
