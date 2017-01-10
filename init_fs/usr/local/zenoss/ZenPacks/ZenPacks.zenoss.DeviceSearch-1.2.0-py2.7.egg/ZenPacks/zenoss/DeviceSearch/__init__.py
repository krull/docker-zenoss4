##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
log = logging.getLogger('zen.DeviceSearch')

import os
import Globals
from Products.CMFCore.DirectoryView import registerDirectory


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase

class ZenPack(ZenPackBase):
    """
    Customize ZenPack class to allow additional installation and removal steps.
    """
    
    def install(self, dmd):
        super(ZenPack, self).install(dmd)
        
    def remove(self, dmd, leaveObjects=False):
        super(ZenPack, self).remove(dmd, leaveObjects)
