##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """SoftwareMap
Gather the software inventory list.Requires that the WMI Windows Installer Provider is installed.
"""

from pysamba.twisted.callback import WMIFailure
from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class SoftwareMap(WMIPlugin):

    maptype = "SoftwareMap"
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zSoftwareMapMaxPort',)

    attrs = (
        'name',
        'installdate',
    )

    def queries(self):
        return{
        "Win32_Product": \
        "Select %s from Win32_Product" % ",".join(self.attrs),
    }

    def preprocess(self, results, log):
        """Pass errors through to the process step so we can
        report the device name"""
        return results

    def process(self, device, results, log):
        """collect wmi information from this device"""
        if isinstance(results, WMIFailure):
            log.warning("Unable to load software from "
                        "device %s (%s).", device.id, str(results))
            if str(results) == 'NT code 0x80041013':
                log.warn("Install the WMI Windows "
                         "Installer Provider on the device to enable "
                         "software inventory collection.")
            return

        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for sw in results['Win32_Product']:
            if sw.name is not None:
                om = self.objectMap()
                om.setProductKey = sw.name
                om.id = self.prepId(om.setProductKey)
                if not om.id: continue
                if hasattr(om, 'setInstallDate') and sw.installdate and len(sw.installdate)==8:
                    om.setInstallDate = '%s/%s/%s 00:00:00' % \
                        (sw.installdate[0:4], sw.installdate[4:6], sw.installdate[6:8])
                rm.append(om)
        return rm
