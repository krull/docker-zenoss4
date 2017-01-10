##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""
Support classes for integrating deferreds into the Samba asynchronous framework
"""

from ..library import logFuncCall
from ..composite_context import *
from twisted.internet import defer

DEFERS = {}
COUNTER = 0L

class WMIFailure(Exception):
    "Exception that represents a composite_context failure"
    def __str__(self):
        ex = self
        while isinstance(ex.args[0], WMIFailure):
            ex = ex.args[0]
        return library.nt_errstr(ex.args[1])

class Callback(object):
    "Turn a composite_context callback into a deferred callback"
    def __init__(self):
        # keep a reference to this object as long as it lives in the C code
        global COUNTER
        COUNTER += 1
        self.which = COUNTER
        DEFERS[self.which] = self
        self.callback = composite_context_callback(self.callback)
        self.deferred = defer.Deferred()

    @logFuncCall
    def callback(self, ctx):
        # remove the reference to the object now that we're out of C code
        try:
            DEFERS.pop(self.which)
        except KeyError, ex:
            log.error("Encountered error in pysamba.Callback.callback: " + ex)
        d = self.deferred
        if ctx.contents.state == COMPOSITE_STATE_DONE:
            d.callback(ctx.contents.async.private_data)
        else:
            d.errback(WMIFailure(ctx.contents.state,
                                 ctx.contents.status))
