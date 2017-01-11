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
from Products.ZenModel.ZenPack import ZenPack, ZenPackDataSourceMigrateBase
from ZenPacks.zenoss.ZenJMX.datasources.JMXDataSource import JMXDataSource

class ConvertJMXDataSources(ZenPackDataSourceMigrateBase):
    version = Version(3, 1, 2)
    
    # These provide for conversion of datasource instances to the new class
    dsClass = JMXDataSource
    oldDsModuleName = 'Products.ZenJMX.datasources.JMXDataSource'
    oldDsClassName = 'JMXDataSource'
    
    # Reindex all applicable datasource instances
    reIndex = True
