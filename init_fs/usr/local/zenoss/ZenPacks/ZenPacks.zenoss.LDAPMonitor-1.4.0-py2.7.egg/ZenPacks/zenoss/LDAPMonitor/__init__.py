##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


import Globals
import os.path

import logging
log = logging.getLogger("zen.LDAPMonitor")

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    packZProperties = [
        ('zLDAPBaseDN', 'dc=zenoss,dc=com', 'string'),
        ('zLDAPBindDN', '', 'string'),
        ('zLDAPBindPassword', '', 'password'),
    ]

def onCollectorInstalled(ob, event):
    zpFriendly = 'LDAPMonitor'
    errormsg = '{0} binary cannot be found on {1}. This is part of the nagios-plugins ' + \
               'dependency, and must be installed before {2} can function.'
    
    verifyBin = 'check_ldap'
    code, output = ob.executeCommand('zenbincheck %s' % verifyBin, 'zenoss', needsZenHome=True)
    if code:
       	log.warn(errormsg.format(verifyBin, ob.hostname, zpFriendly))
    
    verifyBin = 'check_ldaps'
    code, output = ob.executeCommand('zenbincheck %s' % verifyBin, 'zenoss', needsZenHome=True)
    if code:
       	log.warn(errormsg.format(verifyBin, ob.hostname, zpFriendly))
