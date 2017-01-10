##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007,2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack, ZenPackDataSourceMigrateBase
from ZenPacks.zenoss.ApacheMonitor.datasources.ApacheMonitorDataSource \
        import ApacheMonitorDataSource


class ConvertApacheMonitorDataSources(ZenPackDataSourceMigrateBase):
    version = Version(2, 0, 2)
    
    # These provide for conversion of datasource instances to the new class
    dsClass = ApacheMonitorDataSource
    oldDsModuleName = 'Products.ApacheMonitor.datasources' \
                                                    '.ApacheMonitorDataSource'
    oldDsClassName = 'ApacheMonitorDataSource'
    
    # Reindex all applicable datasource instances
    reIndex = True
