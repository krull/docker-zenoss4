###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2011, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import os.path

from zope.event import notify
from Products.Zuul.catalog.events import IndexingEvent


def load_data(filename):
    path = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(path, 'r') as f:
        return f.read()


def add_obj(relationship, obj):
    '''
    Add obj to relationship, index it, then returns the persistent
    object.
    '''
    relationship._setObject(obj.id, obj)
    obj = relationship._getOb(obj.id)
    obj.index_object()
    notify(IndexingEvent(obj))
    return obj


def test_device(dmd, factor=1):
    '''
    Return an example MySqlMonitorDevice with a full set of example components.
    '''
    from ZenPacks.zenoss.MySqlMonitor.MySQLDatabase import MySQLDatabase
    from ZenPacks.zenoss.MySqlMonitor.MySQLServer import MySQLServer

    dc = dmd.Devices.createOrganizer('/Server')
    dc.setZenProperty('zPythonClass', 'Products.ZenModel.Device.Device')

    device = dc.createInstance('device')
    device.setPerformanceMonitor('localhost')
    device.index_object()
    notify(IndexingEvent(device))

    # Server
    for server_id in range(factor):
        server = add_obj(
            device.mysql_servers,
            MySQLServer('server%s' % (
                server_id)))

        # Database
        for database_id in range(factor):
            database = add_obj(
                server.databases,
                MySQLDatabase('database%s-%s' % (
                    server_id, database_id)))

    return device
