#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2009, 2011, 2012, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


"""
Windows Performance Monitoring daemon that fetches perfmon data remotely using
the Windows remote registry API. 
"""

import logging
import sys
import os

# IMPORTANT! The import of the pysamba.twisted.reactor module should come before
# any other libraries that might possibly use twisted. This will ensure that
# the proper WmiReactor is installed before anyone else grabs a reference to
# the wrong reactor.
import pysamba.twisted.reactor
import pysamba.library

import Globals
import zope.interface
import zope.component
from Products.Five import zcml

from twisted.internet import defer, reactor, task

from PerfRpc import PerfRpc
from Products.ZenCollector.interfaces import ICollectorPreferences, ICollectorWorker
from Products.ZenCollector.tasks import TaskStates
from Products.ZenEvents.Event import Warning, Clear
from Products.ZenEvents.ZenEventClasses import Status_Wmi, Debug
from ZenPacks.zenoss.WindowsMonitor.utils import addNTLMv2Option, setNTLMv2Auth
from Products.ZenCollector.CollectorCmdBase import CollectorCmdBase
from ZenPacks.zenoss.WindowsMonitor.services.WinPerfConfig import WinPerfDataSource

#
# creating a logging context for this module to use
#
log = logging.getLogger("zen.zenwinperf")

class ZenWinPerfPreferences(object):
    zope.interface.implements(ICollectorPreferences)

    def __init__(self):
        """
        Constructs a new ZenWinPerfConfiguration instance and provides default
        values for needed attributes.
        """
        self.collectorName = "zenwinperf"
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 5 * 60 # seconds
        self.configCycleInterval = 20 # minutes
        self.configurationService = 'ZenPacks.zenoss.WindowsMonitor.services.WinPerfConfig'

        # set a reasonable default number of allowed concurrent collection tasks
        self.maxTasks = 50

        self.options = None
        self.dispatcher = 'ZenPacks.zenoss.EnterpriseCollector.DispatchingStrategy.DeviceAffineDispatching'

    def buildOptions(self, parser):
        parser.add_option('--testCounter',
                          dest='testcounter',
                          default=None,
                          help='Perform a test read of this one counter'
                          )
        parser.add_option('--captureFile',
                          dest='capturefile',
                          default=None,
                          help="Filename prefix to capture data into")
        addNTLMv2Option(parser)

    def postStartup(self):
        # turn on low-level pysamba debug logging if requested
        logseverity = self.options.logseverity
        if logseverity <= 5:
            pysamba.library.DEBUGLEVEL.value = 99

        # force NTLMv2 authentication if requested
        setNTLMv2Auth(self.options)

class ZenWinPerfCollector(object):
    STATE_CONNECTING = 'CONNECTING'
    STATE_COLLECTING = 'COLLECTING'

    CLEAR_EVENT = dict(component="zenwinperf",
                       severity=Clear,
                       eventClass=Status_Wmi)

    WARNING_EVENT = dict(component="zenwinperf",
                         severity=Warning,
                         eventClass=Status_Wmi)

    COLLECTION_INIT_CYCLE_LENGTH = 2
    INIT_FETCH_INTERVAL = 2
    
    def __init__(self, deviceId, taskConfig):

