##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
log = logging.getLogger("zen.testcases")
import os

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from ZenPacks.zenoss.XenMonitor.modeler.plugins.zenoss.cmd.Xen \
    import Xen


class TestXen(BaseTestCase):
    def afterSetUp(self):
        super(TestXen, self).afterSetUp()
        self.adm = ApplyDataMap()
        self.plugin = Xen()
        self.device = self.dmd.Devices.createInstance('testDevice')
        self.device.guestDevices = []
        log.setLevel(logging.ERROR)


    def _testTruncatedData(self, results, expectedVMs):
        """
        Data format can be truncated
        """
        # Verify that the modeler plugin processes the data properly.
        relmap = self.plugin.process(self.device, results, log)
        self.assertEquals(len(relmap[0].maps), expectedVMs)

    def testTruncatedData1(self):
        results = """Name ID Mem VCPUs State Time(s)
AD01_SIMSPOC 53 1024 2 -b---- 14331.1
AD02_SIMSPOC 43 1024 2 -b---- 15503.9
Domain-0 0 3765 16 r----- 11621.6
TS01_SIMSPOC 58 2048 2 -b---- 6058.3
TS02_SIMSPOC 54 2048 2 -b---- 11608.6
TSGW01_SIMSPOC 55 2048 1 -b---- 9271.8
TSGW02_SIMSPOC 48 2048 1 -b---- 9473.5
centos54_x32_GOLD 1024 1 86.3
centos54_x64_GOLD 1024 1 0.0
xenwin2k8x32GPLPV_GOLD 2048 1 0.0
xenwin2k8x32_GOLD 2048 1 0.0
xenwin2kx32_base 2048 1 28.8
zenoss_Centos54x32 57 2050 2 -b---- 2185.9
"""

        self._testTruncatedData(results,7)

    def testTruncatedData2(self):
        results = """Name                                      ID Mem(MiB) VCPUs State   Time(s)
Domain-0                                   0      294     1 r-----   1788.2
xenguest1                                  7      199     1 -b----     34.5
"""
        self._testTruncatedData(results,1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXen))
    return suite
