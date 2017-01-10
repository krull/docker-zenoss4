##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
import logging.handlers
import struct
import sys
import unittest
import os

from ZenPacks.zenoss.WindowsMonitor.winreg_ import PerformanceData, getCounterValue

log = logging.getLogger("zen.winperf.winreg")

class TestPerfData(unittest.TestCase):
    def _buildCounterMap(self, data):
        """
        Builds a dictionary of perfmon counter names and their indicies.

        @param data: a block of binary counter data in REG_MULTI_SZ format
        @return: dictionary of indicies to perfmon counter names
        @rtype: dictionary
        @todo: code borrowed from PerfRpc.py; refactor to reuse
        """
        # it's a null-separated list of number/name pairs
        def pairs(seq):
            i = iter(seq)
            while 1:
                yield (i.next(), i.next())

        counterMap = {}
        for index, name in pairs(data.decode('utf-16').split(u'\x00')):
            if index:
                value = name.decode('latin-1').lower()
                key = int(index)
                counterMap[key] = value

        return counterMap

    def _readTestFile(self, filename):
        """
        Opens and reads a file in the same directory as this test script. Does
        not depend on the current working directory to find the file, so you
        can run this test from any directory.
        """
        testFile = open(os.path.join(os.path.dirname(__file__), filename))
        try:
            return testFile.read()
        finally:
            testFile.close()

    def _loadCounters(self, prefixName):
        """
        Loads raw counter data from storage. Counter data is assumed to
        be named prefixName.counters

        @param prefixName: the prefix name of the counter file
        @return: dictionary of indicies to perfmon counter names
        @rtype: dictionary
        """
        return self._buildCounterMap(self._readTestFile(
                '%s.counters' % prefixName))
                
    def _loadPerfData(self, prefixName, counterDict):
        """
        Loads raw performance counter data from storage. Performance data 
        is assumed to be named prefixName-0.perf and prefixName-1.perf

        @param prefixName: the prefix name of the counter file
        @param counterDict: a previous computed counter name dictionary
        @return: parsed performance data objects
        @rtype: tuple of PerformanceData objects
        """
        def loadPerfDatum(id):
            data = self._readTestFile('%s-%s.perf' % (prefixName, id))
            return PerformanceData(data, counterDict)
        return loadPerfDatum(0), loadPerfDatum(1)

    def _testCounters(self, perfData, counters):
        """
        Tests that all of the specified performance counters are present
        in the provided performance data.

        @param perfData: tuple of PerformanceData objects
        @param counters: a list of counter paths to look up
        """
        for counter in counters:
            try:
                result = getCounterValue(counter, perfData[1], perfData[0])
                log.info("%r=%r", counter, result)
            except KeyError:
                result = None
            self.assert_(result != None, "'%s' not found" % counter)

    def _loadAndTestCounters(self, prefixName, counters):
        """
        Loads performance counter data from storage and tests the provided
        counter names.

        @param prefixName: the prefix of the performance data
        @param counters: a list of counter paths to look up
        """
        counterDict = self._loadCounters(prefixName)
        perfData = self._loadPerfData(prefixName, counterDict)
        self._testCounters(perfData, counters)

    def testBadSignature(self):
        """
        Unit test: create PERF_DATA_BLOCK with an invalid signature
        """
        bogusData = u'this is bogus!'.encode("utf-16-le")
        self.failUnlessRaises(RuntimeError, PerformanceData,
                              bogusData, None)

    def testBadLittleEndian(self):
        """
        Unit test: PERF_DATA_BLOCK with an invalid little endian value
        """
        bogusData = u'PERF'.encode("utf-16-le") + struct.pack("I", 99)
        self.failUnlessRaises(RuntimeError, PerformanceData, 
                              bogusData, None)

    def testMissingCounterName(self):
        """
        Unit test: captured performance data with a missing performance
        counter name.
        """
        counterDict = self._loadCounters("win2003")
        # delete a performance counter that is expected to be there
        del counterDict[24] # 24 = available bytes

        perfData = self._loadPerfData("win2003", counterDict)
        self.failUnlessRaises(KeyError, getCounterValue, 
                              "\Memory\Available bytes", 
                              perfData[1], perfData[0])

    def testWindows(self):
        """
        Unit test: test common performance counters available on any
        Windows device.
        """
        testCounters = (
            r"\Memory\Available bytes",
            r"\Memory\Committed Bytes",
            r"\Memory\Pages Input/sec",
            r"\Memory\Pages Output/sec",
            r"\Paging File(_Total)\% Usage",
            r"\Processor(_Total)\% Privileged Time",
            r"\Processor(_Total)\% Processor Time",
            r"\Processor(_Total)\% User Time",
            r"\System\System Up Time",
            )
        self._loadAndTestCounters("win2003", testCounters)

    def testExchange(self):
        """
        Unit test: test performance counters available on MS Exchange
        installations.
        """
        testCounters = (
            r"\LogicalDisk(_Total)\Free Megabytes",
            r"\Memory\% Committed Bytes In Use",
            r"\MSExchangeIS Mailbox(_Total)\Folder opens/sec",
            r"\MSExchangeIS Mailbox(_Total)\Local delivery rate",
            r"\MSExchangeIS Mailbox(_Total)\Message Opens/sec",
            r"\MSExchangeIS\RPC Averaged Latency",
            r"\MSExchangeIS\RPC Operations/sec",
            r"\MSExchangeIS\RPC Requests",
            r"\MSExchangeIS\VM Largest Block Size",
            r"\MSExchangeIS\VM Total 16MB Free Blocks",
            r"\MSExchangeIS\VM Total Free Blocks",
            r"\MSExchangeIS\VM Total Large Free Block Bytes",
            r"\PhysicalDisk(_Total)\Avg. Disk sec/Read",
            r"\PhysicalDisk(_Total)\Avg. Disk sec/Write",
            r"\PhysicalDisk(_Total)\Disk Transfers/sec",
            r"\Process(_Total)\% Processor Time",
            r"\Process(store)\% Processor Time",
            )
        self._loadAndTestCounters("s-exch2007-64", testCounters)

    def testCustomerData(self):
        testCounters = (
            r"\Memory\Available bytes",
            r"\Memory\Committed Bytes",
            r"\Memory\Pages Input/sec",
            r"\Memory\Pages Output/sec",
            r"\Paging File(_Total)\% Usage",
            r"\Processor(_Total)\% Privileged Time",
            r"\Processor(_Total)\% Processor Time",
            r"\ISA Server Firewall Packet Engine\Active Connections",
            r"\ISA Server Firewall Packet Engine\Bytes/sec",
            r"\ISA Server Firewall Packet Engine\Connections/sec",
            r"\ISA Server Firewall Packet Engine\Dropped Packets/sec",
            r"\ISA Server Firewall Packet Engine\Packets/sec",
            r"\ISA Server Firewall Service\Active Sessions",
            r"\ISA Server Firewall Service\Active TCP Connections",
            r"\ISA Server Firewall Service\Active UDP Connections",
            r"\ISA Server Web Proxy\Average Milliseconds/request",
            r"\ISA Server Web Proxy\Failing Requests/sec",
            r"\ISA Server Web Proxy\Requests/sec",
            )
        self._loadAndTestCounters("wrxxcrpisax01", testCounters)

    def testCustomerData2(self):
        testCounters = (
            r"\LogicalDisk(C:)\% Disk Write Time",
            r"\LogicalDisk(C:)\% Disk Read Time",
            r"\LogicalDisk(D:)\% Disk Write Time",
            r"\LogicalDisk(D:)\% Disk Read Time",
            r"\Memory\Available bytes",
            r"\Memory\Committed Bytes",
            r"\Memory\Pages Input/sec",
            r"\Memory\Pages Output/sec",
            r"\Paging File(_Total)\% Usage",
            r"\Processor(_Total)\% Privileged Time",
            r"\Processor(_Total)\% Processor Time",
            )
        self._loadAndTestCounters("wprepw01", testCounters)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPerfData))
    return suite

if __name__ == '__main__':
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    unittest.TextTestRunner(verbosity=2).run(test_suite())
