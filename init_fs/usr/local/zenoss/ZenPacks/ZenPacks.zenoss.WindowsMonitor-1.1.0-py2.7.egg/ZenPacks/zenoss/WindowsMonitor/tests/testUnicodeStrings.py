##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import unittest
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.WindowsMonitor.winreg_ import extractUnicodeString

class TestUnicodeStrings(BaseTestCase):

    # test the extraction of a Unicode string that ends in a NUL
    def testNulTerminated(self):
        testStr = u'_Total\u0000'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == u'_Total')

        testStr = u'yet another\u0000blah blah blah'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == 'yet another')

    # test the extraction of a Unicode string that does not end in a NUL
    # but simply occupies the full buffer space
    def testUnterminated(self):
        testStr = u'_Total'
        bytes = testStr.encode("utf-16-le")
        str = extractUnicodeString(bytes, 0, len(bytes), "utf-16-le")
        self.assert_(str == u'_Total')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUnicodeStrings))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
