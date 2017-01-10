##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class dfi(ComponentCommandParser):

    componentSplit = '\n'

    componentScanner = '[%-] +(?P<component>/.*)'

    scanners = [
        r' (?P<totalInodes>\d+) +(?P<usedInodes>\d+) +'
        r'(?P<availableInodes>\d+) +(?P<percentInodesUsed>\d+)%'
        ]
    
    componentScanValue = 'mount'
