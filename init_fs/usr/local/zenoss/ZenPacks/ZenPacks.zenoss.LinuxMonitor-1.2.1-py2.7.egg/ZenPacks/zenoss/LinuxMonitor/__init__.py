##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.LinuxMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    
    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux.
        """
        linux = app.dmd.Devices.createOrganizer('/Server/SSH/Linux')
        linux.setZenProperty( 'zCollectorPlugins', 
                              ['zenoss.cmd.uname',
                               'zenoss.cmd.uname_a',
                               'zenoss.cmd.df',
                               'zenoss.cmd.linux.cpuinfo', 
                               'zenoss.cmd.linux.memory', 
                               'zenoss.cmd.linux.ifconfig', 
                               'zenoss.cmd.linux.netstat_an', 
                               'zenoss.cmd.linux.netstat_rn', 
                               'zenoss.cmd.linux.process' ] ) 
        
        linux.register_devtype('Linux Server', 'SSH')
        ZenPackBase.install(self, app)
                                   
    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        if not leaveObjects:
            try:
                # Using findChild here to avoid finding /Server/Linux
                # accidentally via acquisition.
                linux = app.dmd.findChild('Devices/Server/SSH/Linux')
                linux.zCollectorPlugins = []
            except AttributeError:
                # No /Server/SSH/Linux device class to remove.
                pass
