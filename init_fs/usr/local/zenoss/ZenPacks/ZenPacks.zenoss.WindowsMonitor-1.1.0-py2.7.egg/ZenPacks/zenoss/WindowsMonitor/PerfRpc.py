##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from pysamba.rpc.Rpc import Rpc
from pysamba.talloc import talloc_zero, talloc_array, talloc_free
from pysamba.composite_context import composite_context
from twisted.internet import defer
from ctypes import *

import Globals
from Products.ZenUtils.Driver import drive

import datetime
import logging

from winreg_ import *
from pysamba.library import library, logFuncCall

library.dcerpc_winreg_OpenHKPD_send.restype = c_void_p
library.dcerpc_winreg_OpenHKPD_send.argtypes = [c_void_p, c_void_p, c_void_p]
library.dcerpc_winreg_OpenHKPD_send = logFuncCall(library.dcerpc_winreg_OpenHKPD_send)
library.dcerpc_winreg_QueryValue_send.restype = c_void_p
library.dcerpc_winreg_QueryValue_send.argtypes = [c_void_p, c_void_p, c_void_p]
library.dcerpc_winreg_QueryValue_send = logFuncCall(library.dcerpc_winreg_QueryValue_send)
library.dcerpc_winreg_CloseKey_send.restype = c_void_p
library.dcerpc_winreg_CloseKey_send.argtypes = [c_void_p, c_void_p, c_void_p]
library.dcerpc_winreg_CloseKey_send = logFuncCall(library.dcerpc_winreg_CloseKey_send)

def pointerTo(obj):
    "Compute a typed pointer to an object"
    return cast(addressof(obj), POINTER(obj.__class__))

class FetchBeforeConnectedError(Exception): pass

