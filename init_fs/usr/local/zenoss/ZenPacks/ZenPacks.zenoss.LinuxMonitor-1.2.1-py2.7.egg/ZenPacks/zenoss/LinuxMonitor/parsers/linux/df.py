##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class df(ComponentCommandParser):

    componentSplit = '\n'

    componentScanner = '% (?P<component>/.*)'

    scanners = [
        r' (?P<totalBlocks>\d+) +(?P<usedBlocks>\d+) '
        r'+(?P<availBlocks>\d+) +(?P<percentUsed>\d+)%'
        ]
    
    componentScanValue = 'mount'
