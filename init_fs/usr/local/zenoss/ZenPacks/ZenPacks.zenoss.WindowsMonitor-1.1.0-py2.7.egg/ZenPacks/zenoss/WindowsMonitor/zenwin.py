#! /usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2006-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


"""
This module provides a collector daemon that polls Windows devices for changes
to Windows services. Retrieved status is then converted into Zenoss events
and sent back to ZenHub for further processing.
"""

import logging
import traceback

# IMPORTANT! The import of the pysamba.twisted.reactor module should come before
# any other libraries that might possibly use twisted. This will ensure that
# the proper WmiReactor is installed before anyone else grabs a reference to
# the wrong reactor.
import pysamba.twisted.reactor

import Globals
import zope.component
import zope.interface

from twisted.internet import defer

from Products.ZenCollector.daemon import CollectorDaemon
from Products.ZenCollector.interfaces import ICollectorPreferences,\
                                             IEventService,\
                                             IScheduledTask
from Products.ZenCollector.tasks import SimpleTaskFactory,\
                                        SimpleTaskSplitter,\
                                        TaskStates
from Products.ZenEvents.ZenEventClasses import Error, Clear, Status_WinService, Status_Wmi
from Products.ZenUtils.observable import ObservableMixin
from ZenPacks.zenoss.WindowsMonitor.WMIClient import WMIClient
from ZenPacks.zenoss.WindowsMonitor.Watcher import Watcher
from ZenPacks.zenoss.WindowsMonitor.utils import addNTLMv2Option, setNTLMv2Auth

# We retrieve our configuration data remotely via a Twisted PerspectiveBroker
# connection. To do so, we need to import the class that will be used by the
# configuration service to send the data over, i.e. DeviceProxy.
from Products.ZenUtils.Utils import unused
from Products.ZenCollector.services.config import DeviceProxy
unused(DeviceProxy)
from ZenPacks.zenoss.WindowsMonitor.services.WinServiceConfig import WinServiceConfig
unused(WinServiceConfig)

#
# creating a logging context for this module to use
#
log = logging.getLogger("zen.zenwin")

# Create an implementation of the ICollectorPreferences interface so that the
# ZenCollector framework can configure itself from our preferences.
class ZenWinPreferences(object):
    zope.interface.implements(ICollectorPreferences)
    
    def __init__(self):
        """
        Construct a new ZenWinPreferences instance and provide default
        values for needed attributes.
        """
        self.collectorName = "zenwin"
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 5 * 60 # seconds
        self.configCycleInterval = 20 # minutes

        # set a reasonable default number of allowed concurrent collection tasks
        self.maxTasks = 50

        self.options = None
        
        # the configurationService attribute is the fully qualified class-name
        # of our configuration service that runs within ZenHub
        self.configurationService = 'ZenPacks.zenoss.WindowsMonitor.services.WinServiceConfig'
        
        self.wmibatchSize = 10
        self.wmiqueryTimeout = 1000
        
    def buildOptions(self, parser):
        parser.add_option('--debug', dest='debug', default=False,
                               action='store_true',
                               help='Increase logging verbosity.')
        parser.add_option('--proxywmi', dest='proxywmi',
                               default=False, action='store_true',
                               help='Use a process proxy to avoid long-term blocking'
                               )
        parser.add_option('--queryTimeout', dest='queryTimeout',
                               default=None, type='int',
                               help='The number of milliseconds to wait for ' + \
                                    'WMI query to respond. Overrides the ' + \
                                    'server settings.')
        parser.add_option('--batchSize', dest='batchSize',
                               default=None, type='int',
                               help='Number of data objects to retrieve in a ' +
                                    'single WMI query.')
        addNTLMv2Option(parser)

    def postStartup(self):
        # turn on low-level pysamba debug logging if requested
        logseverity = self.options.logseverity
        if logseverity <= 5:
            pysamba.library.DEBUGLEVEL.value = 99

        # force NTLMv2 authentication if requested
        setNTLMv2Auth(self.options)


