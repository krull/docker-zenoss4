##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.interfaces import IInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IWinPerfDataSourceInfo(IInfo):
    name = schema.TextLine(title=_t(u"Name"),
                           xtype="idfield",
                           description=_t(u"The name of this datasource"))
    type = schema.TextLine(title=_t(u"Type"),
                           readonly=True)
    counter = schema.TextLine(title=_t(u"Perf Counter"),
                              description=_t(u"Example: \Memory\Available bytes "))
    enabled = schema.Bool(title=_t(u"Enabled"))
