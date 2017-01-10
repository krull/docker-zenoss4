##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="Define structure for the ServerAlive2 RPC call"

from ..library import *

class COMVERSION(Structure):
    _fields_ = [
        ('MajorVersion', uint16_t),
        ('MinorVersion', uint16_t),
        ]

class COMINFO(Structure):
    _fields_ = [
        ('version', COMVERSION),
        ('unknown1', uint32_t),
        ]

class DUALSTRINGARRAY(Structure):
    _fields_ = [
        ('stringbindings', c_void_p), # POINTER(POINTER(STRINGBINDING))),
        ('securitybindings', c_void_p), # POINTER(PIONTER(SECURITYBINDING))),
        ]

uint_t = c_uint
class ServerAlive2_out(Structure):
    _fields_ = [
        ('info', POINTER(COMINFO)),
        ('dualstring', POINTER(DUALSTRINGARRAY)),
        ('unknown2', uint8_t*3),
        ('result', WERROR),
        ]
    
class ServerAlive2(Structure):
    _fields_ = [('out', ServerAlive2_out)]
