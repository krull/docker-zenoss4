##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Globals import InitializeClass
# from AccessControl import ClassSecurityInfo

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class VirtualMachine(DeviceComponent, ManagedEntity):
    "A component that is a virtual device"
    
    portal_type = meta_type = 'VirtualMachine'

    displayName = ""
    osType = ""
    memory = 0
    adminStatus = False
    snmpindex = -1
    operStatus = False

    _properties = (
        dict(id='memory',       type='int',      **_kw),
        dict(id='displayName',  type='string',   **_kw),
        dict(id='osType',       type='string',   **_kw),
        dict(id='adminStatus',  type='boolean',  **_kw),
        dict(id='snmpindex',    type='int',      **_kw),
        dict(id='operStatus',   type='boolean',  **_kw),
        )

    _relations = (
        ('host', ToOne(ToManyCont, 
        'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachineHost', 
            'guestDevices')),
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = (
        {
            'id'             : 'VirtualMachine',
            'meta_type'      : 'VirtualMachine',
            'description'    : 'Virtual Machine Description',
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenossVirtualHostMonitor',
            'factory'        : 'manage_addVirtualMachine',
            'immediate_view' : 'viewVirtualMachineSnmpPerformance',
            'actions'        :
            (
            )
        },
    )

    def device(self):
        return self.host()

    def memoryString(self):
        return convToUnits(self.memory * 1024 * 1024)

    def managedDeviceLink(self):
        from Products.ZenModel.ZenModelRM import ZenModelRM
        d = self.getDmdRoot("Devices").findDevice(self.displayName)
        if d:
            return ZenModelRM.urlLink(d, 'link')
        return None

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    

InitializeClass(VirtualMachine)
