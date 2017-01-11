##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

from zope.component import adapts
from zope.interface import implements

from Products.ZenRelations.RelSchema import ToOne, ToMany, ToManyCont

from Products.Zuul.catalog.paths import DefaultPathReporter, relPath
from Products.Zuul.decorators import info
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from . import CLASS_NAME, MODULE_NAME, SizeUnitsProxyProperty
from .MySQLComponent import MySQLComponent
from .utils import updateToMany, updateToOne


class MySQLServer(MySQLComponent):
    meta_type = portal_type = 'MySQLServer'

    size = None
    data_size = None
    index_size = None
    percent_full_table_scans = None
    slave_status = None
    master_status = None
    version = None
    deadlock_info = None

    _properties = MySQLComponent._properties + (
        {'id': 'size', 'type': 'string'},
        {'id': 'data_size', 'type': 'string'},
        {'id': 'index_size', 'type': 'string'},
        {'id': 'percent_full_table_scans', 'type': 'string'},
        {'id': 'slave_status', 'type': 'string'},
        {'id': 'master_status', 'type': 'string'},
        {'id': 'version', 'type': 'string'},
    )

    _relations = MySQLComponent._relations + (
        ('mysql_host', ToOne(
            ToManyCont, 'Products.ZenModel.Device.Device', 'mysql_servers')),
        ('databases', ToManyCont(
            ToOne, MODULE_NAME['MySQLDatabase'], 'server')),
    )

    def remove(self, object_id=None):
        if object_id:
            self.databases._delObject(object_id)

    def device(self):
        return self.mysql_host()

    # def getStatus(self):
        # return super(MySQLServer, self).getStatus("/Status")


class IMySQLServerInfo(IComponentInfo):
    '''
    API Info interface for MySQLServer.
    '''

    # size = schema.TextLine(title=_t(u'Size'))
    # data_size = schema.TextLine(title=_t(u'Data Size'))
    # index_size = schema.TextLine(title=_t(u'Index Size'))
    percent_full_table_scans = schema.TextLine(
        title=_t(u'Percentage of full table scans'))
    slave_status = schema.TextLine(title=_t(u'Slave status'))
    master_status = schema.TextLine(title=_t(u'Master status'))
    version = schema.TextLine(title=_t(u'Version'))
    db_count = schema.TextLine(title=_t(u'Number of databases'))


class MySQLServerInfo(ComponentInfo):
    ''' API Info adapter factory for MySQLServer '''

    implements(IMySQLServerInfo)
    adapts(MySQLServer)

    size = SizeUnitsProxyProperty('size')
    data_size = SizeUnitsProxyProperty('data_size')
    index_size = SizeUnitsProxyProperty('index_size')
    percent_full_table_scans = ProxyProperty('percent_full_table_scans')
    slave_status = ProxyProperty('slave_status')
    master_status = ProxyProperty('master_status')
    version = ProxyProperty('version')
    deadlock_info = ProxyProperty('deadlock_info')

    @property
    def db_count(self):
        return self._object.databases.countObjects()
