##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging
log = logging.getLogger("zen.migrate")


from Products.ZenModel.DeviceClass import DeviceClass
from Products.ZenModel.migrate.Migrate import Version
from Products.ZenModel.ZenPack import ZenPackMigration

TEMPLATE_NAME = 'MySQL'
MODELER_PLUGIN_NAME = 'MySQLCollector'


def name_for_thing(widget):
    ''' Helper function to provide the name of the Device or DeviceClass '''

    if isinstance(widget, DeviceClass):
        return widget.getOrganizerName()

    return widget.titleOrId()


class MigrateConnectionString(ZenPackMigration):
    ''' Main class that contains the migrate() method.
    Note version setting. '''
    version = Version(3, 0, 0)

    def migrate(self, dmd):
        '''
        This is the main method. Its searches for overridden objects
        (templates) and then migrates the data to the new format or
        properties. In this case bound objects get assigned the new
        modeler pluging.
        '''
        overridden_on = dmd.Devices.getOverriddenObjects(
            'zDeviceTemplates', showDevices=True)

        for thing in overridden_on:
            if TEMPLATE_NAME in thing.zDeviceTemplates:
                self.enable_plugin(thing)
                self.populate_connection_strings(thing)

    def enable_plugin(self, thing):
        '''
        Associate a collector plugin with the thing we have found.
        zCollectorPlugins is used by ModelerService.createDeviceProxy()
        to add associated (modeler) plugins to the list for
        self-discovery. ModelerService.remote_getDeviceConfig() actually
        calls the modelers.
        '''
        current_plugins = list(thing.zCollectorPlugins)
        if MODELER_PLUGIN_NAME in current_plugins:
            return

        log.info(
            "Adding %s modeler plugin to %s",
            MODELER_PLUGIN_NAME, name_for_thing(thing))

        current_plugins.append(MODELER_PLUGIN_NAME)
        thing.setZenProperty('zCollectorPlugins', current_plugins)

    def populate_connection_strings(self, thing):
        ''' Just a helper method to collect data for this ZP '''

        if thing.zMySQLConnectionString:
            return

        if thing.zMySqlUsername:
            connection_string = '{"user":"%s","passwd":"%s","port":"%s"}' % \
                (thing.zMySqlUsername, thing.zMySqlPassword, thing.zMySqlPort)

            log.info(
                "Setting zMySQLConnectionString for %s",
                name_for_thing(thing))

            thing.setZenProperty('zMySQLConnectionString', [connection_string])


MigrateConnectionString()