#        self.name = taskName
        self.configId = deviceId
        self.interval = 1 # TODO - should be taskConfig.zWinPerfCycleSeconds
        self.state = TaskStates.STATE_IDLE

        self._taskConfig = taskConfig

        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp

        self.clearEvent = ZenWinPerfCollector.CLEAR_EVENT.copy()
        self.clearEvent.update({'device':deviceId, 
                                'summary':'Device collected successfully'})
        
        self.failEvent = ZenWinPerfCollector.WARNING_EVENT.copy()
        self.failEvent.update({'device':deviceId})
        
        cmdOptions = self._taskConfig.options
        self._captureFile = cmdOptions.get('capturefile', None)
        self._testCounter = cmdOptions.get('testcounter', None)
        self._ntlmv2auth = cmdOptions.get('ntlmv2auth', False)

        self._perfRpc = None
        self._reset()

    @defer.inlineCallbacks
    def _reset(self):
        """
        Reset the PerfRpc connection and collection stats so that collection 
        can start over from scratch.
        """
        if self._perfRpc:
            yield self._perfRpc.stop()

        self._perfRpc = None
        self._dataCollectCount = 0

    def _getCredentials(self):
        return "{0.zWinUser}%{0.zWinPassword}".format(self._taskConfig)
    
    @defer.inlineCallbacks
    def collect(self):
        successfulScan = False
        datapointsForRRD = []
        collectExceptionMsg = ''
        self.eventsBuffer = []
        
        log.debug("Scanning device %s [%s]", self._devId, self._manageIp)
    
        # see if we need to connect first before doing any collection
        if not self._perfRpc:
            try:
                self.state = ZenWinPerfCollector.STATE_CONNECTING
                log.debug("Connecting to %s [%s]", self._devId, self._manageIp)
        
                if self._testCounter:
                    counters = [self._testCounter]
                else:
                    counters = [dp['counter'] for dp in self._taskConfig.dpInfo]
        
                self._perfRpc = PerfRpc(counters, self._captureFile, self._ntlmv2auth)
                self._perfRpc.ownerDevice = self
                yield self._perfRpc.connect(self._manageIp, self._getCredentials())                
                log.debug("Connected to %s [%s]", self._devId, self._manageIp)

                # if this is a new connection, initialize with 'n' fetches
                # (Windows needs to warm up)
                for _ in range(self.COLLECTION_INIT_CYCLE_LENGTH):
                    log.debug("Waiting %d s before collecting for device %s [%s]",
                              self.INIT_FETCH_INTERVAL, self._devId, self._manageIp)
                    self.state = TaskStates.STATE_WAITING
                    yield self._perfRpc.fetch()
                    # a slight delay
                    yield task.deferLater(reactor, float(self.INIT_FETCH_INTERVAL), lambda : None)

            except Exception as e:
                collectExceptionMsg = str(e)
                err = str(e) #.getErrorMessage()
                log.error("Unable to scan device %s: %s", self._devId, err)
        
                yield self._reset()
                self.sendEvent(self.failEvent,
                    summary="Error collecting performance data: {}".format(err))

        if self._perfRpc:
            self.state = ZenWinPerfCollector.STATE_COLLECTING
            log.debug("Collecting data for %s [%s]", self._devId, self._manageIp)
            try:
                # collect our actual performance data
                values = yield self._perfRpc.fetch()
                self._dataCollectCount += 1
                        
                log.debug("Successful collection from %s [%s], result=%s", self._devId, self._manageIp, values)
                successfulScan = True
        
                for dataPoint in self._taskConfig.dpInfo:
                    try:
                        value = values.get(dataPoint['counter'], None)
                        datapointsForRRD.append(dict(path=dataPoint['path'],
                                                    value=value,
                                                    rrdType=dataPoint['rrdType'],
                                                    rrdCommand=dataPoint['rrdCmd'],
                                                    cycleTime=self.interval,
                                                    min=dataPoint['minv'],
                                                    max=dataPoint['maxv'],
                                                    counter=dataPoint['counter']) )
                    except Exception:
                        log.exception("Unable to write datapoint for counter %s on device %s [%s]",
                                      dataPoint['counter'], self._devId, self._manageIp)
        
                # if asked to test a counter we need to display the results!
                if self._testCounter:
                    if self._testCounter in values:
                        log.info("Collected value for %s: %s", self._testCounter, values[self._testCounter])
                    else:
                        log.info("Unable to collect value for %s", self._testCounter)
        
                # report CLEAR event representing successful data collection
                self.sendEvent(self.clearEvent)

                log.debug("Successful scan of %s [%s] (%d) (%d datapoints)",
                          self._devId, self._manageIp, self._dataCollectCount, len(values))

            except Exception as e:
                collectExceptionMsg = str(e)
                err = str(e)
                log.error("Unable to scan device %s: %s", self._devId, err)
        
                yield self._reset()
                self.sendEvent(self.failEvent,
                    summary = "Error collecting performance data: {}".format(err))
                
            finally:
                # reset the PerfRpc connection if we've reached the
                # cyclesPerConnection threshold for the device
                if self._dataCollectCount >= self._taskConfig.cyclesPerConnection:
                    log.debug("Resetting connection to %s [%s] after %d cycles",
                              self._devId, self._manageIp, self._dataCollectCount)
                    yield self._reset()
            
            if successfulScan:
                log.debug("Successful scan of %s [%s] completed", self._devId, self._manageIp)
            else:
                log.debug("Unsuccessful scan of %s [%s] completed, result=%s", self._devId, self._manageIp, collectExceptionMsg)

        # send collected data and/or events back to dispatcher
        defer.returnValue( (datapointsForRRD, self.eventsBuffer) )
    
    def sendEvent(self, evt, **kwargs):
        evt = evt.copy()
        evt.update(kwargs)
        self.eventsBuffer.append(evt)


class ZenWinPerfWorker(object):
    zope.interface.implements(ICollectorWorker)

    def prepareToRun(self):
        self.deviceCollectorMap = {}

    @defer.inlineCallbacks
    def collect(self, device, taskConfig, *args):
        if device in self.deviceCollectorMap:
            coll = self.deviceCollectorMap[device]
        else:
            coll = ZenWinPerfCollector(device, taskConfig)
            self.deviceCollectorMap[device] = coll

        try:
            results = yield coll.collect()
        except Exception as e:
            results = []
            events = [{'device':device, 'severity':Debug, 'eventClass':Status_Wmi, 'summary':'Exception calling coll.collect:'+str(e)}]
        else:
            if results is not None:
                results, events = results
            else:
                results = []
                events = [{'device':device, 'severity':Debug, 'eventClass':Status_Wmi, 'summary':'None returned from coll.collect'}]

        defer.returnValue( (results, events) )

    @defer.inlineCallbacks
    def disconnect(self, device):
        coll = self.deviceCollectorMap.pop(device, None)
        if coll is not None:
            yield coll._reset()

    @defer.inlineCallbacks
    def stop(self):
        for coll in self.deviceCollectorMap.values():
            yield coll._reset()

if __name__ == "__main__":
    collector = CollectorCmdBase(ZenWinPerfWorker, ZenWinPerfPreferences, noopts=1)
    log = collector.log
    collector.run()
