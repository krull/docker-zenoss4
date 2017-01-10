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
from Products.ZenModel.ZenPack import ZenPack
import logging
log = logging.getLogger('zenpack')

class Menu:
    version = Version(2, 2, 1)

    def migrate(self, pack):
        log.info('installing Guest menu item')
        dmd = pack.__primary_parent__.__primary_parent__
        id = 'virtualMachineDetail'
        try:
            dmd.zenMenus.More.manage_deleteZenMenuItem((id,))
        except (KeyError, AttributeError):
            pass
        dmd.zenMenus.More.manage_addZenMenuItem(
            id,
            action=id,
            description='Guests',
            allowed_classes=('VirtualMachineHost',),
            ordering=5.0)
        log.info('installed Guest menu item')
                     
Menu()
