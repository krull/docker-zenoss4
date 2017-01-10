##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2013 all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """ProcessMap
Gather process information using WMI.
Currently not supported.
"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenModel.OSProcessMatcher import buildObjectMapData

class ProcessMap(WMIPlugin):

    maptype = "OSProcessMap" 
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    deviceProperties = WMIPlugin.deviceProperties + ('osProcessClassMatchData',)

    def queries(self):
        return{
        "Win32_Process":"Select * From Win32_Process",
    }

    def _extractProcessText(self, proc):
        cmd = getattr(p, 'commandline', None) or p.executablepath
        return cmd and cmd.strip()
    
    def process(self, device, results, log):
        """collect wmi information from this device"""
        
        # TODO: Remove the next two lines when WMI process monitoring is
        # implemented.
        log.warn("WMI process discovery is currently not supported")
        return [self.relMap(),]
        
        log.info('Collecting process information for device %s', device.id)
        cmds = map(self._extractProcessText, results['Win32_Process'])
        cmds = filter(bool, cmds)
        rm = self.relMap()
        matchData = device.osProcessClassMatchData
        rm.extend(map(self.objectMap, buildObjectMapData(matchData, cmds)))
        return rm
