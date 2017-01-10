##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """DellCPUMap
Gather Dell Open Manage processor information.
"""

from Products.DataCollector.plugins.CollectorPlugin \
    import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.zenoss.snmp.CpuMap \
    import getManufacturerAndModel

class DellCPUMap(SnmpPlugin):
    """Map Dell Open Manage cpu table to model."""

    maptype = "DellCPUMap"
    modname = "Products.ZenModel.CPU"
    relname = "cpus"
    compname = "hw"

    cpucols = {
        '.2': 'socket',
        '.8': '_manuf',
        '.10': '_familyidx',
        '.12': 'clockspeed',
        '.13': 'extspeed',
        '.14': 'voltage',
        '.16': '_version',
    }

    cachecols = {'.6': 'cpusock', '.11': 'level', '.13': 'size'}

    snmpGetTableMaps = (
        GetTableMap('cpuTable', '.1.3.6.1.4.1.674.10892.1.1100.30.1', cpucols),
            GetTableMap('cacheTable', 
                    '.1.3.6.1.4.1.674.10892.1.1100.40.1', cachecols),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cputable = tabledata.get("cpuTable")
        cachetable = tabledata.get("cacheTable")
        if not cputable: return
        rm = self.relMap()
        cpumap = {}
        for cpu in cputable.values():
            om = self.objectMap(cpu)
            if not getattr(om, '_manuf', False):
                continue
            try: cpufam = self.cpufamily[cpu['_familyidx']-1]
            except IndexError: cpufam = ""
            if not cpufam.startswith(om._manuf):
                cpufam = om._manuf + " " + cpufam
            om.setProductKey = getManufacturerAndModel(
                cpufam + " " + om._version)
            om.title = "%s_%s" % (om._manuf, om.socket)
            om.id = self.prepId(om.title)
            cpumap[om.socket] = om
            rm.append(om)
        
        for cache in cachetable.values():
            cpu = cpumap.get(cache.get('cpusock', None), None)
            if cpu is None: continue
            try: level = self.cacheLevel[cache['level']-1]
            except IndexError: level = None
            if level == "L1": 
                cpu.cacheSizeL1 = cache['size']
            elif level == "L2":
                cpu.cacheSizeL2 = cache['size']
        return rm


    cpufamily = (
        'other', 
        'unknown',
        "8086",
        "80286",
        "80386",
        "80486",
        "8087",
        "80287",
        "80387",
        "80487",
        "Intel Pentium",
        "Pentium Pro",
        "Pentium II",
        "Pentium MMX",
        "Celeron",
        "Xeon",
        "Pentium III",
        "Pentium III Xeon",
        "Pentium III Speed Step",
        "Itanium",
        "Intel Xeon",
        "Pentium 4",
        "Intel Xeon MP",
        "Intel Itanium 2",
    )

    cacheLoc = ('other','unknown','internal','external')
    cacheLevel = ('other', 'unknown', 'L1', 'L2', 'L3')
