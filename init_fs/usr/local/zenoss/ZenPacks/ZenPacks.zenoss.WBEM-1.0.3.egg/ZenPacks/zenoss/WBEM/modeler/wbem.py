##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""API interface to the PyWBEM library.

WBEM classes available
    EnumerateClassNames
    EnumerateClasses
    EnumerateInstances
    EnumerateInstanceNames

example:
    wbemQueries = {
        'ec':'root/emc',
        'ein':'root/emc:CIM_ManagedElement'
        }

You must also have the zWBEMPort, zWBEMUsername and zWBEMPassword properties
set to succesfully pull data.

"""

from twisted.internet import ssl, reactor
from twisted.internet.defer import DeferredList

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath, result_errmsg

addLocalLibPath()

from pywbem.twisted_client import (
    EnumerateClassNames,
    EnumerateClasses,
    EnumerateInstanceNames,
    EnumerateInstances,
)


class WBEMPlugin(PythonPlugin):

    deviceProperties = PythonPlugin.deviceProperties + (
        'zWBEMPort',
        'zWBEMUsername',
        'zWBEMPassword',
        'zWBEMUseSSL',
    )

    wbemQueries = {}

    def collect(self, device, log):
        if not device.manageIp:
            log.error('%s has no management IP address', device.id)

        if not device.zWBEMPort:
            log.error("zWBEMPort empty for %s", device.id)

        if not device.zWBEMUsername:
            log.error("zWBEMUsername empty for %s", device.id)

        if not device.zWBEMPassword:
            log.error("zWBEMPassword empty for %s", device.id)

        if not device.manageIp or \
            not device.zWBEMPort or \
            not device.zWBEMUsername or \
            not device.zWBEMPassword:
            return None

        deferreds = []

        for wbemnamespace, wbemclass in self.wbemQueries.items():
            namespaces = wbemnamespace.split(":")
            namespace = namespaces[0]
            if len(namespaces) > 1:
                classname = namespaces[1]

            userCreds = (device.zWBEMUsername, device.zWBEMPassword)

            if wbemclass == 'ec':
                wbemClass = EnumerateClasses(
                    userCreds, namespace=namespace)

            elif wbemclass == 'ecn':
                wbemClass = EnumerateClassNames(
                    userCreds, namespace=namespace)

            elif wbemclass == 'ei':
                wbemClass = EnumerateInstances(
                    userCreds, namespace=namespace, classname=classname)

            elif wbemclass == 'ein':
                wbemClass = EnumerateInstanceNames(
                    userCreds, namespace=namespace, classname=classname)

            else:
                log.warn('Incorrect class call %s', wbemclass)
                wbemClass = EnumerateClasses(userCreds,
                                             namespace=namespace)

            deferreds.append(wbemClass.deferred)

            if device.zWBEMUseSSL == True:
                reactor.connectSSL(
                    host=device.manageIp,
                    port=int(device.zWBEMPort),
                    factory=wbemClass,
                    contextFactory=ssl.ClientContextFactory())
            else:
                reactor.connectTCP(
                    host=device.manageIp,
                    port=int(device.zWBEMPort),
                    factory=wbemClass)

        # Execute the deferreds and return the results to the callback.
        d = DeferredList(deferreds, consumeErrors=True)
        d.addCallback(self.check_results, device, log)

        return d

    def check_results(self, results, device, log):
        """Check results for errors."""

        # If all results are failures we have a problem to report.
        if len(results) and True not in set(x[0] for x in results):
            log.error('%s WBEM: %s', device.id, result_errmsg(results[0][1]))

            #This will allow for an event to be created by the device class.
            results = "ERROR", result_errmsg(results[0][1])

            return results

        return results
