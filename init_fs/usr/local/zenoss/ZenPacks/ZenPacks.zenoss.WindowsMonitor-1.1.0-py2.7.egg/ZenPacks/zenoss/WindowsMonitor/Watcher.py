##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2007-2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from pysamba.twisted.reactor import eventContext
from pysamba.wbem.Query import Query
from Products.ZenUtils.Driver import drive
from twisted.internet import defer

import logging
log = logging.getLogger("zen.Watcher")

class Watcher(object):

    def __init__(self, device, query):
        self.wmi = Query()
        self.device = device
        self.queryString = query
        self.enum = None
        self.busy = False
        self.closeRequested = False
        log.debug("Starting watcher on %s", device.id)

    @defer.inlineCallbacks
    def connect(self):
        self.busy = True
        try:
            log.debug("connecting to %s", self.device.id)
            d = self.device

            yield self.wmi.connect(eventContext,
                                   d.id,
                                   d.manageIp,
                                   "%s%%%s" % (d.zWinUser, d.zWinPassword))

            log.debug("connected to %s sending query %s", self.device.id, self.queryString)
            self.enum = yield self.wmi.notificationQuery(self.queryString)
            log.debug("got query response from %s", self.device.id)
        finally:
            self.busy = False
            if self.closeRequested:
                self.close()

    @defer.inlineCallbacks
    def getEvents(self, timeout=0, chunkSize=10):
        assert self.enum
        self.busy = True
        log.debug("Fetching events for %s", self.device.id)
        result = []

        try:
            result = yield self.enum.fetchSome(timeoutMs=timeout, chunkSize=chunkSize)
        finally:
            self.busy = False
            if self.closeRequested:
                self.close()

        log.debug("Events fetched for %s", self.device.id)
        defer.returnValue(result)
    
    def close(self):
        if self.busy:
            log.debug("close requested on busy WMI Query for %s; deferring",
                           self.device.id)
            self.closeRequested = True
        elif self.wmi:
            log.debug("closing WMI Query for %s", self.device.id)
            self.wmi.close()
            self.wmi = None

    def __del__(self):
        log.debug("Watcher.__del__ called for %s, busy=%r closeRequested=%r",
                  self.device.id, self.busy, self.closeRequested)
        self.close()
