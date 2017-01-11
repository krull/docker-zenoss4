##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import logging
import md5

import Globals
from Products.ZenUtils.ZenTales import talesEval
from Products.ZenEvents.ZenEventClasses import Error, Clear
from Products.ZenCollector.services.config import CollectorConfigService

from ZenPacks.zenoss.ZenJMX.datasources.JMXDataSource import JMXDataSource

from twisted.spread import pb

log = logging.getLogger( "zen.zenjmxconfigservices" )


class RRDConfig(pb.Copyable, pb.RemoteCopy):
    """
    RRD configuration for a datapoint.
    Contains the create command and the min and max
    values for a datapoint
    """
    def __init__(self, dp):
        self.dpName = dp.name()
        self.command = dp.createCmd
        self.dataPointId = dp.id
        self.min = dp.rrdmin
        self.max = dp.rrdmax
        self.rrdType = dp.rrdtype

pb.setUnjellyableForClass(RRDConfig, RRDConfig)


class JMXDeviceConfig(pb.Copyable, pb.RemoteCopy):
    """
    Represents the configuration for a device.
    Contains a list of JMXDataSourceConfig objects
    """

    def __init__(self, device):
        self.id = device.id
        self.configId = device.id
        #map of jmxserverkey to JMXDataSourceConfig list
        self.jmxDataSourceConfigs = {}
        self.manageIp = device.manageIp
        self.thresholds = []

        # Default interval is 5 minutes.
        # This may be replaced with per datasource
        # intervals at some point.  For now, this
        # will be ignored at the collector.
        self.configCycleInterval = 5 * 60

    def findDataSource(self, dataSourceId):
        for subList in self.jmxDataSourceConfigs.values():
            for dsConfig in subList:
                if(dsConfig.datasourceId == dataSourceId):
                    return dsConfig
        return None

    def add(self, jmxDataSourceConfig):
        """
        add a JMXDataSourceConfig to the device configuration
        """
        key = jmxDataSourceConfig.getJMXServerKey()
        configs = self.jmxDataSourceConfigs.get(key)
        if(not configs):
            configs = []
            self.jmxDataSourceConfigs[key] = configs
        configs.append(jmxDataSourceConfig)

pb.setUnjellyableForClass(JMXDeviceConfig, JMXDeviceConfig)


class JMXDataSourceConfig(pb.Copyable, pb.RemoteCopy):
    """
    Represents a JMX datasource configuration on a device.
    """

    def __init__(self, device, component, template, datasource):
        self.device = device.id
        self.manageIp = device.manageIp
        self.datasourceId = datasource.id
        if not component:
            self.component = datasource.getComponent(device)
            self.rrdPath = device.rrdPath()
            self.copyProperties(device, datasource)
        else:
            self.component = datasource.getComponent(component)
            self.rrdPath = component.rrdPath()
            self.copyProperties(component, datasource)

        #dictionary of datapoint name to RRDConfig
        self.rrdConfig = {}
        for dp in datasource.datapoints():
            self.rrdConfig[dp.id] = RRDConfig(dp)


    def copyProperties(self, device, ds):
        """
        copy the properties from the datasouce and set them
        as attributes
        """
        for propName in [prop['id'] for prop in ds._properties]:
            value = getattr(ds, propName)
            if str(value).find('$') >= 0:
                value = talesEval('string:%s' % (value,), device)
            if propName == 'authenticate':
                if value:
                    value = str(value).lower().capitalize()
                value = bool(value)
            setattr(self, propName, value)


    def key(self):
        return self.device, self.datasourceId

    def getJMXServerKey(self):
        """
        string which represents the jmx server  and connection props.
        Can be compared to determine if datasources configurations point to the
        same jmx server
        """
        return self.device + self.manageIp + self.getConnectionPropsKey()

    def getConnectionPropsKey(self):
        """
        string key which represents the connection properties that make up
        the connection properties for the datasource.
        """
        # raw service URL is being used
        if self.jmxRawService:
            return self.jmxRawService

        components = [self.jmxProtocol]
        if self.jmxProtocol in ["RMI", "REMOTING-JMX"]:
            components.append(self.rmiContext)
        components.append(str(self.jmxPort))
        if (self.authenticate):
            creds = self.username + self.password
            components.append( md5.new(creds).hexdigest() );

        return ":".join(components)

    def update(self, value):
        self.__dict__.update(value.__dict__)

pb.setUnjellyableForClass(JMXDataSourceConfig, JMXDataSourceConfig)


class ZenJMXConfigService(CollectorConfigService):
    """ZenHub service for getting ZenJMX configurations
       from the object database"""
    def __init__(self, dmd, instance):
        attributes = ()
        CollectorConfigService.__init__(self,
                                        dmd,
                                        instance,
                                        attributes)
        self._ds_errors = {}

    def _get_ds_conf(self, device, component, template, ds):
        component_id = None if (component is None) else component.id
        ds_error_key = (device.id, component_id, template.id, ds.id)
        ds_conf = None

        try:
            ds_conf = JMXDataSourceConfig(device, component, template, ds)
            evt = self._ds_errors.pop(ds_error_key, None)
            if evt is not None:
                evt["severity"] = Clear
                self.sendEvent(evt)

        except Exception, e:
            fmt = "Evaluation of data source '{0.id}' in template '{1.id}' failed: {2.__class__.__name__}: {2}"
            summary = fmt.format(ds, template, e)
            evt = dict(severity=Error,
                       device=device.id,
                       eventClass="/Status/JMX",
                       summary=summary)
            msg = summary + " device={0.id}".format(device)
            evt["component"] = component_id
            msg += ", component={0}".format(component_id)
            self.sendEvent(evt)
            self._ds_errors[ds_error_key] = evt
            self.log.error(msg)

        return ds_conf

    def _createDeviceProxy(self, device):
        deviceConfig = JMXDeviceConfig(device)
        deviceConfig.thresholds += device.getThresholdInstances(
            JMXDataSource.sourcetype)

        for template in device.getRRDTemplates():
            for ds in self._getDataSourcesFromTemplate(template):
                ds_conf = self._get_ds_conf(device, None, template, ds)
                if ds_conf is not None:
                    deviceConfig.add(ds_conf)

        for component in device.getMonitoredComponents():
            deviceConfig.thresholds += component.getThresholdInstances(
                JMXDataSource.sourcetype)

            for template in component.getRRDTemplates():
                for ds in self._getDataSourcesFromTemplate(template):
                    ds_conf = JMXDataSourceConfig(device, component, template, ds)
                    if ds_conf is not None:
                        deviceConfig.add(ds_conf)

        # Don't both returning a proxy if there are no datasources.
        if not len(deviceConfig.jmxDataSourceConfigs.keys()):
            return None

        return deviceConfig

    def _getDataSourcesFromTemplate(self, template):
        datasources = []
        for ds in template.getRRDDataSources('JMX'):
            if not ds.enabled: continue
            datasources.append(ds)

        return datasources


if __name__ == '__main__':
    from Products.ZenHub.ServiceTester import ServiceTester
    tester = ServiceTester(ZenJMXConfigService)
    def printer(proxy):
        print '\t'.join( ['', 'Hostname', 'Service name', 'Port'] )
        for component, config in proxy.jmxDataSourceConfigs.items():
            print '\t', component
    tester.printDeviceProxy = printer
    tester.showDeviceInfo()

