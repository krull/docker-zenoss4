##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


pack = 'ZenJMX'
__doc__ = '%s ZenPack.  Adds JMX support to Zenoss' % pack

import os
import sys

import Globals

from Products.ZenModel.ZenPack import ZenPackBase
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

libDir = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.isdir(libDir):
    sys.path.append(libDir)

binDir = os.path.join(os.path.dirname(__file__), 'bin')

class ZenPack(ZenPackBase):
    "ZenPack Loader that loads zProperties used by ZenJMX"
    packZProperties = [
        ('zJmxManagementPort', 12345, 'int'),
        ('zJmxAuthenticate', False, 'boolean'),
        ('zJmxUsername', 'admin', 'string'),
        ('zJmxPassword', 'admin', 'password'),
        ]

    def install(self,app):
        if not os.path.exists(os.environ['ZENHOME'] +'/zenjmx-libs'):
            print "Creating %s" % os.environ['ZENHOME'] +'/zenjmx-libs'
            os.makedirs(os.environ['ZENHOME'] +'/zenjmx-libs')

        super(ZenPack, self).install(app)
