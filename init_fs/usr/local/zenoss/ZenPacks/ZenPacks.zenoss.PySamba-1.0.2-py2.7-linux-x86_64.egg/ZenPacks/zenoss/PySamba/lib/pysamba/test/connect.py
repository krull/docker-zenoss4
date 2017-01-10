##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from ctypes import *

from ZenPacks.zenoss.PySamba.twisted.reactor import reactor, eventContext
from ZenPacks.zenoss.PySamba.library import *
from ZenPacks.zenoss.PySamba.rpc.Rpc import Rpc
from ZenPacks.zenoss.PySamba.twisted.callback import WMIFailure
import sys

import ZenPacks.zenoss.PySamba.wbem.Query

from ZenPacks.zenoss.PySamba.twisted.callback import WMIFailure
import logging
log = logging.getLogger('p.t.connect')

import Globals
from Products.ZenUtils.Driver import drive, driveLater

from twisted.internet import defer

def doOneDevice(creds, hostname):
    def inner(driver):
        while 1:
            try:
                q = Rpc()
                yield q.connect(hostname, creds, 'winreg')
                driver.next()
                q.close()
            except Exception, ex:
                log.exception(ex)
    return drive(inner)

        
def main():
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(10)
    DEBUGLEVEL.value = 99

    creds = sys.argv[1]
    hosts = sys.argv[2:]
    defs = []
    for host in hosts:
        defs.append(doOneDevice(creds, host))
    d = defer.DeferredList(defs)
    d.addBoth(lambda x : reactor.stop())
    reactor.run()

sys.exit(main())
