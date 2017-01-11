##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging
LOG = logging.getLogger('zen.WBEM')

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory


# Categorize our zProperties.
setzPropertyCategory('zWBEMPort', 'WBEM')
setzPropertyCategory('zWBEMUsername', 'WBEM')
setzPropertyCategory('zWBEMPassword', 'WBEM')
setzPropertyCategory('zWBEMUseSSL', 'WBEM')


class ZenPack(ZenPackBase):
    """WBEM ZenPack."""

    packZProperties = [
        ('zWBEMPort', '5989', 'integer'),
        ('zWBEMUsername', '', 'string'),
        ('zWBEMPassword', '', 'password'),
        ('zWBEMUseSSL', True, 'boolean'),
        ]
