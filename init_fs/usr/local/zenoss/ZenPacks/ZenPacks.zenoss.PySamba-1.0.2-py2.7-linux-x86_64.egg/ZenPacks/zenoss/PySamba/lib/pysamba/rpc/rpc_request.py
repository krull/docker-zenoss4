##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="Define the rpc_request structure."

from ..library import *

class rpc_request(Structure): pass
class dcerpc_pipe(Structure): pass
class GUID(Structure):
    _fields_ = [
        ]
class DATA_BLOB(Structure):
    _fields_ = [
        ('data', POINTER(uint8_t)),
        ('length', size_t),
        ]
class ndr(Structure):
    _fields_ = [
        ('table', c_void_p),            # lie: POINTER(dcerpc_interface_table)
        ('opnum', uint32_t),
        ('struct_ptr', c_void_p),
        ('mem_ctx', c_void_p),          # lie: POINTER(TALLOC_CTX)
        ]
class async(Structure):
    _fields_ = [
        ('callback', CFUNCTYPE(None, POINTER(rpc_request))),
        ('private', c_void_p),
        ]

rpc_request._fields_ = [
    ('next', POINTER(rpc_request)),
    ('prev', POINTER(rpc_request)),
    ('p', POINTER(dcerpc_pipe)),
    ('status', NTSTATUS),
    ('call_id', uint32_t),
    ('state', enum),
    ('payload', DATA_BLOB),
    ('flags', uint32_t),
    ('fault_code', uint32_t),
    ('recv_handler', c_void_p),           # lie
    ('object', POINTER(GUID)),
    ('opnum', uint16_t), 
    ('request_data', DATA_BLOB),
    ('async_call', BOOL),
    ('ndr', ndr),
    ('async', async),
    ]
