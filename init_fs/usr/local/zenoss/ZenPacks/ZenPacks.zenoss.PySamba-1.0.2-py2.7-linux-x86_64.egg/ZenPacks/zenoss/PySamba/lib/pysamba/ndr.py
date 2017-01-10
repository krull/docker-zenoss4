##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = "Provide access to generic NDR routines"

from .library import library

NDR_OUT = 2
def debugPrint(text, printFunct, obj):
    "Print an NDR structure to debug output"
    library.ndr_print_function_debug(printFunct, text, NDR_OUT, obj)
