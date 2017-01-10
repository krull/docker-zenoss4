##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
import logging
from .data import modeling_data
from mock import MagicMock, patch
from MySQLdb import cursors

from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from Products.ZenCollector.services.config import DeviceProxy

from ZenPacks.zenoss.MySqlMonitor.modeler.plugins.MySQLCollector \
    import MySQLCollector


def patch_asUnitTest(self):
    """
    Patch asUnitTest method of ObjectMap so that it does not
    raise key errors of 'classname' and 'compname'.
    """
    map = {}
    map.update(self.__dict__)
    del map["_attrs"]
    try:
        del map["modname"]
        del map["compname"]
        del map["classname"]
    except:
        pass
    return map


class TestMySQLCollector(BaseTestCase):

    def afterSetUp(self):
        self.device = DeviceProxy()
        self.device.id = "test"
        self.device.manageIp = "127.0.0.1"
        self.logger = logging.getLogger('.'.join(['zen', __name__]))
        ObjectMap.asUnitTest = patch_asUnitTest
        self.collector = MySQLCollector()
        self.collector._eventService = MagicMock()
        self.collector.queries = {'test': 'test'}

    def test_process_data(self):
        results = modeling_data.RESULT1
        server_map, db_map = self.collector.\
            process(self.device, results, self.logger)

        self.assertEquals({
            'data_size': 53423729,
            'id': 'root_3306',
            'index_size': 4143104,
            'master_status': 'OFF',
            'percent_full_table_scans': '71.2%',
            'size': 57566833,
            'slave_status': 'IO running: No; SQL running: '
                            'No; Seconds behind: None',
            'version': '5.5.28 MySQL Community Server (GPL) (i686)',
            'title': 'root_3306'}, server_map.maps[0].asUnitTest())

        self.assertEquals({
            'data_size': 0,
            'default_character_set_name': 'utf8',
            'default_collation_name': 'utf8_general_ci',
            'id': 'root_3306(.)information_schema',
            'index_size': 9216,
            'size': 9216,
            'table_count': 40L,
            'title': 'information_schema'}, db_map.maps[0].asUnitTest())

    @patch('ZenPacks.zenoss.MySqlMonitor.modeler.'
           'plugins.MySQLCollector.adbapi')
    def test_collect(self, mock_adbapi):
        self.device.zMySQLConnectionString = ['{"user":"root",'
                                              '"passwd":"zenoss",'
                                              '"port":"3306"}']
        self.collector.collect(self.device, self.logger)
        mock_adbapi.ConnectionPool.assert_called_with(
            'MySQLdb',
            passwd='zenoss',
            port=3306,
            host='127.0.0.1',
            user='root',
            cursorclass=cursors.DictCursor
        )

    def test_table_scans(self):
        self.assertEquals(
            self.collector._table_scans(modeling_data.SERVER_STATUS1),
            '71.2%'
        )
        self.assertEquals(
            self.collector._table_scans(modeling_data.SERVER_STATUS2),
            'N/A'
        )

    def test_master_status(self):
        self.assertEquals(
            self.collector._master_status(modeling_data.MASTER_STATUS1),
            "ON; File: mysql-bin.000002; Position: 107"
        )
        self.assertEquals(
            self.collector._master_status(modeling_data.MASTER_STATUS2),
            "OFF"
        )

    def test_slave_status(self):
        self.assertEquals(
            self.collector._slave_status(modeling_data.SLAVE_STATUS1),
            "IO running: No; SQL running: No; Seconds behind: 10"
        )
        self.assertEquals(
            self.collector._slave_status(modeling_data.SLAVE_STATUS2),
            "OFF"
        )

    def test_version(self):
        self.assertEquals(
            self.collector._version(modeling_data.VERSION1),
            '5.5.28 MySQL Community Server (GPL) (i686)'
        )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMySQLCollector))
    return suite
