##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration
import logging
log = logging.getLogger("zen")

class MigrateThreadCountDataPoints(ZenPackMigration):
    version = Version(3, 1, 5)
    
    def migrate(self, pack):
        log.info("MigrateThreadCountDataPoints migrate")
        #find devices with either the java or zenjmx templat
        #and delete the rrd file for the threadcount datapoint
        
        for d in pack.dmd.Devices.getSubDevices():
            log.debug("MigrateThreadCountDataPoints device %s" % d.id)

            for template in d.getRRDTemplates():

                templateId = template.getPrimaryDmdId()
                log.debug("MigrateThreadCountDataPoints template %s" % templateId)

                dpName = None
                if  templateId == '/Devices/rrdTemplates/Java':
                    dpName = 'Thread Count_ThreadCount'
                elif templateId == '/Devices/rrdTemplates/ZenJMX':
                    dpName = 'ZenJMX Thread Count_ThreadCount'
                
                if dpName:
                    log.debug("MigrateThreadCountDataPoints dpName %s" % dpName)
                    perfConf = d.getPerformanceServer()
                    log.debug("MigrateThreadCountDataPoints perfConf %s" % perfConf.id)
                    perfConf.deleteRRDFiles(device=d.id, datapoint=dpName)
