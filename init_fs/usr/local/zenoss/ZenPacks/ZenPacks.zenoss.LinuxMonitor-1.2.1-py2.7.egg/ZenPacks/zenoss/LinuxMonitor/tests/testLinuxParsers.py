##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase
from Products.ZenRRD.parsers.uptime import uptime

from ZenPacks.zenoss.LinuxMonitor.parsers.linux.df import df
from ZenPacks.zenoss.LinuxMonitor.parsers.linux.dfi import dfi
from ZenPacks.zenoss.LinuxMonitor.parsers.linux.mem import mem

class LinuxParsersTestCase(BaseParsersTestCase):

    def testLinuxParsers(self):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        datadir = "%s/parserdata/linux" % os.path.dirname(__file__)
        
        parserMap = {'/bin/df -Pk': df,
                     '/bin/df -iPk': dfi,
                     '/usr/bin/uptime': uptime,
                     '/bin/cat /proc/meminfo': mem,
                     }
        
        self._testParsers(datadir, parserMap)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(LinuxParsersTestCase))
    return suite
