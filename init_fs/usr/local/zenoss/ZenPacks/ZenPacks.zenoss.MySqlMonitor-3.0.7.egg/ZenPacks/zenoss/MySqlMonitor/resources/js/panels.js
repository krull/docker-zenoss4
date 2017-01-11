/*****************************************************************************
 *
 * Copyright (C) Zenoss, Inc. 2013, all rights reserved.
 *
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 *
 ****************************************************************************/

(function(){

var ZC = Ext.ns('Zenoss.component');
var ZD = Ext.ns('Zenoss.devices');

/* pingStatus renderer override */
var upDownTemplate = new Ext.Template(
    '<span class="status-{0}{2}">{1}</span>');
upDownTemplate.compile();

Ext.apply(Zenoss.render, {
    linkFromSubgrid: function(value, metaData, record) {
        if (this.subComponentGridPanel) {
            return Zenoss.render.link(record.data.uid, null, value);
        } else {
            return value;
        }
    }
});

/* MySQLServer */
ZC.MySQLServerPanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'MySQLServer',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'status'},
                {name: 'locking'},
                {name: 'db_count'},
                {name: 'size'},
                {name: 'data_size'},
                {name: 'index_size'},
                {name: 'percent_full_table_scans'},
                {name: 'slave_status'},
                {name: 'master_status'},
                {name: 'version'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
            },{
                id: 'version',
                dataIndex: 'version',
                header: _t('Version'),
            },{
                id: 'db_count',
                dataIndex: 'db_count',
                header: _t('Number of databases'),
                width: 120
            },{
                id: 'percent_full_table_scans',
                dataIndex: 'percent_full_table_scans',
                header: _t('Percentage of full table scans'),
                width: 150
            },{
                id: 'slave_status',
                dataIndex: 'slave_status',
                header: _t('Slave status'),
            },{
                id: 'master_status',
                dataIndex: 'master_status',
                header: _t('Master status'),
            // },{
            //     id: 'size',
            //     dataIndex: 'size',
            //     header: _t('Size'),
            //     width: 65
            // },{
            //     id: 'data_size',
            //     dataIndex: 'data_size',
            //     header: _t('Data size'),
            //     width: 65
            // },{
            //     id: 'index_size',
            //     dataIndex: 'index_size',
            //     header: _t('Index size'),
            //     width: 65
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus,
                width: 65
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 60
            }]
        });
        ZC.MySQLServerPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('MySQLServerPanel', ZC.MySQLServerPanel);

/* MySQLDatabase */
ZC.MySQLDatabasePanel = Ext.extend(ZC.ComponentGridPanel, {
    subComponentGridPanel: false,

    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'MySQLDatabase',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'status'},
                {name: 'locking'},
                {name: 'size'},
                {name: 'server'},
                {name: 'data_size'},
                {name: 'index_size'},
                {name: 'table_count'},
                {name: 'default_character_set_name'},
                {name: 'default_collation_name'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                renderer: Zenoss.render.linkFromSubgrid,
            },{
                id: 'server',
                dataIndex: 'server',
                header: _t('Server'),
                renderer: Zenoss.render.linkFromGrid,
            },{
                id: 'table_count',
                dataIndex: 'table_count',
                header: _t('Number of tables'),
            },{
                id: 'default_character_set_name',
                dataIndex: 'default_character_set_name',
                header: _t('Default character set'),
                width: 120
            },{
                id: 'default_collation_name',
                dataIndex: 'default_collation_name',
                header: _t('Default collation'),
            // },{
            //     id: 'size',
            //     dataIndex: 'size',
            //     header: _t('Size'),
            //     width: 65
            // },{
            //     id: 'data_size',
            //     dataIndex: 'data_size',
            //     header: _t('Data size'),
            //     width: 65
            // },{
            //     id: 'index_size',
            //     dataIndex: 'index_size',
            //     header: _t('Index size'),
            //     width: 65
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus,
                width: 65
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 60
            }]
        });
        ZC.MySQLDatabasePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('MySQLDatabasePanel', ZC.MySQLDatabasePanel);


/* Subcomponent Panels */
/* MySQLDatabase */
Zenoss.nav.appendTo('Component', [{
    id: 'databases',
    text: _t('Databases'),
    xtype: 'MySQLDatabasePanel',
    subComponentGridPanel: true,
    filterNav: function(navpanel) {
         switch (navpanel.refOwner.componentType) {
            case 'MySQLServer': return true;
            default: return false;
         }
    },
    setContext: function(uid) {
        ZC.MySQLDatabasePanel.superclass.setContext.apply(this, [uid]);
    }
}]);

})();
