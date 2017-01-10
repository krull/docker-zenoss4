def get_monitoring_template(graphs):
    xml = []
    xml.append('''
    <property id="targetPythonClass" mode="w" type="string">
      Products.ZenModel.Device
    </property>
    <tomanycont id="datasources">
      <object class="PythonDataSource" id="MyDataSources"
        module="ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource">
        <property id="sourcetype" mode="w"
        select_variable="sourcetypes" type="selection">
          Python
        </property>
        <property id="enabled" mode="w" type="boolean">
          True
        </property>
        <property id="component" mode="w" type="string">
          ${here/id}
        </property>
        <property id="eventClass" mode="w" type="string">
          /Status
        </property>
        <property id="severity" mode="w" type="int">
          3
        </property>
        <property id="cycletime" mode="w" type="string">
          300
        </property>
        <property id="plugin_classname" mode="w" type="string">
          ZenPacks.zenoss.MySqlMonitor.dsplugins.MySqlMonitorPlugin
        </property>
        <tomanycont id="datapoints">
    ''')
    for graph in graphs:
        for datapoint in graph[1]:
            xml.append('''
          <object class="RRDDataPoint" id="{datapoint}"
            module="Products.ZenModel.RRDDataPoint">
            <property id="rrdtype" mode="w"
            select_variable="rrdtypes" type="selection">
              GAUGE
            </property>
            <property id="isrow" mode="w" type="boolean">
              True
            </property>
          </object>
            '''.format(datapoint=get_id(datapoint)))
    xml.append('''
        </tomanycont>

      </object>
    </tomanycont>
    <tomanycont id="graphDefs">
    ''')
    for graph in graphs:
        xml.append('''
      <object class="GraphDefinition" id="{graph_id}"
        module="Products.ZenModel.GraphDefinition">
        <property id="height" mode="w" type="int">
          100
        </property>
        <property id="width" mode="w" type="int">
          500
        </property>
        <property id="log" mode="w" type="boolean">
          False
        </property>
        <property id="base" mode="w" type="boolean">
          False
        </property>
        <property id="miny" mode="w" type="int">
          -1
        </property>
        <property id="maxy" mode="w" type="int">
          -1
        </property>
        <property id="hasSummary" mode="w" type="boolean">
          True
        </property>
        <property id="sequence" mode="w" type="long">
          0
        </property>
        <tomanycont id="graphPoints">
        '''.format(graph_id=graph[0]))
        for datapoint in graph[1]:
            xml.append('''
          <object class="DataPointGraphPoint" id="{datapoint}"
            module="Products.ZenModel.DataPointGraphPoint">
            <property id="sequence" mode="w" type="long">
              1
            </property>
            <property id="lineType" mode="w"
            select_variable="lineTypes" type="selection">
              LINE
            </property>
            <property id="lineWidth" mode="w" type="long">
              1
            </property>
            <property id="stacked" mode="w" type="boolean">
              False
            </property>
            <property id="format" mode="w" type="string">
              %5.2lf%s
            </property>
            <property id="legend" mode="w" type="string">
              {legend}
            </property>
            <property id="limit" mode="w" type="long">
              -1
            </property>
            <property id="dpName" mode="w" type="string">
              MySQL_{datapoint}
            </property>
            <property id="cFunc" mode="w" type="string">
              AVERAGE
            </property>
          </object>
            '''.format(datapoint=get_id(datapoint), legend=datapoint))
        xml.append('''
        </tomanycont>
      </object>
        ''')
    xml.append('''
    </tomanycont>
    ''')
    return ''.join(xml)


def get_id(datapoint):
    return datapoint.lower().replace(' ', '_')

print get_monitoring_template((
    ('Connections', (
        'Threads connected',
    )),
    ('Aborted', (
        'Aborted clients',
        'Aborted connects'
    )),
    ('Bytes', (
        'Bytes sent',
        'Bytes received',
    )),
    ('Commands', (
        'Com alter db',
        'Com alter table',
        'Com call procedure',
        'Com check',
        'Com commit',
        'Com create db',
        'Com create table',
        'Com create user',
        'Com delete multi',
        'Com delete',
        'Com drop db',
        'Com drop table',
        'Com drop user',
        'Com execute sql',
        'Com flush',
        'Com insert select',
        'Com insert',
        'Com purge',
        'Com repair',
        'Com replace',
        'Com rollback',
        'Com select',
        'Com update multi',
        'Com update',
    )),
    ('Handler', (
        'Handler commit',
        'Handler delete',
        'Handler rollback',
        'Handler update',
        'Handler write',
        'Handler read first',
        'Handler read key',
        'Handler read last',
        'Handler read next',
        'Handler read prev',
        'Handler read rnd',
        'Handler read rnd next',
        'Handler savepoint',
    )),
    ('Key cache', (
        'Key reads',
        'Key writes',
        'Key read requests',
    )),
    ('Open objects', (
        'Open files',
        'Open streams',
        'Open tables',
    )),
    ('Joins stats', (
        'Select full join',
        'Select full range join',
        'Select range',
        'Select range check',
        'Select scan',
    )),
))
