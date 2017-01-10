##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals

from Products.ZenModel.Device import Device, manage_createDevice
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.WindowsMonitor.services.EventLogConfig import EventLogConfig

class TestEventLogConfig(BaseTestCase):
    def afterSetUp(self):
        super(TestEventLogConfig, self).afterSetUp()
        dev = manage_createDevice(self.dmd, "test-dev1",
                                  "/Server/Windows",
                                  manageIp="10.0.10.1")
        dev.zWmiMonitorIgnore = False
        dev.zWinEventlog = True
        self._testDev = dev
        self._deviceNames = [ "test-dev1" ]
        self._configService = EventLogConfig(self.dmd, "localhost")

    def beforeTearDown(self):
        self._testDev = None
        self._deviceNames = None
        self._configService = None
        super(TestEventLogConfig, self).beforeTearDown()

    def testProductionStateFilter(self):
        self._testDev.setProdState(-1)

        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)

        self._testDev.setProdState(1000)
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

    def testWmiMonitorFlagFilter(self):
        self._testDev.zWmiMonitorIgnore = True
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)

        self._testDev.zWmiMonitorIgnore = False
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

    def testEventLogFlagFilter(self):
        self._testDev.zWinEventlog = False
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 0)

        self._testDev.zWinEventlog = True
        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertEqual(len(proxies), 1)

    def testMultipleDevices(self):
        dev = manage_createDevice(self.dmd, "test-dev2",
                                  "/Server/Windows",
                                  manageIp="10.0.10.2")
        dev.zWmiMonitorIgnore = False
        dev.zWinEventlog = True
        self._deviceNames.append("test-dev2")

        proxies = self._configService.remote_getDeviceConfigs(self._deviceNames)
        self.assertTrue(len(proxies), 2)

        proxies = self._configService.remote_getDeviceConfigs(None)
        self.assertTrue(len(proxies), 2)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEventLogConfig))
    return suite

if __name__=="__main__":
    framework()
