##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2009, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


"""
This module provides common utilities for monitoring Windows devices.
"""

def addNTLMv2Option(parser):
    """
    Adds the --ntlmv2auth option to the provided command-line parser.
    @param parser: the command-line option parser to add the argument to
    @type parser: OptionParser
    """
    parser.add_option('--ntlmv2auth',
                  dest='ntlmv2auth',
                  default=False,
                  action="store_true",
                  help="Enable NTLMv2 Authentication for Windows Devices")

def setNTLMv2Auth(options):
    """
    Enables or disables NTLMv2 Authentication in the current process based
    upon the setting of the ntlmv2auth option.
    @param options: the command-line options object
    """
    # DO NOT PROMOTE THIS IMPORT TO THE TOP OF THE MODULE
    # only this method should depend on the successful import of the 
    # PySamba zenpack
    try:
        from pysamba.twisted import reactor
    except ImportError:
        pass
    else:
        flag = bool(getattr(options, 'ntlmv2auth', False))
        reactor.setNTLMv2Authentication(flag)
