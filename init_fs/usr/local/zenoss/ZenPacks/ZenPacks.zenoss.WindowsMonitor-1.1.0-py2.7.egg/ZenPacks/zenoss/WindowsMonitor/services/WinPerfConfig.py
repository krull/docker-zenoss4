##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''WinPerfConfig

ZenHub service for handling zenwinperf configuration
'''

from Products.ZenCollector.services.config import CollectorConfigService

from ZenPacks.zenoss.WindowsMonitor.datasources.WinPerfDataSource \
                                        import WinPerfDataSource

WINPERF_DSTYPE = WinPerfDataSource.WINPERF_DSTYPE


import logging
log = logging.getLogger("zenhub")


class WinPerfConfig(CollectorConfigService):
    def __init__(self, dmd, instance):
        deviceProxyAttributes = ('zWmiMonitorIgnore',
                                 'zWinUser',
                                 'zWinPassword')
        CollectorConfigService.__init__(self, dmd, instance, deviceProxyAttributes)

    def _filterDevice(self, device):
        include = CollectorConfigService._filterDevice(self, device)

        # WMI ~= PerfMon, but eh
        if getattr(device, 'zWmiMonitorIgnore', False):
            self.log.debug("Device %s skipped because zWmiMonitorIgnore is on",
                           device.id)
            include = False

        # No credentials: we'll never login anyhow
        elif not device.zWinUser:
            self.log.debug("Device %s skipped because zWinUser is not set",
                           device.id)
            include = False

        return include

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)

        proxy.configCycleInterval = max(device.getProperty('zWinPerfCycleSeconds', 1), 1)
        proxy.cyclesPerConnection = max(device.getProperty('zWinPerfCyclesPerConnection', 2), 2)
        proxy.timeoutSeconds = max(device.getProperty('zWinPerfTimeoutSeconds', 1), 1)


        proxy.dpInfo = []
        proxy.thresholds = []

        perfServer = device.getPerformanceServer()

        # get the datapoints & thresholds first for the device itself
        self._getDataPointInfo(proxy, device, device.id, None, perfServer)
        proxy.thresholds += device.getThresholdInstances(WINPERF_DSTYPE)

        # and then for all of the monitored components that have them
        for comp in device.getMonitoredComponents():
            self._getDataPointInfo(proxy, comp, comp.device().id, comp.id,
                                   perfServer)
            proxy.thresholds += comp.getThresholdInstances(WINPERF_DSTYPE)

        # if there are no datapoints to be monitored then we don't need a
        # proxy to monitor this device
        if not proxy.dpInfo:
            self.log.debug("Device %s has no datapoints to be monitored",
                           device.id)
            return None

        return proxy

    # Loop through the device and all monitored components,
    # accumulating information on all applicable datapoints
    # and thresholds
    def _getDataPointInfo(self, proxy, devOrComp, devId, compId, perfServer):
        if compId:
            perfmonInstance = getattr(devOrComp, 'perfmonInstance', None)
            if not perfmonInstance:
                self.log.debug('Cannot collect data via PerfMon for '
                                '%s on %s because it has not been ' %
                                (compId, devId) +
                                'modeled with the WinPlugins modeler '
                                'plugins.')
                return
        else:
            perfmonInstance = ''

        for template in devOrComp.getRRDTemplates():
            dataSources = [ds for ds
                            in template.getRRDDataSources(WINPERF_DSTYPE)
                            if ds.enabled]
            for ds in dataSources:
                for dp in ds.datapoints():
                    # zenwinperf uses == to compare lists of dpInfo
                    # so if something ends up in dpInfo that doesn't
                    # play nice with a == comparison that part
                    # of zenwinperf (Connection.updateConfig) will need
                    # some rejiggering
                    counter = dp.counter
                    if not counter:
                        continue
                    if not counter.startswith('\\'):
                        counter = '\\%s' % counter

                    proxy.dpInfo.append(dict(
                        devId=devId,
                        compId=compId,
                        dsId=ds.id,
                        dpId=dp.id,
                        counter=perfmonInstance + counter,
                        path='/'.join((devOrComp.rrdPath(), dp.name())),
                        rrdType=dp.rrdtype,
                        rrdCmd=dp.getRRDCreateCommand(perfServer),
                        minv=dp.rrdmin,
                        maxv=dp.rrdmax
                        ))
