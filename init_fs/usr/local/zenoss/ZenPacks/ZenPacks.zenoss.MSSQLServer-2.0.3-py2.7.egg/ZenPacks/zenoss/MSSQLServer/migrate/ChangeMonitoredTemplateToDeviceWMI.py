##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

import logging
log = logging.getLogger("zen.ZenPacks.zenoss.MSSQLServer")

class ChangeMonitoredTemplateToDeviceWMI(ZenPackMigration):
    """
    Change Monitoring template for MSSQLServer from Device (SNMP-oriented) to Device_WMI
    """
    version = Version(2, 0, 3)

    def migrate(self, pack):
        try:
            devices = pack.dmd.getDmdRoot("Devices")
            mssql_dc = devices.Server.Windows.WMI.MSSQLServer
            templates = mssql_dc.zDeviceTemplates
            changed = False
            
            if 'Device' in templates:
                templates.remove('Device')
                changed = True
                
            if 'Device_WMI' not in templates:
                templates.insert(0, 'Device_WMI')
                changed = True
                
            if changed:
                mssql_dc.setZenProperty('zDeviceTemplates', templates)
            
        except Exception as e:
            log.warn("Failed to modify zDeviceTemplates on MSSQLServer device class, %s", e)


ChangeMonitoredTemplateToDeviceWMI()
