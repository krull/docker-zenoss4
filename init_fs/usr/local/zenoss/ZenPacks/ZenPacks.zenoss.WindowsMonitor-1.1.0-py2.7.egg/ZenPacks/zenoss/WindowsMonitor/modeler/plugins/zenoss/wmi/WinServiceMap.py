##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """WinServiceMap
Collect Windows service information using WMI, which enables monitoring
of Windows services via zenwin.
"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class WinServiceMap(WMIPlugin):

    compname = "os"
    relname = "winservices"
    modname = "Products.ZenModel.WinService"
    
    attrs = ("name","caption",
             "pathName","serviceType","startMode","startName","state")

    
    def queries(self):
        return {
            "Win32_Service" :
            "Select %s From Win32_Service" % (",".join(self.attrs)),
            }
    
    def process(self, device, results, log):
        """Collect win service info from this device.
        """
        log.info('Processing WinServices for device %s' % device.id)
        
        rm = self.relMap()
        for svc in results["Win32_Service"]:
            om = self.objectMap()
            om.id = prepId(svc.name)
            om.serviceName = svc.name
            om.caption = svc.caption
            om.setServiceClass = {'name':svc.name, 'description':svc.caption}
            for att in self.attrs:
                if att in ("name", "caption", "state"): continue
                setattr(om, att, getattr(svc, att, "")) 
            rm.append(om)
        
        return rm