class PerfRpc(Rpc):
    def __init__(self, counters, capturePath=None, ntlmv2auth=False):
        Rpc.__init__(self, ntlmv2auth)
        self.log = logging.getLogger("zen.winperf.PerfRpc")
        self.logLevel = log.getEffectiveLevel()
        self.counters = counters
        self.handle = None
        self.prev = None
        self.connected = False
        self.capturePath = capturePath
        self.fetches = 0
        self.ownerDevice = None

    def set_name(self, query):
        "Sent the query name in a QueryValue request"
        p = self.params.contents
        p._in.value_name.name = query
        p._in.value_name.name_len = 2 * library.strlen_m_term(query)
        p._in.value_name.name_size = p._in.value_name.name_len
        
    @defer.inlineCallbacks
    def connect(self, host, credentials):
        self.host = host
        
        yield Rpc.connect(self, host, credentials, 'winreg')

        params = talloc_zero(self.ctx, winreg_OpenHKPD)
        self.handle = talloc_zero(self.ctx, policy_handle)
        params.contents.out.handle = self.handle
        self.hkpt = yield self.call(library.dcerpc_winreg_OpenHKPD_send, params)
    
        # first learn how big the data is
        self.log.debug("Learning counter object ids")
        self.type = enum()
        self.size = uint32_t()
        self.out_size = uint32_t()
        self.length = uint32_t()
        self.type.value = self.size.value = self.length.value = 0
        self.params = talloc_zero(self.ctx, winreg_QueryValue)
        p = self.params.contents
        p._in.handle = self.handle
        self.set_name('Counters')
        p._in.type = p.out.type = pointerTo(self.type)
        p._in.size = pointerTo(self.size)
        p.out.size = pointerTo(self.out_size)
        p.out.length = p._in.length = pointerTo(self.length)
        p._in.data = p.out.data = None
        yield self.call(library.dcerpc_winreg_QueryValue_send, self.params)

        # allocate space
        sz = p.out.size.contents.value
        self.log.debug("size is %d", sz)
        p.out.data = p._in.data = talloc_array(params, uint8_t, sz)
        self.size.value = sz
        self.length.value = 0 # we don't need to xmit any raw data
        # now fetch it
        yield self.call(library.dcerpc_winreg_QueryValue_send, self.params)

        # now decode the mapping of counters to indexes
        REG_MULTI_SZ = 7
        data = string_at(p.out.data, p.out.length.contents.value)
        assert p.out.type.contents.value == REG_MULTI_SZ

        # save the counter data if requested to do so
        if self.capturePath:
            capFile = open("%s-%s-counters" % (self.capturePath, self.host), "w")
            capFile.write(data)
            capFile.close()

        # it's a null-separated list of number/name pairs
        def pairs(seq):
            i = iter(seq)
            while 1:
                yield (i.next(), i.next())
        self.counterMap = {}
        self.counterRevMap = {}
        for index, name in pairs(data.decode('utf-16').split(u'\x00')):
            if self.logLevel < logging.DEBUG:
                self.log.debug("Found counter: %r=%r", index, name)
            if index:
                key = name.decode('latin-1').lower()
                try:
                    value = int(index)
                except ValueError, e:
                    self.log.warn("Found non-numeric counter: %s=%s",
                        index, name)
                else:
                    self.counterMap[key] = value
                    self.counterRevMap[value] = key

        objects = set()
        for path in self.counters:
            try:
                counterObject = parseCounter(path)['object']
                objects.add(counterObject)
            except (AttributeError, KeyError):
                self.log.error("The counter name %s is invalid -- ignoring.", path)

        ids = []
        for obj in objects:
            if self.counterMap.has_key(obj):
                ids.append(self.counterMap[obj])
                self.log.debug("Found Perfmon Object: %r=%r", self.counterMap[obj], obj)
        ids.sort()
        query = ' '.join(map(str, ids))
        self.log.debug("Perfmon Object query: %s", query)
        self.set_name(query)
        self.connected = True

    @defer.inlineCallbacks
    def fetch(self):
        p = self.params.contents
        if not self.connected:
            raise FetchBeforeConnectedError()
        
        
        # don't bother fetching any data if there are no counters to fetch
        if not p._in.value_name.name:
            raise Exception("No PerfMon objects to query")


        ctx = talloc_zero(self.ctx, composite_context)
        try:
            # If hKey specifies HKEY_PERFORMANCE_DATA and the lpData buffer 
            # is not large enough to contain all of the returned data, 
            # RegQueryValueEx returns ERROR_MORE_DATA and the value returned 
            # through the lpcbData parameter is undefined. This is because 
            # the size of the performance data can change from one call to 
            # the next. In this case, you must increase the buffer size and 
            # call RegQueryValueEx again passing the updated buffer size in 
            # the lpcbData parameter. Repeat this until the function 
            # succeeds. You need to maintain a separate variable to keep 
            # track of the buffer size, because the value returned by 
            # lpcbData is unpredictable.
            while 1:
              self.log.debug("Fetching counters")
              self.length.value = 0 # we don't need to xmit any raw data
              yield self.call(library.dcerpc_winreg_QueryValue_send,
                              self.params,
                              ctx)

              if p.out.result.v == 234L: # ERROR_MORE_DATA
                sz = self.size.value + 65536
                self.log.debug("ERROR_MORE_DATA returned, increasing buffer size to %d", sz)
                talloc_free(p.out.data)
                p.out.data = p._in.data = talloc_array(self.params, uint8_t, sz)
                self.size.value = sz
                continue

              break

            data = string_at(p.out.data, p.out.length.contents.value)
            self.log.debug("Counter data fetched, length=%d",
                               p.out.length.contents.value)

            # save the raw data if requested to do so
            if self.capturePath:
                capFile = open("%s-%s-%d" % (self.capturePath, self.host, self.fetches), "w")
                capFile.write(data)
                capFile.close()
                self.fetches = self.fetches + 1

            perf = PerformanceData(data, self.counterRevMap)
            result = {}
            badCounterPaths = []
            for path in self.counters:
                try:
                    result[path] = getCounterValue(path, perf, self.prev)
                except (AttributeError, KeyError):
                    badCounterPaths.append(path)

            if badCounterPaths:
                summaryMsg = "Bad Counter(s) - %d bad counter(s) for device %s" % (len(badCounterPaths), self.host)
                self.log.warning(summaryMsg + " " + ", ".join(badCounterPaths))
                if self.ownerDevice is not None:
                    self.ownerDevice.sendEvent(
                        self.ownerDevice.WARNING_EVENT,
                        component = "zen.winperf.PerfRpc",
                        device = self.ownerDevice._devId,
                        eventKey = "bad_wmi_counter_consolidation_event",
                        summary = summaryMsg,
                        explanation = "These WMI performance counter(s) are being queried, but the specific performance counter(s) are not on the remote system",
                        resolution = "Stop monitoring the component or fix and/or remove the performance counter name from the monitoring template. 'typeperf -q' on the remote system will show available counters",
                        details = ", ".join(badCounterPaths))
            else:
                summaryMsg = "No bad counters detected for device %s" % (self.host)
                self.log.debug(summaryMsg)
                if self.ownerDevice is not None:
                    self.ownerDevice.sendEvent(
                        self.ownerDevice.CLEAR_EVENT,
                        component = "zen.winperf.PerfRpc",
                        device = self.ownerDevice._devId,
                        eventKey = "bad_wmi_counter_consolidation_event",
                        summary = summaryMsg)

            self.prev = perf
            talloc_free(ctx)
            ctx = None
            defer.returnValue(result)
        except Exception as ex:
            if ctx is not None:
                talloc_free(ctx)
                ctx = None
            raise


    @defer.inlineCallbacks
    def __del__(self):
        try:
            yield self.stop()
        finally:
            super(PerfRpc, self).__del__()
        
    @defer.inlineCallbacks
    def stop(self):
        if self.handle is not None:
            try:
                params = talloc_zero(self.handle, winreg_CloseKey)
                params.contents._in.handle = self.handle
                params.contents.out.handle = self.handle
                yield self.call(library.dcerpc_winreg_CloseKey_send, params)
            finally:
                talloc_free(self.handle)
                self.handle = None
                self.close()
                self.ownerDevice = None
