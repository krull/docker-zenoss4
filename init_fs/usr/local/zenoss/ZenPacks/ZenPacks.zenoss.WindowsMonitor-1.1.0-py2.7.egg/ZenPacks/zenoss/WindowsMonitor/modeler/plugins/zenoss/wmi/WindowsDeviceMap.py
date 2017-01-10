##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""WindowsDeviceMap

Uses WMI to map Windows OS & hardware information

"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.ZenUtils.Utils import prepId
import re

class WindowsDeviceMap(WMIPlugin):

    maptype = "WindowsDeviceMap"
    
    def queries(self):
        return  {
            "Win32_OperatingSystem":"select * from Win32_OperatingSystem",
            "Win32_SystemEnclosure":"select * from Win32_SystemEnclosure",
        }
    
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)

        om = self.objectMap()
        
        for os in results["Win32_OperatingSystem"]:
            if re.search(r'Microsoft', os.manufacturer, re.I):
                os.manufacturer = "Microsoft"
                os.caption = re.sub(r'\s*\S*Microsoft\S*\s*', '', os.caption)
            
            om.setOSProductKey = MultiArgs(os.caption, os.manufacturer)
            om.snmpSysName = os.csname # lies!
            om.snmpContact = os.registereduser # more lies!
            break

        for e in results["Win32_SystemEnclosure"]:
            om.setHWTag = e.smbiosassettag.rstrip()
            om.setHWSerialNumber = e.serialnumber.rstrip()
            model = e.model
            if not model: model = "Unknown"
            manufacturer = e.manufacturer
            if not manufacturer:
                manufacturer = "Unknown"
            elif re.search(r'Dell', manufacturer):
                manufacturer = "Dell"
            om.setHWProductKey = MultiArgs(model, manufacturer)
            break 

        return om
