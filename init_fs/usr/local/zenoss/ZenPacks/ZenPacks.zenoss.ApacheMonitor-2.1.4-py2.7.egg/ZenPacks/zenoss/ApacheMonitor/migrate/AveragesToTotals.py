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
log = logging.getLogger("zen.migrate")

class AveragesToTotals(ZenPackMigration):
    """
    Prior to version 2.0.2 of ZenPacks.zenoss.ApacheMonitor we were plotting
    the bytesPerSec and reqPerSec. It turns out that Apache keeps this as
    running averages that will eventually become less and less valuable.
    
    This migrate script converts existing templates to use the totalKBytes and
    totalAccesses metrics instead. These will remain valuable regardless of how
    long the httpd server has been running.
    
    http://dev.zenoss.com/trac/ticket/4238
    """
    
    version = Version(2, 0, 2)
    
    def migrate(self, pack):
        log.info("Converting Apache templates to use totalAccesses/totalKBytes")
        
        for t in pack.dmd.Devices.getAllRRDTemplates():
            if t.id != "Apache": continue
            
            # Eliminate old data points that we don't use anymore.
            for ds in t.datasources():
                if ds.sourcetype != 'ApacheMonitor': continue
                for dp in ds.datapoints():
                    if dp.id in ('bytesPerSec', 'reqPerSec'):
                        ds.datapoints._delObject(dp.id)
            
            # Convert any thresholds to the new data points.
            for th in t.thresholds():
                for i, dsname in enumerate(th.dsnames):
                    if dsname == 'apache_bytesPerSec':
                        th.dsnames[i] == 'apache_totalKBytes'
                    elif dsname == 'apache_reqPerSec':
                        th.dsnames[i] == 'apache_totalAccesses'
            
            # Remove references to old data points from graphs.
            for g in t.graphDefs():
                for gp in g.graphPoints():
                    if gp.meta_type != 'DataPointGraphPoint': continue
                    if gp.dpName in ('apache_bytesPerSec', 'apache_reqPerSec'):
                        g.graphPoints._delObject(gp.id)


AveragesToTotals()
