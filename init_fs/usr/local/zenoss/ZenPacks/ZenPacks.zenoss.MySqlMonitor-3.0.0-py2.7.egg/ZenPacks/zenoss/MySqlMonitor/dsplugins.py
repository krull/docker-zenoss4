######################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is
# installed.
#
######################################################################

from logging import getLogger
log = getLogger('zen.python')

import re
import time

from twisted.enterprise import adbapi
from twisted.internet import defer

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
#from ZenPacks.zenoss.PythonCollector import patches

from ZenPacks.zenoss.MySqlMonitor.utils import parse_mysql_connection_string
from ZenPacks.zenoss.MySqlMonitor import NAME_SPLITTER


def connection_pool(ds, ip):
    servers = parse_mysql_connection_string(ds.zMySQLConnectionString)
    server = servers[ds.component.split(NAME_SPLITTER)[0]]
    return adbapi.ConnectionPool(
        "MySQLdb",
        cp_reconnect=True,
        host=ip,
        user=server['user'],
        port=server['port'],
        passwd=server['passwd']
    )


def datasource_to_dbpool(ds, ip, dbpool_cache={}):
    servers = parse_mysql_connection_string(ds.zMySQLConnectionString)
    server = servers[ds.component.split(NAME_SPLITTER)[0]]

    connection_key = (ip, server['user'], server['port'], server['passwd'])
    if not((connection_key in dbpool_cache)
            and dbpool_cache[connection_key].running):
        dbpool_cache[connection_key] = connection_pool(ds, ip)
    return dbpool_cache[connection_key]


class MysqlBasePlugin(PythonDataSourcePlugin):
    proxy_attributes = ('zMySQLConnectionString', 'table_count')

    def get_query(self, component):
        raise NotImplemented

    def query_results_to_values(self, results):
        return {}

    def query_results_to_events(self, results, ds):
        return []

    def query_results_to_maps(self, results, component):
        return []

    @defer.inlineCallbacks
    def collect(self, config):
        values = {}
        events = []
        maps = []
        res = None
        for ds in config.datasources:
            try:
                try:
                    dbpool = datasource_to_dbpool(ds, config.manageIp)
                    res = yield dbpool.runQuery(self.get_query(ds.component))
                except Exception, e:
                    if 'MySQL server has gone away' in str(e) or\
                            "Can't connect to MySQL server" in str(e):
                        dbpool = connection_pool(ds, config.manageIp)
                        res = yield dbpool.runQuery(
                            self.get_query(ds.component)
                        )
                if res:
                    values[ds.component] = self.query_results_to_values(res)
                    events.extend(self.query_results_to_events(res, ds))
                    maps.extend(self.query_results_to_maps(res, ds.component))
            except Exception, e:
                if NAME_SPLITTER not in ds.component:
                    events.append({
                        'component': ds.component,
                        'summary': str(e),
                        'eventClass': '/Status',
                        'eventKey': 'mysql_result',
                        'severity': 4,
                    })

        defer.returnValue(dict(
            events=events,
            values=values,
            maps=maps,
        ))

    def onSuccess(self, result, config):
        for component in result["values"].keys():
            # Clear events for success components.
            result['events'].insert(0, {
                'component': component,
                'summary': 'Monitoring ok',
                'eventClass': '/Status',
                'eventKey': 'mysql_result',
                'severity': 0,
            })
        return result

    def onError(self, result, config):
        log.error(result)
        return {
            'vaues': {},
            'events': [{
                'summary': 'error: %s' % result,
                'eventClass': '/Status',
                'eventKey': 'mysql_result',
                'severity': 4,
            }],
            'maps': [],
        }


class MySqlMonitorPlugin(MysqlBasePlugin):
    def get_query(self, component):
        return 'show global status'

    def query_results_to_values(self, results):
        return dict((k.lower(), (v, 'N')) for k, v in results)


class MySqlDeadlockPlugin(MysqlBasePlugin):
    deadlock_re = re.compile(
        '\n-+\n(LATEST DETECTED DEADLOCK\n-+\n.*?\n)-+\n',
        re.M | re.DOTALL
    )

    def get_query(self, component):
        return 'show engine innodb status'

    def query_results_to_events(self, results, ds):
        text = results[0][2]
        deadlock_match = self.deadlock_re.search(text)
        if deadlock_match:
            summary = deadlock_match.group(1)
            severity = 3
        else:
            summary = 'No last deadlock data'
            severity = 0

        return [{
            'severity': severity,
            'eventKey': 'innodb_deadlock',
            'eventClass': '/Status',
            'summary': summary,
            'component': ds.component,
        }]


