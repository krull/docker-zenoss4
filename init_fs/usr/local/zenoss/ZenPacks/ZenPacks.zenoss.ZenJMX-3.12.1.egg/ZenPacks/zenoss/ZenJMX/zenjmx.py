#! /usr/bin/env python
##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = """Monitor Java Management eXtension (JMX) mbeans

Dispatches calls to a java server process to collect JMX values for a device.
"""
import logging
import sys
import os
import socket
import Globals
import zope

from twisted.internet.defer import Deferred
from twisted.web import xmlrpc
from twisted.internet.protocol import ProcessProtocol
from twisted.internet import defer, reactor, error

from Products.ZenCollector.daemon import CollectorDaemon
from Products.ZenCollector.interfaces import ICollectorPreferences,\
                                             IDataService,\
                                             IEventService,\
                                             IScheduledTask
from Products.ZenCollector.tasks import SimpleTaskFactory,\
                                        SimpleTaskSplitter,\
                                        TaskStates
from Products.ZenEvents import Event
from Products.ZenHub.XmlRpcService import XmlRpcService
from Products.ZenUtils.NJobs import NJobs
from Products.ZenUtils.Utils import unused
from Products.ZenUtils.observable import ObservableMixin
import ZenPacks.zenoss.ZenJMX

from ZenPacks.zenoss.ZenJMX.services.ZenJMXConfigService import JMXDataSourceConfig

unused(JMXDataSourceConfig)

log = logging.getLogger( "zen.zenjmx" )
DEFAULT_HEARTBEAT_TIME = 5 * 60

WARNING_EVENT = dict(eventClass='/Status/JMX', component='JMX',
                     device=socket.getfqdn(), severity=Event.Warning)

class ZenJMXPreferences(object):
    """
    Configuration values for the zenjmx daemon.
    """
    zope.interface.implements(ICollectorPreferences)

    def __init__(self):
        """
        Construct a new ZenJMXPreferences instance and provide default
        values for needed attributes.
        """
        self.collectorName = "zenjmx"
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 5 * 60 # seconds
        self.configCycleInterval = 20 # minutes
        self.options = None

        # the configurationService attribute is the fully qualified class-name
        # of our configuration service that runs within ZenHub
        self.configurationService = 'ZenPacks.zenoss.ZenJMX.services.ZenJMXConfigService'

    def buildOptions(self, parser):
        parser.add_option('-j','--zenjmxjavaport',
                                dest='zenjmxjavaport',
                                default=9988,
                                type='int',
                                help='Port for zenjmxjava process; default 9988. '+\
                                'Tries 5 consecutive ports if there is a conflict',
                                )
        parser.add_option('--concurrentJMXCalls',
                               dest='concurrentJMXCalls',
                               action='store_true', default=False,
                               help='Enable concurrent calls to a JMX server'
                               )
        parser.add_option('--parallel', dest='parallel',
                               default=200, type='int',
                               help='Number of devices to collect from at one time'
                               )
        parser.add_option('--cycleInterval', dest='cycleInterval',
                               default=300, type='int',
                               help='Cycle time, in seconds, to run collection'
                               )
        parser.add_option('--portRange', dest='portRange',
                               default=5, type='int',
                               help='Number of ports to attempt when starting' +
                                    'Java jmx client')
        parser.add_option('--javaheap',
                            dest="maxHeap",type="int", default=512,
                            help="Max heap, in MB, to use for java process")
                               
    def postStartup(self):
        pass

    def getJavaClientArgs(self):
        args = None
        if self.options.configfile:
            args = ('--configfile', self.options.configfile)
        if self.options.logseverity:
            args = args + ('-v', str(self.options.logseverity))
        if self.options.concurrentJMXCalls:
            args = args + ('-concurrentJMXCalls', )
        return args

    def getStartingPort(self):
        return self.options.zenjmxjavaport

    def getAttemptedPortRange(self):
        return self.options.portRange


class IZenJMXJavaClient(zope.interface.Interface):

    listenPort = zope.interface.Attribute("listenPort")


class ZenJMXJavaClientImpl(ProcessProtocol):
    """
    Protocol to control the zenjmxjava process
    """
    zope.interface.implements(IZenJMXJavaClient)

    def __init__(
        self,
        args,
        cycle=True,
        zenjmxjavaport=9988,
        maxHeap=512
        ):
        """
        Initializer
        
        @param args: argument list for zenjmx
        @type args: list of strings
        @param cycle: whether to run once or repeat
        @type cycle: boolean
        @param zenjmxjavaport: port on which java process
                               will listen for queries
        @type zenjmxjavaport: int
        """
        self.deferred = Deferred()
        self.stopCalled = False
        self.process = None
        self.outReceived = sys.stdout.write
        self.errReceived = sys.stderr.write
        self.log = logging.getLogger('zen.ZenJMXJavaClient')
        self.args = args
        self.cycle = cycle
        self.listenPort = zenjmxjavaport
        self._maxHeap = maxHeap
        self.restartEnabled = False
        self._eventService = zope.component.queryUtility(IEventService)
        self._preferences = zope.component.queryUtility(ICollectorPreferences,
                                                      'zenjmx')

    def processEnded(self, reason):
        """
        Twisted reactor function called when the process ends.
        
        @param reason: message from the process
        @type reason: string
        """
        self.process = None
        if not self.stopCalled:
            procEndEvent = {
                'eventClass': '/Status/JMX',
                'summary': 'zenjmxjava ended unexpectedly: %s'\
                     % reason.getErrorMessage(),
                'severity': Event.Warning,
                'component': 'zenjmx',
                'device': self._preferences.options.monitor,
                }
            self._eventService.sendEvent(procEndEvent)
            self.log.warn('processEnded():zenjmxjava process ended %s'
                           % reason)
            if self.deferred:
                msg = reason.getErrorMessage()
                exitCode = reason.value.exitCode
                if exitCode == 10:
                    msg = 'Could not start up Java web server, '+\
                        'possible port conflict'
                self.deferred.callback((exitCode,msg))
                self.deferred = None
            elif self.restartEnabled:
                self.log.info('processEnded():restarting zenjmxjava')
                reactor.callLater(1, self.run)

    def stop(self):
        """
        Twisted reactor function called when we are shutting down.
        """
        import signal
        self.log.info('stop():stopping zenjmxjava')
        self.stopCalled = True
        if not self.process:
            self.log.debug('stop():no zenjmxjava process to stop')
            return
        try:
            self.process.signalProcess(signal.SIGKILL)
        except error.ProcessExitedAlready:
            self.log.info('stop():zenjmxjava process already exited')
            pass
        try:
            self.process.loseConnection()
        except Exception:
            pass
        self.process = None

    def connectionMade(self):
        """
        Called when the Twisted reactor starts up
        """
        self.log.debug('connectionMade():zenjmxjava started')

        def doCallback():
            """
            doCallback
            """
            msg = \
                'doCallback(): callback on deferred zenjmxjava proc is up'
            self.log.debug(msg)
            if self.deferred:
                self.deferred.callback((True,'zenjmx java started'))
            if self.process:
                procStartEvent = {
                    'eventClass': '/Status/JMX',
                    'summary': 'zenjmxjava started',
                    'severity': Event.Clear,
                    'component': 'zenjmx',
                    'device': self._preferences.options.monitor,
                    }
                self._eventService.sendEvent(procStartEvent)
            self.deferred = None

        if self.deferred:
            self.log.debug('connectionMade():scheduling callback')

            # give the java service a chance to startup
            reactor.callLater(3, doCallback)
        self.log.debug('connectionMade(): done')


    def run(self):
        """
        Twisted function called when started
        """
        if self.stopCalled:
            return
        self.log.info('run():starting zenjmxjava')
        zenjmxjavacmd = os.path.join(ZenPacks.zenoss.ZenJMX.binDir,
                'zenjmxjava')
        if self.cycle:
            args = ('runjmxenabled', )
        else:
            # don't want to start up with jmx server to avoid port conflicts
            args = ('run', )
            
        args = args + ('-zenjmxjavaport',
                       str(self.listenPort))
        if self.args:
            args = args + self.args
        cmd = (zenjmxjavacmd, ) + args
        self.log.debug('run():spawn process %s' % (cmd, ))
        self.deferred = Deferred()
        env = dict(os.environ)
        env['JVM_MAX_HEAP'] = '-Xmx%sm'%self._maxHeap
        self.process = reactor.spawnProcess(self, zenjmxjavacmd, cmd,
                env=env)
        return self.deferred


DEFAULT_JMX_JAVA_CLIENT_NAME = 'zenjmxjavaclient'

class ZenJMXJavaClientInitialization(object):
    """
    Wrapper that continues to start the Java jmx client until
    successful.
    """

    def __init__(self,
                 registeredName=DEFAULT_JMX_JAVA_CLIENT_NAME):
        """
        @param registeredName: the name with which this client
                               will be registered as a utility

        """
        self._jmxClient = None
        self._clientName = registeredName

    def initialize(self):
        """
        Begin the first attempt to start the Java jmx client.  Note that
        this method returns a Deferred that relies on the ZenJMXPreferences
        being present when it is finally executed.  This is meant to be
        the Deferred that is given to the CollectorDaemon for
        initialization before the first JMX task is scheduled.

        @return the deferred that represents the loading of preferences
                and the initial attempt to start the Java jmx client
        @rtype defer.Deferred
        """
        def loadPrefs():
            log.debug( "Retrieving java client startup args")
            preferences = zope.component.queryUtility(ICollectorPreferences,
                                                 'zenjmx')
            self._args = preferences.getJavaClientArgs()
            self._cycle = preferences.options.cycle
            self._maxHeap = preferences.options.maxHeap
            self._startingPort = preferences.getStartingPort()
            self._rpcPort = self._startingPort
            self._attemptedPortRange = preferences.getAttemptedPortRange()

        def printProblem(result):
            log.error( str(result) )
            sys.exit(1)

        d = defer.maybeDeferred( loadPrefs )
        d.addCallback( self._startJavaProc )
        d.addErrback( printProblem )
        return d

    def _tryClientOnCurrentPort( self ):
        """
        Returns the Deferred for executing an attempt
        to start the java jmx client on the current port.
        """
        log.debug( 'Attempting java client startup on port %s',
                    self._rpcPort )
        self._jmxClient = ZenJMXJavaClientImpl( self._args, self._cycle, self._rpcPort, self._maxHeap )
        zope.component.provideUtility(
                              self._jmxClient,
                              IZenJMXJavaClient,
                              self._clientName
                              )
        return self._jmxClient.run()

    def _startJavaProc( self, result=None ):
        """
        Checks whether startup of the java jmx client was successful.  If
        it was unsuccessful due to port conflict, increments the port and
        tries to start the client again.
        """
        # If the result is not None, that means this was called as a callback
        # after an attempt to start the client
        if result is not None:
            # If result[0] is True, the client process started
            if result[0] is True:
                log.debug( 'Java jmx client started' )
                self._jmxClient.restartEnabled = True
                deferred = defer.succeed( True )
            # If the result[0] is 10, there was a port conflict
            elif result[0] == 10:
                log.debug( 'Java client didn\'t start; port %s occupied',
                           self._rpcPort )
                if self._rpcPort < ( self._startingPort +
                                     self._attemptedPortRange ):
                    self._rpcPort += 1
                    deferred = self._tryClientOnCurrentPort()
                    deferred.addCallback( self._startJavaProc )
                else:
                    raise RuntimeError(
                        "ZenJMXJavaClient could not be started, check ports")
            else:
                #unknown error
                raise RuntimeError('ZenJMXJavaClient could not be started, '+\
                                   'check JVM type and version: %s' % result[1])
        # If there was no result passed in, then this is the first attempt
        # to start the client
        else:
            deferred = self._tryClientOnCurrentPort()
            deferred.addCallback( self._startJavaProc )

        return deferred


class ZenJMXTask(ObservableMixin):
    """
    The scheduled task for all the jmx datasources on an individual device.
    """
    zope.interface.implements(IScheduledTask)

    def __init__(self,
                 deviceId,
                 taskName,
                 scheduleIntervalSeconds,
                 taskConfig,
                 clientName=DEFAULT_JMX_JAVA_CLIENT_NAME ):

        super( ZenJMXTask, self ).__init__()
        self.name = taskName
        self.configId = deviceId
        self.state = TaskStates.STATE_IDLE
        
        self._taskConfig = taskConfig
        self._manageIp = self._taskConfig.manageIp

        self._dataService = zope.component.queryUtility( IDataService )
        self._eventService = zope.component.queryUtility( IEventService )
        self._preferences = zope.component.queryUtility( ICollectorPreferences,
                                                         'zenjmx' )
        self._client = zope.component.queryUtility( IZenJMXJavaClient,
                                                    clientName )

        # At this time, do not use the interval passed from the device
        # configuration.  Use the value pulled from the daemon
        # configuration.
        unused( scheduleIntervalSeconds )
        self.interval = self._preferences.options.cycleInterval
        
    def createEvent(self, errorMap, component=None):
        """
        Given an event dictionary, copy it and return the event

        @param errorMap: errorMap
        @type errorMap: s dictionarytring
        @param component: component name
        @type component: string
        @return: updated event
        @rtype: dictionary
        """
        event = errorMap.copy()
        if component:
            event['component'] = component
        if event.get('datasourceId') and not event.get('eventKey'):
            event['eventKey'] = event.get('datasourceId')
        return event

    def sendEvent(self, event, **kw):
        self._eventService.sendEvent(event, **kw)

    def _collectJMX(self, dsConfigList):
        """
        Call Java JMX process to collect JMX values

        @param dsConfigList: DataSource configuration
        @type dsConfigList: list of JMXDataSourceConfig
        @return: Twisted deferred object
        @rtype: Twisted deferred object
        """
        def toDict(config):
            """
            Marshall the fields from the datasource into a dictionary and
            ignore everything that is not a primitive

            @param config: dictionary of results
            @type config: string
            @return: results from remote device
            @rtype: dictionary
            """
            vals = {}
            for (key, val) in config.__dict__.items():
                if key != 'rrdConfig' and type(val)\
                     in XmlRpcService.PRIMITIVES:
                    vals[key] = val

            rrdConfigs = config.rrdConfig.values()
            rrdConfigs.sort(lambda x, y: cmp(x.dataPointId,
                            y.dataPointId))

            vals['dps'] = []
            vals['dptypes'] = []
            for rrdConfig in rrdConfigs:
                vals['dps'].append(rrdConfig.dataPointId)
                vals['dptypes'].append(rrdConfig.rrdType)

            vals['connectionKey'] = config.getConnectionPropsKey()
            return vals

        def rpcCall():
            """
            Communicate with our local JMX process to collect results.
            This is a generator function

            @param driver: generator
            @type driver: string
            """
            port = self._client.listenPort
            xmlRpcProxy = xmlrpc.Proxy('http://localhost:%s/' % port)
            d = xmlRpcProxy.callRemote('zenjmx.collect', configMaps)
            d.addCallbacks( processResults , processRpcError)
            return d

        def processRpcError(error):
            log.debug("Could not make XML RPC call for device %s; content of call: %s", self._taskConfig, configMaps)
            self.sendEvent({}, severity=Event.Error,
                                eventClass='/Status/JMX',
                                summary='unexpected error: %s' % error.getErrorMessage(),
                                eventKey='unexpected_xmlrpc_error',
                                device=self.configId)
            return error


        def processResults(jmxResults):
            """
            Given the results from JMX, store them or send events.

            @param jmxResults: jmxResults
            @type jmxResults: string
            """

            #Send clear for RPC error
            self.sendEvent({}, severity=Event.Clear,
                                eventClass='/Status/JMX',
                                summary='unexpected error cleared',
                                eventKey='unexpected_xmlrpc_error',
                                device=self.configId)

            result = {}
            hasConnectionError = False
            hasUnexpectedError = False
            for result in jmxResults:
                log.debug("JMX result -> %s", result)
                evtSummary = result.get('summary')
                deviceId = result.get('device')
                evt = self.createEvent(result)
                if not evtSummary:
                    rrdPath = result.get('rrdPath')
                    dsId = result.get('datasourceId')
                    dpId = result.get('dpId')
                    value = result.get('value')
                    try:
                        self.storeRRD(deviceId, rrdPath, dsId, dpId, value)
                    except ValueError:
                        pass
                    self.sendEvent(evt,summary="Clear",severity=Event.Clear)
                else:
                    # send event
                    log.debug('processResults(): '
                                    + 'jmx error, sending event for %s'
                                    % result)
                    if evt.get("eventClass", "") == '/Status/JMX/Connection':
                        hasConnectionError = True
                    if evt.get("eventKey", "") == 'unexpected_error':
                        hasUnexpectedError = True

                    self.sendEvent(evt, severity=Event.Error)

            if not hasConnectionError:
                self.sendEvent({}, severity=Event.Clear,
                    eventClass='/Status/JMX/Connection',
                    summary='Connection is up',
                    eventKey=connectionComponentKey,
                    device=self.configId)
            if not hasUnexpectedError:
                self.sendEvent({}, severity=Event.Clear,
                    eventClass='/Status/JMX',
                    summary='Unexpected error cleared',
                    eventKey='unexpected_error',
                    device=self.configId)



            return jmxResults

        connectionComponentKey = ''
        configMaps = []
        for config in dsConfigList:
            connectionComponentKey = config.getConnectionPropsKey()
            configMaps.append(toDict(config))
        log.info('collectJMX(): for %s %s' % (config.device,
                      connectionComponentKey))
        return rpcCall()

    def storeRRD(
        self,
        deviceId,
        rrdPath,
        dataSourceId,
        dataPointId,
        dpValue,
        ):
        """
        Store a value into an RRD file

        @param deviceId: name of the remote device
        @type deviceId: string
        @param dataSourceId: name of the data source
        @type dataSourceId: string
        @param dataPointId: name of the data point
        @type dataPointId: string
        @param dpValue: dpValue
        @type dpValue: number
        """
        deviceConfig = self._taskConfig
        dsConfig = deviceConfig.findDataSource(dataSourceId)
        if not dsConfig:
            log.info(
                  'No data source config found for device %s datasource %s' \
                  % (deviceId, dataSourceId))
            return
        rrdConf = dsConfig.rrdConfig.get(dataPointId)
        type = rrdConf.rrdType
        if(type in ('COUNTER', 'DERIVE')):
            try:
                # cast to float first because long('100.0') will fail with a
                # ValueError
                dpValue = long(float(dpValue))
            except (TypeError, ValueError):
                log.warning("value %s not valid for derive or counter data points", dpValue)
        else:
            try:
                dpValue = float(dpValue)
            except (TypeError, ValueError):
                log.warning("value %s not valid for data point", dpValue)

        if not rrdConf:
            log.info(
                'No RRD config found for device %s datasource %s datapoint %s' \
                % (deviceId, dataSourceId, dataPointId))
            return

        dpPath = '/'.join((rrdPath, rrdConf.dpName))
        min = rrdConf.min 
        max = rrdConf.max
        self._dataService.writeRRD(dpPath, dpValue, rrdConf.rrdType,
                              rrdConf.command, min=min, max=max)

    def _finished(self, results):
        for result in results:
            log.debug("Finished with result %s" % str( result ) )
        return results

    def doTask(self):
        log.debug("Scanning device %s [%s]", self.configId, self._manageIp)
        
        d = self._collectCallback()
        d.addBoth(self._finished)

        # returning a Deferred will keep the framework from assuming the task
        # is done until the Deferred actually completes
        return d

    def _collectCallback(self):

        jobs = NJobs(self._preferences.options.parallel,
                     self._collectJMX,
                     self._taskConfig.jmxDataSourceConfigs.values())
        deferred = jobs.start()
        return deferred

    def cleanup(self):
        pass

def stopJavaJmxClients():
    # Currently only starting/stopping one.
    clientName = DEFAULT_JMX_JAVA_CLIENT_NAME
    client = zope.component.queryUtility( IZenJMXJavaClient,
                                          clientName )
    if client is not None:
        log.debug( 'Shutting down JMX Java client %s' % clientName )
        client.stop()

if __name__ == '__main__':
    myPreferences = ZenJMXPreferences()
    initialization = ZenJMXJavaClientInitialization()
    myTaskFactory = SimpleTaskFactory(ZenJMXTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)

    daemon = CollectorDaemon(myPreferences, myTaskSplitter,
                        initializationCallback=initialization.initialize,
                        stoppingCallback=stopJavaJmxClients)
    daemon.run()
