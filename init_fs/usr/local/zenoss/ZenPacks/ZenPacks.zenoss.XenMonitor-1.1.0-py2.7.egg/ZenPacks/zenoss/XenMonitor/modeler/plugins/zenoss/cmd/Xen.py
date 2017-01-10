##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""Xen
Plugin to gather information about virtual machines running
under Xen
"""

import Globals
from Products.DataCollector.plugins.CollectorPlugin \
     import CommandPlugin
from Products.DataCollector.plugins.DataMaps \
     import ObjectMap

class Xen(CommandPlugin):
    """
    Fetch data from a Xen server using ssh and the xm command
    """
    relname = "guestDevices"
    modname = 'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachine'
    command = '/usr/sbin/xm list'

    def copyDataToProxy(self, device, proxy):
        result = CommandPlugin.copyDataToProxy(self, device, proxy)
        proxy.guestDevices = [g.id for g in device.guestDevices()]
        return result
    
    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        log.debug('Results from %s = "%s"', self.command, results)

        rm = self.relMap()
        before = set(device.guestDevices)
        # Skip the first two lines, which are
        # the header line and the domain-0 line.
        for line in results.splitlines()[1:]:
            if not line or line.startswith('Domain-0'):
                continue

            try:
                # Name  ID Mem(MiB) VCPUs State  Time(s)
                name, id, memory, cpus, state, times = line.rsplit(None, 5)
            except ValueError:
                name = line.split()[0]
                log.warn("Ignoring %s as data missing (eg ID, Mem,"
                         " VCPUs, State or Time info): '%s'",
                         name, line)
                continue

            info = {}
            info['adminStatus'] = True
            info['operStatus'] = ('r' in state or 'b' in state)
            info['memory'] = int(memory)
            info['osType'] = 'Unknown'
            info['displayName'] = name
            om = self.objectMap(info)
            om.id = self.prepId(name)
            before.discard(om.id)
            rm.append(om)

        for id in before:
            om = self.objectMap(dict(adminStatus=False))
            om.id = id
            rm.append(om)

        return [rm]
