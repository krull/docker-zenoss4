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
from ZenPacks.zenoss.MSSQLServer import ZenPack
from Products.ZenRelations.Exceptions import ObjectNotFound
import logging

log = logging.getLogger("zen.ZenPacks.zenoss.MSSQLServer")

class ChangeLowBufferHitRatioThreshold:
    version = Version(2, 0, 2)

    def migrate(self, pack):
        devices = pack.dmd.getDmdRoot("Devices")

        thresholdName = "low buffer hit ratio"
        try:
            templates = devices.Server.Windows.WMI.MSSQLServer.rrdTemplates
            threshold = templates.MSSQLServer.thresholds._getOb(thresholdName)
            # only change the threshold if we find it to be configured the way
            # the original one was
            if getattr(threshold, 'maxval', "") == "90":
                threshold.minval = "90"
                threshold.maxval = ""
                log.info("Changed %s to have a minval of 90", thresholdName)
        except ObjectNotFound:
            log.warn("Unable to find expected %s threshold to modify",
                     thresholdName)
            pass
