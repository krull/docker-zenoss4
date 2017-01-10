##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import re
from ZenPacks.zenoss.WindowsMonitor.WMIPlugin import WMIPlugin


class MSMQQueueMap(WMIPlugin):
    relname = "msmqqueues"
    modname = "ZenPacks.zenoss.MSMQMonitor.MSMQQueue"

    deviceProperties = WMIPlugin.deviceProperties + (
        'zMSMQIgnoreQueues',)

    def queries(self):
        return {
            'MSMQQueue': \
            'Select name From Win32_PerfFormattedData_MSMQ_MSMQQueue',
            }

    def process(self, device, results, log):
        log.info('Collecting MSMQ queues for device %s', device.id)

        ignore = getattr(device, 'zMSMQIgnoreQueues', None)
        if ignore:
            ignore = re.compile(ignore).search

        rm = self.relMap()
        for queue in results['MSMQQueue']:
            if not getattr(queue, 'name', None):
                continue

            om = self.objectMap()

            # Skip queue names that match zMSMQIgnoreQueues.
            if ignore and ignore(queue.name):
                continue

            om.id = self.prepId(queue.name.replace('$', ''))
            om.queueName = queue.name
            om.perfmonInstance = '\MSMQ Queue(%s)' % queue.name
            rm.append(om)

        return rm
