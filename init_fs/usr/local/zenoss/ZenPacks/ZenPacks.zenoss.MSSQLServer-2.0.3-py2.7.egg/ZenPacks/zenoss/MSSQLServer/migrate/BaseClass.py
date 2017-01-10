##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
from Products.ZenModel.migrate.Migrate import Version
from ZenPacks.zenoss.MSSQLServer import ZenPack
import logging

class BaseClass:
    version = Version(2, 0, 1)

    def migrate(self, pack):
        if pack.__class__ != ZenPack:
            pack.__class__ = ZenPack
