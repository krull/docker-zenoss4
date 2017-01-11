##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################
"""
Custom ZenPack initialization code. All code defined in this module will be
executed at startup time in all Zope clients.
"""
import math
import logging
log = logging.getLogger('zen.MySqlMonitor')

import Globals

from Products.ZenEvents.EventManagerBase import EventManagerBase
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenUtils.Utils import unused
from Products.Zuul.interfaces import ICatalogTool

#from ZenPacks.zenoss.PythonCollector import patches

unused(Globals)


# Modules containing model classes. Used by zenchkschema to validate
# bidirectional integrity of defined relationships.
productNames = (
    'MySQLServer',
    'MySQLDatabase'
    )

# Useful to avoid making literal string references to module and class names
# throughout the rest of the ZenPack.
ZP_NAME = 'ZenPacks.zenoss.MySqlMonitor'
MODULE_NAME = {}
CLASS_NAME = {}
for product_name in productNames:
    MODULE_NAME[product_name] = '.'.join([ZP_NAME, product_name])
    CLASS_NAME[product_name] = '.'.join([ZP_NAME, product_name, product_name])

# Useful for components' ids.
NAME_SPLITTER = '(.)'

# Define new device relations.
NEW_DEVICE_RELATIONS = (
    ('mysql_servers', 'MySQLServer'),
    )

NEW_COMPONENT_TYPES = (
    'ZenPacks.zenoss.MySqlMonitor.MySQLServer.MySQLServer',
    )

# Add new relationships to Device if they don't already exist.
for relname, modname in NEW_DEVICE_RELATIONS:
    if relname not in (x[0] for x in Device._relations):
        Device._relations += (
            (relname,
             ToManyCont(ToOne, '.'.join((ZP_NAME, modname)), 'mysql_host')),
        )


# Add ErrorNotification to Device
def setErrorNotification(self, msg):
    if msg == 'clear':
        self.dmd.ZenEventManager.sendEvent(dict(
            device=self.id,
            summary=msg,
            eventClass='/Status',
            eventKey='ConnectionError',
            severity=0,
            ))
    else:
        self.dmd.ZenEventManager.sendEvent(dict(
            device=self.id,
            summary=msg,
            eventClass='/Status',
            eventKey='ConnectionError',
            severity=5,
            ))

    return


def getErrorNotification(self):
    return

Device.setErrorNotification = setErrorNotification
Device.getErrorNotification = getErrorNotification


class ZenPack(ZenPackBase):
    """
    ZenPack loader that handles custom installation and removal tasks.
    """

    packZProperties = [
        ('zMySqlUsername', '', 'string'),
        ('zMySqlPassword', '', 'password'),
        ('zMySqlPort', '', 'string'),
        ('zMySQLConnectionString', '', 'multilinecredentials'),
        ('zMySqlTimeout', 30, 'int'),
    ]

    def install(self, app):
        super(ZenPack, self).install(app)

        log.info('Adding MySqlMonitor relationships to existing devices')
        self._buildDeviceRelations()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:
            log.info('Removing MySqlMonitor components')
            cat = ICatalogTool(app.zport.dmd)
            for brain in cat.search(types=NEW_COMPONENT_TYPES):
                component = brain.getObject()
                component.getPrimaryParent()._delObject(component.id)

            # Remove our Device relations additions.
            Device._relations = tuple(
                [x for x in Device._relations
                    if x[0] not in NEW_DEVICE_RELATIONS])

            log.info('Removing MySqlMonitor device relationships')
            self._buildDeviceRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildDeviceRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.buildRelations()


def SizeUnitsProxyProperty(propertyName):
    """This uses a closure to make a getter and
    setter for the size property and assigns it
    a calculated value with unit type.
    """
    def setter(self, value):
        return setattr(self._object, propertyName, value)

    def getter(self):
        val = getattr(self._object, propertyName)
        try:
            val = int(val)
            if val == 0:
                return val
            units = ("B", "KB", "MB", "GB", "TB", "PB")
            i = int(math.floor(math.log(val, 1024)))
            p = math.pow(1024, i)
            s = round(val/p, 2)
            if (s > 0):
                return '%s %s' % (s, units[i])
            else:
                return '0 B'
        except:
            return val

    return property(getter, setter)
