##########################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
# testNtpMonitorDataSource.py
#
##########################################################################

from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.ZenUtils.Utils import importClass

class TestNtpMonitorDataSource(BaseTestCase):

    def testClassLoading(self):
        """
        Test that the class can be imported from the module dynamically
        """
        moduleName = "ZenPacks.zenoss.NtpMonitor.datasources.NtpMonitorDataSource"
        className = "NtpMonitorDataSource"
        constructor = importClass(moduleName, className)
        self.assert_(constructor is not None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestNtpMonitorDataSource))
    return suite


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite')
