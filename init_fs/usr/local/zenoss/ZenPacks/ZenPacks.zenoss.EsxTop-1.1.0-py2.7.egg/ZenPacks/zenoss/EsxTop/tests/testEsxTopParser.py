##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase

from ZenPacks.zenoss.EsxTop.parsers.esx.esxtop import esxtop


class EsxTopParsersTestCase(BaseParsersTestCase):

    def testLinuxParsers(self):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        datadir = "%s/parserdata/esx" % os.path.dirname(__file__)
        
        parserMap = {
             "check_esxtop --statCategory='Group Cpu' --component=host": esxtop,
             "check_esxtop --statCategory='Memory'": esxtop,
        }
        
        self._testParsers(datadir, parserMap)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(EsxTopParsersTestCase))
    return suite
