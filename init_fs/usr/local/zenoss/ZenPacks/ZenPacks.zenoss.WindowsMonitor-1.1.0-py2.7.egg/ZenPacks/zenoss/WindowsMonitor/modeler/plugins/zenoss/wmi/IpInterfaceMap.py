##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """IpInterfaceMap
Model Windows IP interfaces using WMI
"""

import re

from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin
from Products.ZenUtils.IpUtil import checkip, IpAddressError
from ZenPacks.zenoss.WindowsMonitor.PerfmonInstance import standardizeInstance


class IpInterfaceMap(WMIPlugin):
    """
    Retrieve network interfaces
    """
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zInterfaceMapIgnoreNames',
                                              'zInterfaceMapIgnoreTypes')

    def queries(self):
        return  {
        "Win32_NetworkAdapterConfiguration": \
        "Select * From Win32_NetworkAdapterConfiguration",
        "Win32_PerfRawData_Tcpip_NetworkInterface": \
        "Select * From Win32_PerfRawData_Tcpip_NetworkInterface",
    }
    
    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        skipifregex = getattr(device, 'zInterfaceMapIgnoreNames', None)
        log.debug( "zIpInterfaceMapIgnoreNames = '%s'" % skipifregex )

        maps = []
        rm = self.relMap()

        adapterResults = results["Win32_NetworkAdapterConfiguration"]
        raw = results["Win32_PerfRawData_Tcpip_NetworkInterface"]

        perfmonInstanceMap = self.buildPerfmonInstances(adapterResults, log)
        
        for adapter in adapterResults:
            if adapter.description is not None:
                if skipifregex and re.match( skipifregex, adapter.description ):
                    log.debug( "Interface %s matched regex -- skipping" % \
                               adapter.description)
                    continue

                om = self.objectMap()

                ips = []
                if adapter.ipaddress:
                    log.debug("Network adapter '%s' has IP addresses of %s/%s", 
                              adapter.description, adapter.ipaddress, adapter.ipsubnet)
                    for ipRecord, ipMask in zip(adapter.ipaddress, adapter.ipsubnet):
                        # make sure the IP Address for this adapter is valid
                        # invalid addresses will usually mean IPv6
                        try:
                            checkip(ipRecord)
                            if not ipMask:
                                raise IpAddressError()

                            ipEntry = '%s/%s' % (ipRecord, self.maskToBits(ipMask))
                            log.debug("Adding IP entry %s", ipEntry)
                            ips.append(ipEntry)
                        except IpAddressError:
                            log.debug("Invalid IP address %s encountered and "
                                      "skipped", ipRecord)

                om.setIpAddresses = ips
                om.interfaceName = adapter.description
                om.macaddress = adapter.macaddress
                om.description = adapter.description
                om.mtu = adapter.mtu
                om.monitor = om.operStatus = bool(adapter.ipenabled)
                om.id = self.prepId(adapter.description)

                # Windows XP, Windows 2000, and Windows NT 4.0:  
                # This property is not available. Use the Index instead if not
                # not available.
                try:
                    om.ifindex = adapter.interfaceindex
                except AttributeError:
                    om.ifindex = adapter.index

                if perfmonInstanceMap.has_key(adapter.index):
                    om.perfmonInstance = perfmonInstanceMap[adapter.index]
                else:
                    log.warning("Adapter '%s':%d does not have a perfmon "
                                "instance name and will not be monitored for "
                                "performance data", adapter.description, 
                                adapter.index)

                # These virtual adapters should not be monitored as they are
                # like loopback, and are NOT available via perfmon
                if 'Microsoft Failover Cluster Virtual Adapter' in om.description:
                    om.monitor = False

                # TODO expensive O(n^2) algorithm to worry about if N gets large
                for data in raw:
                    if data.Name == adapter.description:
                        om.speed = data.CurrentBandwidth
            
                om.id = self.prepId(adapter.description)
                rm.append(om)
        maps.append(rm)
        return maps
    
    # builds a dictionary of perfmon instance paths for each network adapter
    # found in the WMI results query, keyed by the Index attribute
    #
    # the performon instance path is uses the following format:
    # \Network Interface(%instancename%#%index%)
    #
    # If multiple adapters are present with the same description then the #
    # sign followed by an index number for all additional instances beyond the
    # very first one. The index number does not correspond to the value found
    # in the Index or InterfaceIndex attribute directly, but instead is just a
    # simple counter for each instance of the same name found. The instances
    # are sorted by the InterfaceIndex or Index attribute to ensure that they 
    # will receive the same calculated index value that perfmon uses.
    #
    # TOOD: this method can be made generic for all perfmon data that has
    # multiple instances and should be moved into WMIPlugin or some other
    # helper class.
    def buildPerfmonInstances(self, adapters, log):
        # don't bother with adapters without a description or interface index
        adapters = [a for a in adapters 
                      if getattr(a, 'description', None) is not None and 
                         getattr(a, 'index', None) is not None]
        
        def compareAdapters(a, b):
            n = cmp(a.description, b.description)
            if n == 0:
                n = cmp(a.index, b.index)
            return n
        adapters.sort(compareAdapters)

        # use the sorted interfaces to determine the perfmon unique instance
        # path 
        instanceMap = {}
        index = 0
        prevDesc = None
        for adapter in adapters:
            # if we've encountered the same description multiple times in a row
            # then increment the index for this description for the additional 
            # instances, otherwise build a perfmon-compatible description and
            # reset the index
            desc = adapter.description
            if desc == prevDesc:
                index += 1
            else:
                index = 0
                prevDesc = standardizeInstance(desc)
            
            # only additional instances need the #index appended to the instance
            # name - the first item always appears without that qualifier
            if index > 0:
                perfmonInstance = '\\Network Interface(%s#%d)' % (prevDesc,
                                                                  index)
            else:
                perfmonInstance = '\\Network Interface(%s)' % prevDesc

            log.debug("%d=%s", adapter.index, perfmonInstance)
            instanceMap[adapter.index] = perfmonInstance
            
        return instanceMap
