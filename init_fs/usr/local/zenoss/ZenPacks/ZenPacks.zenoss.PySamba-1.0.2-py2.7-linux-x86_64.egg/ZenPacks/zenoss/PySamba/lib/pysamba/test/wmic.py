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
from ZenPacks.zenoss.PySamba.wbem.wbem import *
from ZenPacks.zenoss.PySamba.wbem.Query import Query
from ZenPacks.zenoss.PySamba.twisted.callback import WMIFailure
import sys

import logging
log = logging.getLogger('p.t.wmic')

import Globals
from Products.ZenUtils.Driver import drive, driveLater

from twisted.internet import defer

def doOneDevice(creds, query, hostname):
    def inner(driver):
        try:
            q = Query()
            yield q.connect(eventContext, hostname, creds)
            driver.next()
            log.info("Query sent")
            yield q.query(query)
            result = driver.next()
            class_name = ''
            while 1:
                yield result.fetchSome()
                if not driver.next(): break
                for obj in driver.next():
                    props = [p for p in obj.__dict__.keys()
                             if not p.startswith('_')]
                    if obj._class_name != class_name:
                        class_name = obj._class_name
                        print obj._class_name
                        print repr(props)
                    print repr([getattr(obj, p) for p in props])
            q.close()
        except Exception, ex:
            log.exception(ex)
    return driveLater(0.25, inner)

        
def main():
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(10)
    DEBUGLEVEL.value = 99

    creds, query = sys.argv[1:3]
    hosts = sys.argv[3:]

    def stop(result):
        print result
        reactor.stop()
    def later():
        d = defer.DeferredList(
            [doOneDevice(creds, query, h) for h in hosts]
            )
        d.addBoth(stop)
    reactor.callLater(1, later)
    reactor.run()

sys.exit(main())
