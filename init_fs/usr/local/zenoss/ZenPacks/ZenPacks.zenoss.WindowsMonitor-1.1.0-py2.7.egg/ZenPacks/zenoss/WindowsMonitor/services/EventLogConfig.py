##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__='''EventLogConfig

Provides configuration to zeneventlog clients.
'''

import Globals

from Products.ZenCollector.services.config import CollectorConfigService

import logging
log = logging.getLogger('zen.ModelerService.EventLogConfig')

class EventLogConfig(CollectorConfigService):
    def __init__(self, dmd, instance):
        deviceProxyAttributes = ('zWmiMonitorIgnore',
                                 'zWinUser',
                                 'zWinPassword',
                                 'zWinEventlogMinSeverity',
                                 'zWinEventlogClause')
        CollectorConfigService.__init__(self, dmd, instance, deviceProxyAttributes)

    def _filterDevice(self, device):
        include = CollectorConfigService._filterDevice(self, device)

        if getattr(device, 'zWmiMonitorIgnore', False):
            self.log.debug("Device %s skipped because zWmiMonitorIgnore is True",
                           device.id)
            include = False

        elif not getattr(device, 'zWinEventlog', True):
            log.debug("Device %s skipped because zWinEventlog is False",
                      device.id)
            include = False

        return include

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)

        # for now, every device gets a single configCycleInterval based upon
        # the collector's eventlogCycleInterval configuration.
        # TODO: create a zProperty that allows for individual device schedules
        proxy.configCycleInterval = self._prefs.eventlogCycleInterval

        return proxy


if __name__ == '__main__':
    from Products.ZenHub.ServiceTester import ServiceTester
    tester = ServiceTester(EventLogConfig)
    def printer(config):
        print "zWinEventlogMinSeverity = %s" % config.zWinEventlogMinSeverity
        print "zWinEventlogClause = '%s'" % config.zWinEventlogClause
    tester.printDeviceProxy = printer
    tester.showDeviceInfo()
