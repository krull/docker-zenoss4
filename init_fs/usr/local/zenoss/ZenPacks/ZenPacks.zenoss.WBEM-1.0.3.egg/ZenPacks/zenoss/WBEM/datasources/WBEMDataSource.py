##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

import logging
log = logging.getLogger('zen.WBEM')

import calendar

from twisted.internet import threads

from zope.component import adapts
from zope.interface import implements

from Products.ZenUtils.Utils import prepId
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.template import RRDDataSourceInfo
from Products.Zuul.interfaces import IRRDDataSourceInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSource, PythonDataSourcePlugin

from ZenPacks.zenoss.WBEM.utils import addLocalLibPath, result_errmsg

addLocalLibPath()

from pywbem.cim_operations import WBEMConnection


def string_to_lines(string):
    if isinstance(string, (list, tuple)):
        return string
    elif hasattr(string, 'splitlines'):
        return string.splitlines()

    return None


class WBEMDataSource(PythonDataSource):
    """Datasource used to capture datapoints from WBEM providers."""

    ZENPACKID = 'ZenPacks.zenoss.WBEM'

    sourcetypes = ('WBEM',)
    sourcetype = sourcetypes[0]

    plugin_classname = 'ZenPacks.zenoss.WBEM.datasources.WBEMDataSource.WBEMDataSourcePlugin'

    namespace = ''
    query_language = 'CQL'  # hard-coded for now.
    query = ''
    result_component_key = ''
    result_component_value = ''
    result_timestamp_key = ''

    _properties = PythonDataSource._properties + (
        {'id': 'namespace', 'type': 'string'},
        {'id': 'query_language', 'type': 'string'},
        {'id': 'query', 'type': 'lines'},
        {'id': 'result_component_key', 'type': 'string'},
        {'id': 'result_component_value', 'type': 'string'},
        {'id': 'result_timestamp_key', 'type': 'string'},
        )


class IWBEMDataSourceInfo(IRRDDataSourceInfo):
    cycletime = schema.TextLine(
        title=_t(u'Cycle Time (seconds)'))

    namespace = schema.TextLine(
        group=_t('WBEM'),
        title=_t('Namespace'))

    query = schema.Text(
        group=_t(u'WBEM'),
        title=_t('CQL Query'),
        xtype='twocolumntextarea')

    result_component_key = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Component Key'))

    result_component_value = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Component Value'))

    result_timestamp_key = schema.TextLine(
        group=_t(u'WBEM Results'),
        title=_t(u'Result Timestamp Key'))


class WBEMDataSourceInfo(RRDDataSourceInfo):
    implements(IWBEMDataSourceInfo)
    adapts(WBEMDataSource)

    testable = False

    cycletime = ProxyProperty('cycletime')

    namespace = ProxyProperty('namespace')
    result_component_key = ProxyProperty('result_component_key')
    result_component_value = ProxyProperty('result_component_value')
    result_timestamp_key = ProxyProperty('result_timestamp_key')

    @property
    def query(self):
        return "\n".join(self._object.query)

    @query.setter
    def query(self, val):
        self._object.query = string_to_lines(val)


class WBEMDataSourcePlugin(PythonDataSourcePlugin):
    proxy_attributes = (
        'zWBEMPort', 'zWBEMUsername', 'zWBEMPassword', 'zWBEMUseSSL',
        )

    @classmethod
    def config_key(cls, datasource, context):
        params = cls.params(datasource, context)
        return (
            context.device().id,
            datasource.getCycleTime(context),
            datasource.rrdTemplate().id,
            datasource.id,
            datasource.plugin_classname,
            params.get('namespace'),
            params.get('query_language'),
            params.get('query'),
            )

    @classmethod
    def params(cls, datasource, context):
        params = {}

        params['namespace'] = datasource.talesEval(
            datasource.namespace, context)

        params['query_language'] = datasource.query_language
        params['query'] = datasource.talesEval(
            ' '.join(string_to_lines(datasource.query)), context)

        params['result_component_key'] = datasource.talesEval(
            datasource.result_component_key, context)

        params['result_component_value'] = datasource.talesEval(
            datasource.result_component_value, context)

        params['result_timestamp_key'] = datasource.talesEval(
            datasource.result_timestamp_key, context)

        return params

    def collect(self, config):

        ds0 = config.datasources[0]

        credentials = (ds0.zWBEMUsername, ds0.zWBEMPassword)

        url = '{0}://{1}:{2}'.format(
            'https' if ds0.zWBEMUseSSL else 'http',
            ds0.manageIp, ds0.zWBEMPort
        )

        def _inner():
            return WBEMConnection(url, credentials).ExecQuery(
                ds0.params['query_language'],
                ds0.params['query'],
                namespace=ds0.params['namespace'])
        return threads.deferToThread(_inner)

    def onSuccess(self, results, config):
        data = self.new_data()

        if not isinstance(results, list):
            results = [results]

        # Convert datasources to a dictionary with result_component_value as
        # the key. This allows us to avoid an inner loop below.
        datasources = dict(
            (x.params.get('result_component_value', ''), x) \
                for x in config.datasources)

        result_component_key = \
            config.datasources[0].params['result_component_key']

        for result in results:
            if result_component_key:
                datasource = datasources.get(result[result_component_key])

                if not datasource:
                    log.debug("No datasource for result: %r", result.items())
                    continue

            else:
                datasource = config.datasources[0]

            if result_component_key and result_component_key in result:
                result_component_value = datasource.params.get(
                    'result_component_value')

                if result_component_value != result[result_component_key]:
                    continue

            component_id = prepId(datasource.component)

            # Determine the timestamp that the value was collected.
            result_timestamp_key = datasource.params.get(
                'result_timestamp_key')

            timestamp = None

            if result_timestamp_key and result_timestamp_key in result:
                cim_date = result[result_timestamp_key]
                timestamp = calendar.timegm(cim_date.datetime.utctimetuple())

            if not timestamp:
                timestamp = 'N'

            for datapoint in datasource.points:
                if datapoint.id in result:
                    data['values'][component_id][datapoint.id] = \
                        (result[datapoint.id], timestamp)

        data['events'].append({
            'eventClassKey': 'wbemCollectionSuccess',
            'eventKey': 'wbemCollection',
            'summary': 'WBEM: successful collection',
            'device': config.id,
            })

        return data

    def onError(self, result, config):
        errmsg = 'WBEM: %s' % result_errmsg(result)

        log.error('%s %s', config.id, errmsg)

        data = self.new_data()
        data['events'].append({
            'eventClassKey': 'wbemCollectionError',
            'eventKey': 'wbemCollection',
            'summary': errmsg,
            'device': config.id,
            })

        return data
