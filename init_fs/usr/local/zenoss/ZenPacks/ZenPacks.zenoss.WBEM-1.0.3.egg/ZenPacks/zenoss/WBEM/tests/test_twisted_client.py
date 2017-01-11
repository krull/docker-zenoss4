##############################################################################
#
# Copyright (C) Zenoss, Inc. 2015, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from mock import Mock, sentinel

from xml.etree.ElementTree import fromstring, tostring

from Products.ZenTestCase.BaseTestCase import BaseTestCase

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath
addLocalLibPath()

from pywbem.twisted_client import EnumerateInstances
from pywbem.cim_obj import CIMInstance

class TestParseResponse(BaseTestCase):
    def test_parses(self):
        xml = fromstring('''<xml>
<VALUE.NAMEDINSTANCE>
<INSTANCENAME CLASSNAME="Clar_DiskDrive">
<KEYBINDING NAME="CreationClassName"><KEYVALUE TYPE="string" VALUETYPE="string">Clar_DiskDrive</KEYVALUE></KEYBINDING>
<KEYBINDING NAME="DeviceID"><KEYVALUE TYPE="string" VALUETYPE="string">CLARiiON+0_0_0</KEYVALUE></KEYBINDING>
<KEYBINDING NAME="SystemCreationClassName"><KEYVALUE TYPE="string" VALUETYPE="string">Clar_StorageSystem</KEYVALUE></KEYBINDING>
<KEYBINDING NAME="SystemName"><KEYVALUE TYPE="string" VALUETYPE="string">CLARiiON+APM00141704021</KEYVALUE></KEYBINDING>
</INSTANCENAME>
<INSTANCE CLASSNAME="Clar_DiskDrive">
<PROPERTY NAME="CreationClassName" TYPE="string"><VALUE>Clar_DiskDrive</VALUE>
</PROPERTY>
<PROPERTY NAME="DeviceID" TYPE="string"><VALUE>CLARiiON+0_0_0</VALUE>
</PROPERTY>
<PROPERTY.ARRAY NAME="OperationalStatus" TYPE="uint16"><VALUE.ARRAY>
<VALUE>2</VALUE>
</VALUE.ARRAY>
</PROPERTY.ARRAY>
<PROPERTY NAME="OtherInterconnectType" TYPE="string"><VALUE />
</PROPERTY>
<PROPERTY NAME="RequestedState" TYPE="uint16"><VALUE>12</VALUE>
</PROPERTY>
<PROPERTY NAME="RPM" TYPE="uint32"><VALUE>4294967295</VALUE>
</PROPERTY>
<PROPERTY.ARRAY NAME="StatusDescriptions" TYPE="string"><VALUE.ARRAY>
<VALUE>OK</VALUE>
</VALUE.ARRAY>
</PROPERTY.ARRAY>
<PROPERTY NAME="TransitioningToState" TYPE="uint16"><VALUE>12</VALUE>
</PROPERTY>
</INSTANCE>
</VALUE.NAMEDINSTANCE>
        </xml>''')
        res = EnumerateInstances.parseResponse(xml)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].classname, 'Clar_DiskDrive')
        self.assertEqual(len(res[0].properties), 8)

        self.assertEqual(res[0].properties['OtherInterconnectType'].value, '')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestParseResponse))
    return suite