class ZenWinTask(ObservableMixin):
    zope.interface.implements(IScheduledTask)
        
    STATE_WMIC_CONNECT = 'WMIC_CONNECT'
    STATE_WMIC_QUERY = 'WMIC_QUERY'
    STATE_WMIC_PROCESS = 'WMIC_PROCESS'
    STATE_WATCHER_CONNECT = 'WATCHER_CONNECT'
    STATE_WATCHER_QUERY = 'WATCHER_QUERY'
    STATE_WATCHER_PROCESS = 'WATCHER_PROCESS'
    
    # windows service states from wmi queries (lowercased)
    RUNNING = "running"
    STOPPED = "stopped"
    
    def __init__(self,
                 deviceId,
                 taskName,
                 scheduleIntervalSeconds,
                 taskConfig):
        """
        Construct a new task instance to watch for Windows Event Log changes
        for the specified device.
        
        @param deviceId: the Zenoss deviceId to watch
        @type deviceId: string
        @param taskName: the unique identifier for this task
        @type taskName: string
        @param scheduleIntervalSeconds: the interval at which this task will be
               collected
        @type scheduleIntervalSeconds: int
        @param taskConfig: the configuration for this task
        """
        super(ZenWinTask, self).__init__()
        
        self.name = taskName
        self.configId = deviceId
        self.interval = scheduleIntervalSeconds
        self.state = TaskStates.STATE_IDLE
        
        self._taskConfig = taskConfig
        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp
        
        self._eventService = zope.component.queryUtility(IEventService)
        self._preferences = zope.component.queryUtility(ICollectorPreferences,
                                                        "zenwin")
                                                        
        # if the user hasn't specified the batchSize or queryTimeout as command
        # options then use whatever has been specified in the collector
        # preferences
        # TODO: convert these to zProperties
        self._batchSize = self._preferences.options.batchSize
        if not self._batchSize:
            self._batchSize = self._preferences.wmibatchSize
        self._queryTimeout = self._preferences.options.queryTimeout
        if not self._queryTimeout:
            self._queryTimeout = self._preferences.wmiqueryTimeout
            
        self._wmic = None # the WMIClient
        self._watcher = None
        self._reset()
        
    def _reset(self):
        """
        Reset the WMI client and notification query watcher connection to the
        device, if they are presently active.
        """
        if self._wmic:
            self._wmic.close()
        self._wmic = None
        if self._watcher:
            self._watcher.close()
        self._watcher = None
        
    def _sendWinServiceEvent(self, name, summary, severity):
        event = {'summary': summary,
                 'eventClass': Status_WinService,
                 'device': self._devId,
                 'severity': severity,
                 'agent': 'zenwin',
                 'component': name,
                 'eventGroup': 'StatusTest'}
        self._eventService.sendEvent(event)
    
    def _isRunning(self, state):
        return state.lower() == self.RUNNING

    def _cacheServiceState(self, service):
        if service.name in self._taskConfig.services:
            _, stoppedSeverity, _, monitoredStartModes = self._taskConfig.services[service.name]

            running = self._isRunning(service.state)
            log.debug("Service %s has initial state: %s mode: %s", 
                        service.name, service.state, service.startMode)
            self._taskConfig.services[service.name] =\
                (running, stoppedSeverity, service.startMode, monitoredStartModes)

    def _handleResult(self, name, state, startMode):
        """
        Handle a result from the wmi query. Results from both the initial WMI
        client query and the watcher's notification query are processed by
        this method. Log running and stopped transitions. Send an event if the
        service is monitored.
        """
        if state is None:
            state = "unknown"
        state = state.lower()
        summary = "Windows service '%s' is %s" % (name, state)
        logLevel = logging.DEBUG
        if name in self._taskConfig.services:
            was_running, stoppedSeverity, oldStartMode, monitoredStartModes = \
                self._taskConfig.services[name]

            running = self._isRunning(state)
            service_was_important = (oldStartMode in monitoredStartModes)
            service_is_important = (startMode in monitoredStartModes)

            logLevel = logging.INFO
            if service_is_important:
                if running:
                    self._sendWinServiceEvent(name, summary, Clear)
                else:
                    self._sendWinServiceEvent(name, summary, stoppedSeverity)
                    logLevel = logging.CRITICAL
            else:
                self._sendWinServiceEvent(name, summary, Clear)

            self._taskConfig.services[name] = (
                running, stoppedSeverity, startMode, monitoredStartModes)

        logState = state
        if startMode == '' or startMode is None:
            logState = "unknown"
        summary = "Windows service '%s' is %s" % (name, logState)
        log.log(logLevel, '%s on %s', summary, self._devId)
        
    def cleanup(self):
        return self._reset()

    @defer.inlineCallbacks
    def _connect(self):
        log.debug("Connecting to %s [%s]", self._devId, self._manageIp)
        self.state = ZenWinTask.STATE_WMIC_CONNECT
        self._wmic = WMIClient(self._taskConfig)
        yield self._wmic.connect()
        
        self.state = ZenWinTask.STATE_WMIC_QUERY
        wql = "SELECT Name, State, StartMode FROM Win32_Service"
        result = yield self._wmic.query({'query': wql})
        
        self.state = ZenWinTask.STATE_WMIC_PROCESS
        for service in result['query']:
            self._cacheServiceState(service)
        self._wmic.close()
        self._wmic = None
        
        self.state = ZenWinTask.STATE_WATCHER_CONNECT
        wql = "SELECT * FROM __InstanceModificationEvent WITHIN 5 "\
              "WHERE TargetInstance ISA 'Win32_Service'"
        self._watcher = Watcher(self._taskConfig, wql)
        yield self._watcher.connect()

        log.debug("Connected to %s [%s]", self._devId, self._manageIp)
    
    @defer.inlineCallbacks
    def doTask(self):
        log.debug("Scanning device %s [%s]", self._devId, self._manageIp)
        
        try:
            # see if we need to connect first before doing any collection
            if not self._watcher:
                yield self._connect()
    
            # try collecting events after a successful connect, or if we're already
            # connected
            if self._watcher:
                log.debug("Polling for events from %s [%s]", self._devId, self._manageIp)
        
                # make a local copy of monitored services list
                services = self._taskConfig.services.copy()
                
                # read until we get an empty results list returned from our query
                self.state = ZenWinTask.STATE_WATCHER_QUERY
                results = []
                while True:
                    newresults = yield self._watcher.getEvents(self._queryTimeout, self._batchSize)
                    if not newresults:
                        break
                    results.extend(newresults)
                    log.debug("Queuing another fetch for %s [%s]", self._devId, self._manageIp)

                if log.isEnabledFor(logging.DEBUG):
                    showattrs = lambda ob,attrs: tuple(getattr(ob,attr,'') for attr in attrs)
                    log.debug("Successful collection from %s [%s], results=%s",
                              self._devId, self._manageIp, 
                              [showattrs(r.targetInstance, ('name','state','startmode')) for r in results]
                              )

                self.state = ZenWinTask.STATE_WATCHER_PROCESS

                # collapse repeated results for same service - this maintains our
                # state model from collection to collection, without weird 
                # intermediate states caused by multiple service state and 
                # configuration changes between collections messing things up
                results_summary = {}
                for r in results:
                    result = r.targetInstance
                    if result.state:
                        results_summary[result.name] = r

                # now process all results to update service state
                # and emit CRITICAL/CLEAR events as needed
                for r in results_summary.itervalues():
                    result = r.targetInstance
                    # remove service from local copy
                    services.pop(result.name, None)
                    self._handleResult(result.name, result.state, result.startmode)

                # send events for the services that did not show up in results
                for name, data in services.iteritems():
                    running, failSeverity, startMode, monitoredStartModes = data
                    if running:
                        state = self.RUNNING
                    else:
                        state = self.STOPPED
                    self._handleResult(name, state, startMode)

                msg = 'WMI connection to %s up.' % self._devId
                self._eventService.sendEvent(dict(
                    summary=msg,
                    eventClass=Status_Wmi,
                    device=self._devId,
                    severity=Clear,
                    component='zenwin'))

                log.debug("Device %s [%s] scanned successfully",
                          self._devId, self._manageIp)
        except Exception as e:
            err = str(e)
            log.debug("Device %s [%s] scanned failed, %s",
                      self._devId, self._manageIp, err)

            log.error("Unable to scan device %s: %s", self._devId, err)

            self._reset()

            summary = """
                Could not read Windows services (%s). Check your
                username/password settings and verify network connectivity.
                """ % err

            self._eventService.sendEvent(dict(
                summary=summary,
                component='zenwin',
                eventClass=Status_Wmi,
                device=self._devId,
                severity=Error,
                traceback=traceback.format_exc()
                ))

#
# Collector Daemon Main entry point
#
if __name__ == '__main__':
    myPreferences = ZenWinPreferences()
    myTaskFactory = SimpleTaskFactory(ZenWinTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)
    daemon = CollectorDaemon(myPreferences, myTaskSplitter)
    daemon.run()
