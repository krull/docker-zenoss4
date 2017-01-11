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


class MySQLDatabase(MySQLComponent):
    meta_type = portal_type = 'MySQLDatabase'

    size = None
    data_size = None
    index_size = None
    default_character_set_name = None
    default_collation_name = None
    table_count = None

    _properties = MySQLComponent._properties + (
        {'id': 'size', 'type': 'string'},
        {'id': 'data_size', 'type': 'string'},
        {'id': 'index_size', 'type': 'string'},
        {'id': 'default_character_set_name', 'type': 'string'},
        {'id': 'default_collation_name', 'type': 'string'},
        {'id': 'table_count', 'type': 'int'},
    )

    _relations = MySQLComponent._relations + (
        ('server', ToOne(ToManyCont, MODULE_NAME['MySQLServer'], 'databases')),
    )

    def device(self):
        return self.server().device()

    # def getStatus(self):
    #     return super(MySQLDatabase, self).getStatus("/Status")


class IMySQLDatabaseInfo(IComponentInfo):
    '''
    API Info interface for MySQLDatabase.
    '''

    device = schema.Entity(title=_t(u'Device'))
    server = schema.Entity(title=_t(u'Server'))
    # size = schema.TextLine(title=_t(u'Size'))
    # data_size = schema.TextLine(title=_t(u'Data size'))
    # index_size = schema.TextLine(title=_t(u'Index size'))
    default_character_set_name = \
        schema.TextLine(title=_t(u'Default character set'))
    default_collation_name = schema.TextLine(title=_t(u'Default collation'))
    table_count = schema.Int(title=_t(u'Number of tables'))


class MySQLDatabaseInfo(ComponentInfo):
    '''
    API Info adapter factory for MySQLDatabase.
    '''

    implements(IMySQLDatabaseInfo)
    adapts(MySQLDatabase)

    table_count = ProxyProperty('table_count')
    size = SizeUnitsProxyProperty('size')
    data_size = SizeUnitsProxyProperty('data_size')
    index_size = SizeUnitsProxyProperty('index_size')
    default_character_set_name = ProxyProperty('default_character_set_name')
    default_collation_name = ProxyProperty('default_collation_name')

    @property
    @info
    def device(self):
        return self._object.device()

    @property
    @info
    def server(self):
        return self._object.server()


class MySQLDatabasePathReporter(DefaultPathReporter):
    ''' Path reporter for MySQLDatabase.  '''

    def getPaths(self):
        return super(MySQLDatabasePathReporter, self).getPaths()
