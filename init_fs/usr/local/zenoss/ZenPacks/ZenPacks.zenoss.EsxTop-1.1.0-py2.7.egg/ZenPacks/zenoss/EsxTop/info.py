##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from zope.interface import implements

from Products.Zuul.infos.component import ComponentInfo

from ZenPacks.zenoss.EsxTop.interfaces import *

class VirtualMachineInfo(ComponentInfo):
    implements(IVirtualMachineInfo)

    @property
    def monitored(self):
        return False

    @property
    def status(self):
        return 'Up'
