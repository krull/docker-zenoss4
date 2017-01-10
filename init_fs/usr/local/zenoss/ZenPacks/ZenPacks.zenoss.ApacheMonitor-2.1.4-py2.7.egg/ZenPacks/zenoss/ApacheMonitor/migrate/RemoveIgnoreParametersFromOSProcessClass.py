##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
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

class RemoveIgnoreParametersFromOSProcessClass(ZenPackMigration):
    version = Version(2, 1, 4)
    
    def migrate(self, pack):
        log.info("Removing ignoreParameters from OSProcessClass object")
        uid = "/zport/dmd/Processes/Apache/osProcessClasses/httpd"
        pc = pack.dmd.unrestrictedTraverse(uid, None)
        if pc:
            includeRegex = "^[^ ]*httpd[^ /]*( |$)"
            replaceRegex = "^([^ ]*httpd[^ /]*)( .*|$)"
            replacement = "\\1"
            try:
                if getattr(pc, 'ignoreParameters', False):
                    pc.ignoreParameters = False
                if getattr(pc, 'ignoreParametersWhenModeling', False):
                    pc.ignoreParametersWhenModeling = False
                if not getattr(pc, 'includeRegex', False) == includeRegex:
                    pc.includeRegex = includeRegex
                if not getattr(pc, 'replaceRegex', False) == replaceRegex:
                    pc.replaceRegex = replaceRegex
                if not getattr(pc, 'replacement', False) == replacement:
                    pc.replacement = replacement
            except:
                log.warn("Failed to migrate %s", uid, exc_info=True)

RemoveIgnoreParametersFromOSProcessClass()
