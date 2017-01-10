##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """DellDeviceMap
Gather Dell Open Manage hardware model + serial number and OS information.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs
import re

class DellDeviceMap(SnmpPlugin):
    """Map mib elements from Dell Open Manage mib to get hw and os products.
    """

    maptype = "DellDeviceMap" 

    snmpGetMap = GetMap({ 
        #'.1.3.6.1.4.1.674.10892.1.300.10.1.8' : 'manufacturer',
        '.1.3.6.1.4.1.674.10892.1.300.10.1.9.1' : 'setHWProductKey',
        '.1.3.6.1.4.1.674.10892.1.300.10.1.11.1' : 'setHWSerialNumber',
        '.1.3.6.1.4.1.674.10892.1.400.10.1.6.1': 'setOSProductKey',
         })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        om.setHWProductKey = MultiArgs(om.setHWProductKey, "Dell")
        if re.search(r'Microsoft', om.setOSProductKey, re.I):
            om.setOSProductKey = MultiArgs(om.setOSProductKey, "Microsoft")
        elif re.search(r'Red\s*Hat', om.setOSProductKey, re.I):
            om.setOSProductKey = MultiArgs(om.setOSProductKey, "RedHat")
        return om
