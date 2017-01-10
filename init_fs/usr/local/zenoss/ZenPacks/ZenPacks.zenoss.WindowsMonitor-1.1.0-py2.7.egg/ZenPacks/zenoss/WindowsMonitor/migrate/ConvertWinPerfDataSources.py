##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackDataSourceMigrateBase
from ZenPacks.zenoss.WindowsMonitor.datasources.WinPerfDataSource \
        import WinPerfDataSource


class ConvertWinPerfDataSources(ZenPackDataSourceMigrateBase):
    version = Version(2, 1, 2)
    
    # These provide for conversion of datasource instances to the new class
    dsClass = WinPerfDataSource
    oldDsModuleName = 'Products.ZenWinPerf.datasources.WinPerfDataSource'
    oldDsClassName = 'WinPerfDataSource'
    
    # Reindex all applicable datasource instances
    reIndex = True
