##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.zenoss.ZenJMX.datasources.JMXDataSource import JMXDataSource


class TestJMXDataSource(BaseTestCase):

    def afterSetUp(self):
        self.ds = JMXDataSource(id='1')

    def test_getDescription(self):
        self.assertEqual(self.ds.getDescription(), '${dev/id}')

    def test_getProtocols(self):
        self.assertEqual(self.ds.getProtocols(), ['REMOTING-JMX', 'RMI', 'JMXMP'])

    def test_zmanage_editProperties(self):
        with self.assertRaises(AttributeError):
            self.ds.zmanage_editProperties()
