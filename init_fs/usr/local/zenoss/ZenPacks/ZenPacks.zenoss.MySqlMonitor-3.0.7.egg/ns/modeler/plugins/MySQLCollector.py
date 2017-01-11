##############################################################################
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

''' Models discovery tree for MySQL. '''

import collections
import zope.component
from itertools import chain
from MySQLdb import cursors
from twisted.enterprise import adbapi
from twisted.internet import defer

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from Products.ZenCollector.interfaces import IEventService
from ZenPacks.zenoss.MySqlMonitor import MODULE_NAME, NAME_SPLITTER
from ZenPacks.zenoss.MySqlMonitor.modeler import queries

from ZenPacks.zenoss.MySqlMonitor.utils import parse_mysql_connection_string


class MySQLCollector(PythonPlugin):
    '''
    PythonCollector plugin for modelling device components
    '''
    is_clear_run = True
    device_om = None

    _eventService = zope.component.queryUtility(IEventService)

    deviceProperties = PythonPlugin.deviceProperties + (
        'zMySQLConnectionString',
        )

    queries = {
        'server': queries.SERVER_QUERY,
        'server_size': queries.SERVER_SIZE_QUERY,
        'master': queries.MASTER_QUERY,
        'slave': queries.SLAVE_QUERY,
        'db': queries.DB_QUERY,
        'version': queries.VERSION_QUERY
    }

    @defer.inlineCallbacks
    def collect(self, device, log):
        log.info("Collecting data for device %s", device.id)
        try:
            servers = parse_mysql_connection_string(
                device.zMySQLConnectionString)
        except ValueError, error:
            self.is_clear_run = False
            log.error(error.message)
            self._send_event(error.message, device.id, 5)
            defer.returnValue('Error')
            return

        result = []
        for el in servers.values():
            dbpool = adbapi.ConnectionPool(
                "MySQLdb",
                user=el.get("user"),
                port=el.get("port"),
                host=device.manageIp,
                passwd=el.get("passwd"),
                cursorclass=cursors.DictCursor
            )

            res = {}
            res["id"] = "{0}_{1}".format(el.get("user"), el.get("port"))
            for key, query in self.queries.iteritems():
                try:
                    res[key] = yield dbpool.runQuery(query)
                except Exception, e:
                    self.is_clear_run = False
                    res[key] = ()
                    msg, severity = self._error(
                        str(e), el.get("user"), el.get("port"))

                    log.error(msg)

                    if severity == 5:
                        self._send_event(msg, device.id, severity)
                        dbpool.close()
                        defer.returnValue('Error')
                        return

            dbpool.close()
            result.append(res)

        defer.returnValue(result)

    def process(self, device, results, log):
        log.info(
            'Modeler %s processing data for device %s',
            self.name(), device.id
        )

        # 4.2.3 event sending
        if self.device_om:
            return self.device_om

        # 4.2.4 workaround
        if results == 'Error':
            return

        maps = collections.OrderedDict([
            ('servers', []),
            ('databases', []),
            ('device', []),
        ])

        # List of servers
        server_oms = []
        for server in results:
            s_om = ObjectMap(server.get("server_size")[0])
            s_om.id = self.prepId(server["id"])
            s_om.title = server["id"]
            s_om.percent_full_table_scans = self._table_scans(
                server.get('server', ''))
            s_om.master_status = self._master_status(server.get('master', ''))
            s_om.slave_status = self._slave_status(server.get('slave', ''))
            s_om.version = self._version(server.get('version', ''))
            server_oms.append(s_om)

            # List of databases
            db_oms = []
            for db in server['db']:
                d_om = ObjectMap(db)
                d_om.id = s_om.id + NAME_SPLITTER + self.prepId(db['title'])
                db_oms.append(d_om)

            maps['databases'].append(RelationshipMap(
                compname='mysql_servers/%s' % s_om.id,
                relname='databases',
                modname=MODULE_NAME['MySQLDatabase'],
                objmaps=db_oms))

        maps['servers'].append(RelationshipMap(
            relname='mysql_servers',
            modname=MODULE_NAME['MySQLServer'],
            objmaps=server_oms))

        log.info(
            'Modeler %s finished processing data for device %s',
            self.name(), device.id
        )
        if self.is_clear_run:
            self._send_event("clear", device.id, 0, True)
            if self.device_om:
                maps['device'] = [self.device_om]

        return list(chain.from_iterable(maps.itervalues()))

    def _error(self, error, user, port):
        """
        Create an error messsage for event.

        @param error: mysql error
        @type error: string
        @param user: user
        @type user: string
        @param port: port
        @type port: string
        @return: message and severity for event
        @rtype: str, int
        """

        if "privilege" in error:
            msg = ("The user '%s' needs (at least one of) the SUPER, "
                   "REPLICATION CLIENT privilege(s) to retrieve MySQL "
                   "Replication data" % user)
            severity = 4
        elif "Access denied" in error:
            msg = "Access denied for user '%s:***:%s'" % (user, port)
            severity = 5
        elif "Can't connect" in error:
            msg = ("Can't connect to MySQL server. Check permissions for "
                "remote connections for %s:***:%s" % (user, port))
            severity = 5
        else:
            msg = "Error modeling MySQL server for %s:***:%s" % (user, port)
            severity = 5

        return msg, severity

    def _version(self, version_result):
        """
        Return the version of MySQL server.

        @param version_result: result of VERSION_QUERY
        @type version_result: string
        @return: the server version with machine version
        @rtype: str
        """

        result = dict((el['Variable_name'], el['Value'])
                      for el in version_result)

        return "{0} {1} ({2})".format(
            result['version'],
            result['version_comment'],
            result['version_compile_machine']
        )

    def _table_scans(self, server_result):
        """
        Calculate the percent of full table scans for server.

        @param server_result: result of SERVER_QUERY
        @type server_result: string
        @return: rounded value with percent sign
        @rtype: str
        """

        r = dict((el['Variable_name'], el['Value'])
                 for el in server_result)

        if int(r['Handler_read_key']) == 0:
            return "N/A"

        # percent = float(result['Handler_read_first']) /\
        #    float(result['Handler_read_key'])
        # 1 - (handler_read_rnd_next + handler_read_rnd) /
        # (handler_read_rnd_next + handler_read_rnd + handler_read_first +
        # handler_read_next + handler_read_key + handler_read_prev )
        percent = 1 - (
            float(r['Handler_read_rnd_next']) +
            float(r['Handler_read_rnd'])) / (
            float(r['Handler_read_rnd_next']) + float(r['Handler_read_rnd']) +
            float(r['Handler_read_first']) + float(r['Handler_read_next']) +
            float(r['Handler_read_key']) + float(r['Handler_read_prev'])
        )

        return str(round(percent, 3)*100)+'%'

    def _master_status(self, master_result):
        """
        Parse the result of MASTER_QUERY.

        @param master_result: result of MASTER_QUERY
        @type master_result: string
        @return: master status
        @rtype: str
        """

        if master_result:
            master = master_result[0]
            return "ON; File: %s; Position: %s" % (
                master['File'], master['Position'])
        else:
            return "OFF"

    def _slave_status(self, slave_result):
        """
        Parse the result of SLAVE_QUERY.

        @param master_result: result of SLAVE_QUERY
        @type master_result: string
        @return: slave status
        @rtype: str
        """

        if slave_result:
            slave = slave_result[0]
            return "IO running: %s; SQL running: %s; Seconds behind: %s" % (
                slave['Slave_IO_Running'], slave['Slave_SQL_Running'],
                slave['Seconds_Behind_Master'])
        else:
            return "OFF"

    def _send_event(self, reason, id, severity, force=False):
        """
        Send event for device with specified id, severity and
        error message.
        """

        if self._eventService:
            self._eventService.sendEvent(dict(
                summary=reason,
                eventClass='/Status',
                device=id,
                eventKey='ConnectionError',
                severity=severity,
                ))
            return True
        else:
            if force or (severity > 0):
                self.device_om = ObjectMap({
                    'setErrorNotification': reason
                })
