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
import MySQLdb

from twisted.internet import defer, threads

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
from Products.ZenEvents import ZenEventClasses
from Products.DataCollector.plugins.DataMaps import ObjectMap
#from ZenPacks.zenoss.PythonCollector import patches

from ZenPacks.zenoss.MySqlMonitor.utils import (
    parse_mysql_connection_string, adbapi_safe)
from ZenPacks.zenoss.MySqlMonitor import NAME_SPLITTER


def connection_cursor(ds, ip):
    servers = parse_mysql_connection_string(ds.zMySQLConnectionString)
    server = servers[ds.component.split(NAME_SPLITTER)[0]]
    db = MySQLdb.connect(
        host=ip,
        user=server['user'],
        port=server['port'],
        passwd=server['passwd'],
        connect_timeout=ds.zMySqlTimeout
    )
    db.ping(True)
    return db.cursor()


class MysqlBasePlugin(PythonDataSourcePlugin):
    '''Base plugin for MySQL monitoring tasks'''

    proxy_attributes = (
        'zMySQLConnectionString',
        'zMySqlTimeout',
        'table_count'
    )

    def get_query(self, component):
        raise NotImplemented

    def query_results_to_values(self, results):
        return {}

    def query_results_to_events(self, results, ds):
        return []

    def query_results_to_maps(self, results, component):
        return []

    def inner(self, config):
        # Data structure with empty events, values and maps.
        data = self.new_data()

        # The query execution result.
        res = None
        curs = None

        for ds in config.datasources:
            try:
                curs = connection_cursor(ds, config.manageIp)
                curs.execute(self.get_query(ds.component))
                res = curs.fetchall()
                if res:
                    data['values'][ds.component] = (
                        self.query_results_to_values(res))
                    data['events'].extend(
                        self.query_results_to_events(res, ds))
                    data['maps'].extend(
                        self.query_results_to_maps(res, ds.component))
            except Exception as e:
                # Make sure the event is sent only for MySQLServer
                # component, but not for all databases.
                if ds.component and NAME_SPLITTER in ds.component:
                    continue
                message = str(e)

                if 'MySQL server has gone away' in message or\
                    "Can't connect to MySQL server" in message:
                    message = "Can't connect to MySQL server or timeout error."

                data['events'].append({
                    'component': ds.component,
                    'summary': message,
                    'eventClass': '/Status',
                    'eventKey': 'mysql_result',
                    'severity': ds.severity,
                })

        return data

    def collect(self, config):
        return threads.deferToThread(lambda: self.inner(config))

    def onSuccess(self, result, config):
        for component in result["values"].keys():
            # Clear events for success components.
            result['events'].insert(0, {
                'component': component,
                'summary': 'Monitoring ok',
                'eventClass': '/Status',
                'eventKey': 'mysql_result',
                'severity': ZenEventClasses.Clear,
            })
        return result

    def onError(self, result, config):
        log.error(result)
        ds0 = config.datasources[0]
        data = self.new_data()
        data['events'].append({
            'summary': 'error: %s' % result,
            'eventClass': '/Status',
            'eventKey': 'mysql_result',
            'severity': ds0.severity,
        })
        return data


class MySqlMonitorPlugin(MysqlBasePlugin):
    def get_query(self, component):
        return 'show global status'

    def query_results_to_values(self, results):
        return dict((k.lower(), (v, 'N')) for k, v in results)


class MySqlDeadlockPlugin(MysqlBasePlugin):

    proxy_attributes = MysqlBasePlugin.proxy_attributes + ('deadlock_info',)

    deadlock_time = None
    deadlock_db = None
    deadlock_evt_clear_time = None

    deadlock_re = re.compile(
        '\n-+\n(LATEST DETECTED DEADLOCK\n-+\n.*?\n)-+\n',
        re.M | re.DOTALL
    )

    def _event(self, severity, summary, component):
        return {
            'severity': severity,
            'eventKey': 'innodb_deadlock',
            'eventClass': '/Status',
            'summary': summary,
            'component': component,
        }

    def get_query(self, component):
        return 'show engine innodb status'

    def query_results_to_events(self, results, ds):
        events = []

        text = results[0][2]
        deadlock_match = self.deadlock_re.search(text)
        component = ds.component

        # Clear a previous deadlock event after 30 mins.
        # Might be changed to another X minutes.
        if ds.deadlock_info and len(ds.deadlock_info) == 3:
            dl_time, dl_db, evt_clear_time = ds.deadlock_info

            if evt_clear_time and time.time() > evt_clear_time:
                events.append(self._event(ZenEventClasses.Clear, 'Ok', dl_db))
        else:
            dl_time = dl_db = evt_clear_time = None

        # Parse and process innodb status output.
        if deadlock_match:
            summary = deadlock_match.group(1)
            # Parse LATEST DETECTED DEADLOCK and find time identifier
            dtime = re.match(
                r'.+DEADLOCK\n-+\n(.+?)\n\*\*\*\s\(1\)\sTRANSACTION',
                summary
            )
            # Parse LATEST DETECTED DEADLOCK and find database name
            pattern = re.compile("`([\w]*)`\.")
            database = [''.join(pattern.findall(x)) for x in
                        summary.split('\n\n') if '*** (1) TRANSACTION:' in x]
            if database:
                component = ds.component + NAME_SPLITTER + database[0]

            if dtime:
                self.deadlock_time = dtime.group(1)

                # Create event only for new deadlock
                if dl_time != self.deadlock_time:
                    events = []
                    self.deadlock_db = component
                    # Set clear event after 30 mins.
                    self.deadlock_evt_clear_time = time.time() + 60*30
                    # Clear a previous event
                    events.append(self._event(
                        ZenEventClasses.Clear, 'Ok', dl_db))
                    # Create a new event
                    events.append(self._event(
                        ZenEventClasses.Info, summary, component))

        return events

    def query_results_to_maps(self, results, component):
        if not self.deadlock_evt_clear_time:
            return []

        return [ObjectMap({
            "compname": "mysql_servers/%s" % (component),
            "modname": "Deadlock time",
            "deadlock_info": (self.deadlock_time, self.deadlock_db,
                self.deadlock_evt_clear_time)
        })]


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
        fields = enumerate(('table_count', 'size', 'data_size', 'index_size'))
        return dict((f, (results[0][i] or 0)) for i, f in fields)


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
        ''' % adbapi_safe(component.split(NAME_SPLITTER)[-1])

    def query_results_to_values(self, results):
        fields = enumerate(('table_count', 'size', 'data_size', 'index_size'))
        return dict((f, (results[0][i] or 0)) for i, f in fields)

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
        ''' % adbapi_safe(
            component.split(NAME_SPLITTER)[-1]
        )

    def query_results_to_events(self, results, ds):
        if not results[0][0]:
            # Database does not exist, will be deleted
            db_name = ds.component.split(NAME_SPLITTER)[-1]
            return [{
                'severity': ZenEventClasses.Info,
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
