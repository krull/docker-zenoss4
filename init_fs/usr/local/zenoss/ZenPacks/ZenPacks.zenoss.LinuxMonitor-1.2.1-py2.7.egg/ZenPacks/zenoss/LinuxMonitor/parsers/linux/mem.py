##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.ZenRRD.CommandParser import CommandParser

MULTIPLIER = {
    'kB' : 1024,
    'MB' : 1024 * 1024,
    'b' : 1
}

class mem(CommandParser):

    def processResults(self, cmd, result):
        """
        Process the results of "cat /proc/meminfo".
        """
        datapointMap = dict([(dp.id, dp) for dp in cmd.points])
        data = [line.split(':', 1) for line in cmd.result.output.splitlines()]
        
        for id, vals in data:
            if id in datapointMap:
                try:
                    value, unit = vals.strip().split()
                except:
                    value = vals
                    unit = 1
                size = int(value) * MULTIPLIER.get(unit, 1)
                result.values.append((datapointMap[id], size))
        
        return result
