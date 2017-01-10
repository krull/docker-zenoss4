
import Globals
import os.path

import logging
log = logging.getLogger("zen.DigMonitor")

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def onCollectorInstalled(ob, event):
    zpFriendly = 'DigMonitor'
    errormsg = '{0} binary cannot be found on {1}. This is part of the nagios-plugins ' + \
               'dependency, and must be installed before {2} can function.'
    
    verifyBin = 'check_dig'
    code, output = ob.executeCommand('zenbincheck %s' % verifyBin, 'zenoss', needsZenHome=True)
    if code:
       	log.warn(errormsg.format(verifyBin, ob.hostname, zpFriendly))
