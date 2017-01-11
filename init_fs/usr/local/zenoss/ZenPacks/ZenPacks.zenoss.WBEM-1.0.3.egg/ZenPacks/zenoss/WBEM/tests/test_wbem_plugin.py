##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from mock import Mock, sentinel

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.WBEM.modeler.wbem import WBEMPlugin


class TestWBEMPlugin(BaseTestCase):

    def test_present(self):
        self.assertTrue(WBEMPlugin)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWBEMPlugin))
    return suite

