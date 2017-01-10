##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc_ = """IpRouteMap
Use WMI to gather routing information.
"""

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class IpRouteMap(WMIPlugin):
    
    maptype = "IpRouteMap"
    relname = "routes"
    compname = "os"
    modname = "Products.ZenModel.IpRouteEntry"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zIpRouteMapCollectOnlyLocal',
                                              'zIpRouteMapCollectOnlyIndirect')

    attrs = (
        'destination',
        'interfaceindex',
        'mask',
        'metric1',
        'metric2',
        'metric3',
        'metric4',
        'metric5',
        'nexthop',
        'protocol',
        'type',
    )

    def condition(self, device, log):
        if not WMIPlugin.condition(self, device, log):
            return False
        if not getattr(device, 'os', None):
            return False
        if device.os.name().find('2000') >= 0:
            return False
        if device.os.name().find('NT') >= 0:
            return False
        return True

    def queries(self):
        return{
        "Win32_IP4RouteTable": \
        "Select %s From Win32_IP4RouteTable" % ",".join(self.attrs),
    }
    
    def process(self, device, results, log):
        """convert query results to relMaps"""
        log.info('processing %s for device %s', self.name(), device.id)        
        localOnly = getattr(device, 'zIpRouteMapCollectOnlyLocal', False)
        indirectOnly = getattr(device, 'zIpRouteMapCollectOnlyIndirect', False)
        maps = []
        rm = self.relMap()
        for r in results["Win32_IP4RouteTable"]:
            if r.destination is not None:
                om = self.objectMap()
                om.id = self.prepId(r.destination)
                om.routemask = self.maskToBits(r.mask)
            
                om.setInterfaceIndex = r.interfaceindex
                om.setNextHopIp = r.nexthop
                om.routeproto = int(r.protocol)
                om.routetype = int(r.type)
                om.metric1 = r.metric1
                om.metric2 = r.metric2
                om.metric3 = r.metric3
                om.metric4 = r.metric4
                om.metric5 = r.metric5
            
                if not hasattr(om, "id"): continue
                if not hasattr(om, "routemask"): continue
                om.routemask = self.maskToBits(r.mask)
                om.setTarget = om.id + "/" + str(om.routemask)
                om.id = om.id + "_" + str(om.routemask)
            
                if om.routemask == 32: continue
                om.routeproto = self.mapSnmpVal(om.routeproto, self.routeProtoMap)
                if localOnly and om.routeproto != 'local':
                    continue
                if not hasattr(om, 'routetype'): 
                    continue    
                om.routetype = self.mapSnmpVal(om.routetype, self.routeTypeMap)
                if indirectOnly and om.routetype != 'indirect':
                    continue
                rm.append(om)
        maps.append(rm)
        return rm

    def mapSnmpVal(self, value, map):
        if len(map)+1 >= value:
            value = map[value-1]
        return value
    
    routeTypeMap = ('other', 'invalid', 'direct', 'indirect')
    routeProtoMap = ('other', 'local', 'netmgmt', 'icmp',
            'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is',
            'ciscoIgrp', 'bbnSpfIgrp', 'ospf', 'bgp')
