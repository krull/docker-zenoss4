##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""CpuMap

Uses WMI to map processor information on CPU objects

"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId
from Products.DataCollector.plugins.zenoss.snmp.CpuMap \
    import getManufacturerAndModel
import re

FIND_INTEGER = re.compile("\d+").search

class CpuMap(WMIPlugin):

    maptype = "CpuMap" 
    modname = "Products.ZenModel.CPU"
    relname = "cpus"
    compname = "hw"

    attrs = (
        'deviceid', 
        'description', 
        'manufacturer',
        'socketdesignation',
        'currentclockspeed',
        'extclock',
        'currentvoltage',
        'l2cachesize',
        'version',
    )
    
    def queries(self):
        return  {
     "Win32_CacheMemory":"Select deviceid,InstalledSize From Win32_CacheMemory",
     "Win32_Processor":"Select %s From Win32_Processor" % ",".join(self.attrs),
    }
    
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s (Cache) for device %s', self.name(), device.id)
        L1Cache = None
        for cache in results["Win32_CacheMemory"]:
            if cache.deviceid == 'Cache Memory 0': # This is the L1 Cache
                L1Cache = int(cache.installedsize)
                break
            else:
                continue
            
        log.info('processing %s (CPU) for device %s', self.name(), device.id)
        maps = []
        rm = self.relMap()
        for cpu in results["Win32_Processor"]:
            if cpu.deviceid is not None:
                om = self.objectMap()
                om.id = prepId(cpu.deviceid)
                om.setProductKey = getManufacturerAndModel(
                    cpu.manufacturer + " " + cpu.description)
                om.socket = cpu.socketdesignation
                if isinstance(om.socket, basestring):
                    integerMatch = FIND_INTEGER(om.socket)
                    if integerMatch:
                        om.socket = int(integerMatch.group(0))
                om.clockspeed = cpu.currentclockspeed
                om.extspeed = cpu.extclock
                om.voltage = int(cpu.currentvoltage) * 100
                if L1Cache:
                    om.cacheSizeL1 = L1Cache
                    
                # the l2cachesize attribute isn't correct on multicore CPUs
                # when running in VMware
                try:
                    om.cacheSizeL2 = int(cpu.l2cachesize)
                except (TypeError, ValueError):
                    om.cacheSizeL2 = 0

                om.perfmonInstance = self.getPerfmonInstance(cpu, log)
                rm.append(om)
            
        maps.append(rm)
        return maps

    def getPerfmonInstance(self, cpu, log):
        """
        Determines the Perfmon Instance Path for the provided instance of the
        Win32_Processor class
        """
        perfmonInstance = None
        try:
            processor = int(cpu.deviceid.split('CPU')[1])
            perfmonInstance = '\\Processor(%d)' % processor
        except (IndexError, ValueError):
            log.warn("CPU DeviceId property ('%s') malformed, perfmon "
                     "monitoring will be skipped", cpu.deviceid)
        return perfmonInstance