class MySqlReplicationPlugin(MysqlBasePlugin):
    def get_query(self, component):
        return 'show slave status'

    def _event(self, severity, summary, component, suffix):
        return {
            'severity': severity,
            'eventKey': 'replication_status_' + suffix,
            'eventClass': '/Status',
            'summary': summary,
            'component': component,
        }

    def query_results_to_events(self, results, ds):
        if not results:
            # Not a slave MySQL
            return []

        # Slave_IO_Running: Yes
        # Slave_SQL_Running: Yes
        slave_io = results[0][10]
        slave_sql = results[0][11]
        # Last_Errno: 0
        # Last_Error:
        last_err_no = results[0][18]
        last_err_str = results[0][19]
        # Last_IO_Errno: 0
        # Last_IO_Error:
        last_io_err_no = results[0][34]
        last_io_err_str = results[0][35]
        # Last_SQL_Errno: 0
        # Last_SQL_Error:
        last_sql_err_no = results[0][36]
        last_sql_err_str = results[0][37]

        c = ds.component
        events = []

        if slave_io == "Yes":
            events.append(self._event(0, "Slave IO Running", c, "io"))
        else:
            events.append(self._event(4, "Slave IO NOT Running", c, "io"))

        if slave_sql == "Yes":
            events.append(self._event(0, "Slave SQL Running", c, "sql"))
        else:
            events.append(self._event(4, "Slave SQL NOT Running", c, "sql"))

        if last_err_str:
            events.append(self._event(4, last_err_str, c, "err"))
        else:
            events.append(self._event(0, "No replication error", c, "err"))

        if last_io_err_str:
            events.append(self._event(4, last_io_err_str, c, "ioe"))
        else:
            events.append(self._event(0, "No replication IO error", c, "ioe"))

        if last_sql_err_str:
            events.append(self._event(4, last_sql_err_str, c, "se"))
        else:
            events.append(self._event(0, "No replication SQL error", c, "se"))

        return events


class MySQLMonitorServersPlugin(MysqlBasePlugin):
    def get_query(self, component):
        return '''
        SELECT
            count(table_name) table_count,
            sum(data_length + index_length) size,
            sum(data_length) data_size,
            sum(index_length) index_size
        FROM
            information_schema.TABLES
        '''

    def query_results_to_values(self, results):
        t = time.time()
        fields = enumerate(('table_count', 'size', 'data_size', 'index_size'))
        return dict((f, (results[0][i] or 0, t)) for i, f in fields)


class MySQLMonitorDatabasesPlugin(MysqlBasePlugin):
    def get_query(self, component):
        return '''
        SELECT
            count(table_name) table_count,
            sum(data_length + index_length) size,
            sum(data_length) data_size,
            sum(index_length) index_size
        FROM
            information_schema.TABLES
        WHERE
            table_schema = "%s"
        ''' % adbapi.safe(component.split(NAME_SPLITTER)[-1])

    def query_results_to_values(self, results):
        fields = enumerate(('table_count', 'size', 'data_size', 'index_size'))
        return dict((f, (results[0][i] or 0, 'N')) for i, f in fields)

    def query_results_to_maps(self, results, component):
        table_count = results[0][0]
        server = component.split(NAME_SPLITTER)[0]
        om = ObjectMap({
            "compname": "mysql_servers/%s/databases/%s" % (
                server, component),
            "modname": "Tables count",
            "table_count": table_count
        })
        return [om]

    def query_results_to_events(self, results, ds):
        if not ds.table_count:
            ds.table_count = 0

        diff = results[0][0] - ds.table_count
        if diff == 0:
            return []

        grammar = 'table was' if abs(diff) == 1 else 'tables were'
        key, severity = ('added', 2) if diff > 0 else ('dropped', 3)
        return [{
            'severity': severity,
            'eventKey': 'table_count%s' % str(time.time()),
            'eventClass': '/Status',
            'summary': '{0} {1} {2}.'.format(abs(diff), grammar, key),
            'component': ds.component.split(NAME_SPLITTER)[-1],
        }]


class MySQLDatabaseExistencePlugin(MysqlBasePlugin):
    def get_query(self, component):
        return ''' SELECT COUNT(*)
            FROM information_schema.SCHEMATA
            WHERE SCHEMA_NAME="%s"
        ''' % adbapi.safe(
            component.split(NAME_SPLITTER)[-1]
        )

    def query_results_to_events(self, results, ds):
        if not results[0][0]:
            # Database does not exist, will be deleted
            db_name = ds.component.split(NAME_SPLITTER)[-1]
            return [{
                'severity': 2,
                'eventKey': 'db_%s_dropped' % db_name,
                'eventClass': '/Status',
                'summary': 'Database "%s" was dropped.' % db_name,
                'component': ds.component.split(NAME_SPLITTER)[0],
            }]
        return []

    def query_results_to_maps(self, results, component):
        if not results[0][0]:
            # Database does not exist, will be deleted
            server = component.split(NAME_SPLITTER)[0]
            om = ObjectMap({
                "compname": "mysql_servers/%s" % server,
                "modname": "Remove/add",
                "remove": component
            })
            return [om]
        return []
