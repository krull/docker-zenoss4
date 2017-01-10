##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """DellPCIMap
Use Dell Open Manage to determine expansion slot information.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellPCIMap(SnmpPlugin):
    """Map Dell Open Manage PCI table to model."""

    maptype = "DellPCIMap"
    modname = "Products.ZenModel.ExpansionCard"
    relname = "cards"
    compname = "hw"

    columns = {'.6': 'slot','.8': '_manuf','.9': '_model',}

    snmpGetTableMaps = (
        GetTableMap('pciTable', '.1.3.6.1.4.1.674.10892.1.1100.80.1', columns),
    )
    
    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        pcitable = tabledata.get("pciTable")
        if not pcitable: return
        rm = self.relMap()
        for card in pcitable.values():
            try:
                om = self.objectMap(card)
                om.id = self.prepId("%s" % om.slot)
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
