##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.infos import ProxyProperty
from zope.interface import implements
from Products.Zuul.infos import InfoBase
from ZenPacks.zenoss.WindowsMonitor.interfaces import IWinPerfDataSourceInfo


class WinPerfDataSourceInfo(InfoBase):
    implements(IWinPerfDataSourceInfo)

    @property
    def id(self):
        return '/'.join( self._object.getPrimaryPath() )

    @property
    def source(self):
        return self._object.getDescription()
    
    @property
    def type(self):
        return self._object.sourcetype
    
    counter = ProxyProperty('counter')
    enabled = ProxyProperty('enabled')

    @property
    def testable(self):
        """
        We can test this datasource against a specific windows device
        """
        return True
