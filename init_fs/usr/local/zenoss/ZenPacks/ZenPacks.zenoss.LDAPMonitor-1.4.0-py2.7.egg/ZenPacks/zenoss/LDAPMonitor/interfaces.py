##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2010, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


from Products.Zuul.interfaces import IRRDDataSourceInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class ILDAPMonitorDataSourceInfo(IRRDDataSourceInfo):
    cycletime = schema.Int(title=_t(u'Cycle Time (seconds)'))
    timeout = schema.Int(title=_t(u'Timeout (seconds)'))
    ldapServer = schema.TextLine(title=_t(u'LDAP Server'), group=_t(u'LDAP'))
    ldapBindDN = schema.TextLine(title=_t(u'Bind Distinguished Name'), group=_t(u'LDAP'))
    useSSL = schema.Bool(title=_t(u'Use SSL?'), group=_t(u'LDAP'))
    ldapBaseDN = schema.TextLine(title=_t(u'Base Distinguished Name'), group=_t(u'LDAP'))
    ldapBindVersion = schema.TextLine(title=_t(u'Bind Version'), group=_t(u'LDAP'))
    ldapBindPassword = schema.Password(title=_t(u'Bind Password'), group=_t(u'LDAP'))
    port = schema.Int(title=_t(u'Port'), group=_t(u'LDAP'))
