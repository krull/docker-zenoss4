##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007-2013, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.DataCollector.plugins.CollectorPlugin import CollectorPlugin

class WMIPlugin(CollectorPlugin):
    """
    A WMIPlugin defines a native Python collection routine and a parsing
    method to turn the returned data structure into a datamap. A valid
    WMIPlugin must implement the process method.
    """
    transport = "wmi"
    deviceProperties = CollectorPlugin.deviceProperties + (
        'zWmiMonitorIgnore', 
        'zWinUser',
        'zWinPassword',
        'zWinEventlogMinSeverity',
        'zWinEventlogClause',
    )
    
    def condition(self, device, log):
        return not getattr(device, 'zWmiMonitorIgnore', True)

    def copyDataToProxy(self, device, proxy):
        for prop in self.deviceProperties:
            if device.hasProperty(prop, useAcquisition=True):
                value = device.getProperty(prop)
            elif hasattr(device, prop):
                value = getattr(device, prop)
                if callable(value):
                    value = value()
            else:
                continue
            setattr(proxy, prop, value)
        # Do any other prep of plugin here
        setattr(proxy, 'lastChange', getattr(device, '_lastChange', ''))

    def queries(self):
        raise NotImplementedError
    
    def preprocess(self, results, log):
        if isinstance(results, Exception):
            log.error(results)
            return None
        return results
