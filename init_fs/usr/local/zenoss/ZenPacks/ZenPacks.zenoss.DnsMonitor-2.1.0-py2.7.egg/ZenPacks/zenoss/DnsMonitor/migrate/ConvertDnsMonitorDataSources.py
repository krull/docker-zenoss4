##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack, ZenPackDataSourceMigrateBase
from ZenPacks.zenoss.DnsMonitor.datasources.DnsMonitorDataSource \
        import DnsMonitorDataSource


class ConvertDnsMonitorDataSources(ZenPackDataSourceMigrateBase):
    version = Version(2, 0, 0)
    
    # These provide for conversion of datasource instances to the new class
    dsClass = DnsMonitorDataSource
    oldDsModuleName = 'Products.DnsMonitor.datasources' \
                                                    '.DnsMonitorDataSource'
    oldDsClassName = 'DnsMonitorDataSource'
    
    # Reindex all applicable datasource instances
    reIndex = True
