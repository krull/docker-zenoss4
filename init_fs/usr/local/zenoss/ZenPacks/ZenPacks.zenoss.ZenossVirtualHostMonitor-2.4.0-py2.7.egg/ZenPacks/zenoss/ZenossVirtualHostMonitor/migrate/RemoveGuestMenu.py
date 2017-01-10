##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
log = logging.getLogger('zenpack.ZenossVirtualHostMonitor')

import Globals
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPack

class RemoveGuestMenu:
    version = Version(3, 1, 0)

    def migrate(self, pack):
        log.info('Removing Guest menu item')
        dmd = pack.__primary_parent__.__primary_parent__
        id = 'virtualMachineDetail'
        moreMenuIds = [menu.id for menu in dmd.zenMenus.More.objectValues()]
        if id in moreMenuIds:
            try:
                dmd.zenMenus.More.manage_deleteZenMenuItem((id,))
            except (KeyError, AttributeError):
                pass
                     
RemoveGuestMenu()
