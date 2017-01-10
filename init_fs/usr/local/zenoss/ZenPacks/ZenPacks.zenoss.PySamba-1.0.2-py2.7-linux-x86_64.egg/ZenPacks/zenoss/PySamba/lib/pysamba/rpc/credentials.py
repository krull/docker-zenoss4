##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008-2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__ = "Define constants needed for the cli_credentials structure"

( CRED_UNINITIALISED,
  CRED_GUESS_ENV,
  CRED_CALLBACK, 
  CRED_GUESS_FILE,
  CRED_CALLBACK_RESULT, 
  CRED_SPECIFIED ) = range(6)
