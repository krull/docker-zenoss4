
import xml.dom.minidom as minidom

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.MySqlMonitor.utils import here


class TestObjectsXML(BaseTestCase):
    def test_parses(self):
        self.assertTrue(minidom.parse(here('objects/objects.xml')))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestObjectsXML))
    return suite
