##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """cpuinfo
Modeling plugin that parses the contents of /proc/cpuinfo to gather 
information about the device's processor(s).
"""

import re

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class CpuinfoException(Exception):
    pass

class Cpuinfo(object):
    """
    Initialized with a dictionary that contains the colon-delimited items
    found in /proc/cpuinfo.
    """
    
    def __init__(self, cpuinfoDict):
        self.cpuinfoDict = cpuinfoDict
    
    def getProductKey(self):
        """
        Gets the product key from a dictionary based on /proc/cpuinfo.
        """
        if 'vendor_id' in self.cpuinfoDict and \
                'model name' in self.cpuinfoDict:
            productKey = ' '.join([self.cpuinfoDict['vendor_id'],
                                   self.cpuinfoDict['model name']])
        elif 'cpu' in self.cpuinfoDict:
            productKey = self.cpuinfoDict['cpu']
        else:
            raise CpuinfoException(
                    'Could not find product key in /proc/cpuinfo.')
        return productKey
    
    def getCacheSizeL2(self):
        """
        Gets the cache size from a dictionary based on /proc/cpuinfo.
        """
        if 'cache size' in self.cpuinfoDict:
            cacheSizeL2 = self.cpuinfoDict['cache size'].split()[0]
        elif 'L2 cache' in self.cpuinfoDict:
            cacheSizeL2 = self.cpuinfoDict['L2 cache'].split()[0].rstrip('K')
        else:
            raise CpuinfoException(
                    'Could not find cacheSizeL2 in /proc/cpuinfo.')
        return int(cacheSizeL2)
    
    def getClockspeed(self):
        """
        Gets the clockspeed from a dictionary based on the items in /proc/cpu.
        """
        if 'cpu MHz' in self.cpuinfoDict:
            clockspeed = self.cpuinfoDict['cpu MHz']
        elif 'clock' in self.cpuinfoDict:
            clockspeed = self.cpuinfoDict['clock'].rstrip('MHz')
        else:
            raise CpuinfoException(
                    'Could not find clockspeed in /proc/cpuinfo.')
        return float(clockspeed)
    
class cpuinfo(CommandPlugin):
    """
    cat /proc/cpuinfo - get CPU information on Linux machines
    """
    
    command = "/bin/cat /proc/cpuinfo"
    compname = "hw"
    relname = "cpus"
    modname = "Products.ZenModel.CPU"
    
    pattern = re.compile(r"\s*processor\s+:\s+")
    linePattern = re.compile(r"\s*:\s*")
    
    def process(self, device, results, log):
        log.info('Collecting CPU information for device %s' % device.id)
        rm = self.relMap()
        for result in self.pattern.split(results)[1:]:
            lines = result.splitlines()
            pairs = []
            for line in lines[1:]:
                if line:
                    pair = self.linePattern.split(line)
                    if len(pair) == 2: pairs.append(pair)
            cpuinfo = Cpuinfo(dict(pairs))
            om = self.objectMap()
            om.id = lines[0].strip()
            om.socket = om.id
            def setClockspeed():
                om.clockspeed = cpuinfo.getClockspeed()
            def setCachSizeL2():
                om.cacheSizeL2 = cpuinfo.getCacheSizeL2()
            def setProductKey():
                om.setProductKey = cpuinfo.getProductKey()
            for setter in setClockspeed, setCachSizeL2, setProductKey:
                try:
                    setter()
                except CpuinfoException, e:
                    log.debug(e)
            rm.append(om)
        return [rm]
