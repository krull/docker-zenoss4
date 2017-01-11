##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from mock import Mock, patch
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.ZenJMX.services.ZenJMXConfigService import (
    JMXDeviceConfig,
    JMXDataSourceConfig,
    ZenJMXConfigService
)

ds = Mock(
    id='1',
    getComponent=Mock(return_value=Mock()),
    _properties=[{'id': 'id'}],
    datapoints=Mock(return_value=[Mock()])
)

class TestJMXDeviceConfig(BaseTestCase):
    def afterSetUp(self):
        self.config = JMXDeviceConfig(Mock())

    def test_findDataSource(self):
        self.assertEqual(self.config.findDataSource(None), None)

    def test_add(self):
        jmxDataSourceConfig = Mock(
            getJMXServerKey=Mock(return_value='key')
        )
        self.config.add(jmxDataSourceConfig)
        self.assertEqual(len(self.config.jmxDataSourceConfigs), 1)


class TestJMXDataSourceConfig(BaseTestCase):
    def afterSetUp(self):
        self.ds = ds
        self.config = JMXDataSourceConfig(
            device=Mock(),
            component=None,
            template=Mock(),
            datasource=self.ds
        )

    def test_getConnectionPropsKey(self):
        self.config.authenticate = False
        self.config.jmxRawService = False
        self.config.jmxPort = 'jmxPort'
        self.config.jmxProtocol = 'RMI'
        self.config.rmiContext = 'rmiContext'
        self.assertEquals(self.config.getConnectionPropsKey(),
                          'RMI:rmiContext:jmxPort')

        self.config.authenticate = True
        self.config.username = 'username'
        self.config.password = 'password'
        self.assertEquals(self.config.getConnectionPropsKey(),
                          'RMI:rmiContext:jmxPort:d51c9a7e9353746a6020f9602d452929')

        self.config.jmxRawService = True
        self.assertTrue(self.config.getConnectionPropsKey())


class TestZenJMXConfigService(BaseTestCase):
    def afterSetUp(self):
        self.ds = ds
        self.config = ZenJMXConfigService(
            dmd=Mock(),
            instance=Mock()
        )

    def test_get_ds_conf(self):
        ds_conf = self.config._get_ds_conf(
                device=Mock(),
                component=None,
                template=Mock(),
                ds=self.ds)
        self.assertIsNotNone(ds_conf)

    def test_createDeviceProxy(self):
        device = Mock()
        device.getRRDTemplates.return_value = []
        device.getThresholdInstances.return_value = []
        device.getMonitoredComponents.return_value = []
        self.assertEquals(self.config._createDeviceProxy(device), None)

    def test_getDataSourcesFromTemplate(self):
        ds = Mock(enabled=True)
        template = Mock()
        template.getRRDDataSources.return_value=[ds]
        self.assertEquals(self.config._getDataSourcesFromTemplate(template), [ds])
