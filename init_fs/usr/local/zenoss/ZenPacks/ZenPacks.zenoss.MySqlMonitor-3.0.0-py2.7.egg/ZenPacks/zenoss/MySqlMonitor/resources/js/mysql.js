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

ZC.registerName('MySQLServer', _t('MySQL Server'), _t('MySQL Servers'));
ZC.registerName('MySQLDatabase', _t('MySQL Database'), _t('MySQL Databases'));

/* helper function to get the number of stars returned for password */
String.prototype.repeat = function(num) {
    return new Array(isNaN(num)? 1 : ++num).join(this);
}

try {
/* Zenoss.ConfigProperty.Grid override */
Ext.define("MySQL.ConfigProperty.Grid", {
    alias: ['widget.configpropertygrid'],
    extend:"Zenoss.ConfigProperty.Grid",
    constructor: function(config) {
        Ext.applyIf(config, {
            columns: [{
                header: _t("Is Local"),
                id: 'islocal',
                dataIndex: 'islocal',
                width: 60,
                sortable: true,
                filter: false,
                renderer: function(value){
                    if (value) {
                        return 'Yes';
                    }
                    return '';
                }
            },{
                id: 'category',
                dataIndex: 'category',
                header: _t('Category'),
                sortable: true
            },{
                id: 'id',
                dataIndex: 'id',
                header: _t('Name'),
                width: 200,
                sortable: true
            },{
                id: 'value',
                dataIndex: 'valueAsString',
                header: _t('Value'),
                flex: 1,
                width: 180,
                renderer: function(v, row, record) {
                    // renderer for zMySQLConnectionString
                    if (record.internalId == 'zMySQLConnectionString' &&
                        record.get('value') !== "") {
                        return this.__renderMySQLConnectionString(record.get('value'));
                    }

                    if (Zenoss.Security.doesNotHavePermission("zProperties Edit") &&
                        record.data.id == 'zSnmpCommunity') {
                        return "*******";
                    }
                    return v;
                },
                sortable: false
            },{
                id: 'path',
                dataIndex: 'path',
                header: _t('Path'),
                width: 200,
                sortable: true
            }]
        });
        this.callParent(arguments);
    },

    __renderMySQLConnectionString: function(value) {
        result = [];
        Ext.each(value, function (value) {
            try {
                var v = JSON.parse(value);
                result.push(v.user + ":" + "*".repeat(v.passwd.length) + ":" + v.port);
            } catch (err) {
                result.push("ERROR: Invalid connection string!");
            }
        })
        return result.join(';');
    }
});

/* zMySQLConnectionString property */
Zenoss.zproperties.registerZPropertyType('multilinecredentials', {xtype: 'multilinecredentials'});

Ext.define("Zenoss.form.MultilineCredentials", {
    alias:['widget.multilinecredentials'],
    extend: 'Ext.form.field.Base',
    mixins: {
        field: 'Ext.form.field.Field'
    },

    constructor: function(config) {
        config = Ext.applyIf(config || {}, {
            editable: true,
            allowBlank: true,
            submitValue: true,
            triggerAction: 'all'
        });
        config.fieldLabel = "MySQL connection credentials";
        Zenoss.form.MultilineCredentials.superclass.constructor.call(this, config);
    },

    initComponent: function() {
        this.grid = this.childComponent = Ext.create('Ext.grid.Panel', {
            hideHeaders: true,
            columns: [{
                dataIndex: 'value',
                flex: 1,
                renderer: function(value) {
                    try {
                        value = JSON.parse(value);
                        return value.user + ":" + "*".repeat(value.passwd.length) + ":" + value.port;
                    } catch (err) {
                        return "ERROR: Invalid connection string!";
                    }
                }
            }],

            store: {
                fields: ['value'],
                data: []
            },

            height: this.height || 150,
            width: 300,
            
            tbar: [{
                itemId: 'user',
                xtype: "textfield",
                scope: this,
                width: 70,
                emptyText:'User'
            },{
                itemId: 'password',
                xtype: "password",
                scope: this,
                width: 70,
                emptyText:'Password',
                value: '' //to avoid undefined value
            },{
                itemId: 'port',
                xtype: "textfield",
                scope: this,
                width: 50,
                emptyText:'Port',
                value: '' //to avoid undefined value
            },{
                text: 'Add',
                scope: this,
                handler: function() {
                    var user = this.grid.down('#user');
                    var password = this.grid.down('#password');
                    var port = this.grid.down('#port');

                    var value = {
                        'user': user.value,
                        'passwd': password.value, 
                        'port': port.value
                    };
                    if (user.value) {
                        this.grid.getStore().add({value: JSON.stringify(value)});
                    }

                    user.setValue("");
                    password.setValue("");
                    port.setValue("");

                    this.checkChange();
                }
            },{
                text: "Remove",
                itemId: 'removeButton',
                disabled: true, // initial state
                scope: this,
                handler: function() {
                    var grid = this.grid,
                        selModel = grid.getSelectionModel(),
                        store = grid.getStore();
                    store.remove(selModel.getSelection());
                    this.checkChange();
                }
            }],

            listeners: {
                scope: this,
                selectionchange: function(selModel, selection) {
                    var removeButton = this.grid.down('#removeButton');
                    removeButton.setDisabled(Ext.isEmpty(selection));
                }
            }
        });

        this.callParent(arguments);
    },

    // --- Rendering ---
    // Generates the child component markup
    getSubTplMarkup: function() {
        // generateMarkup will append to the passed empty array and return it
        var buffer = Ext.DomHelper.generateMarkup(this.childComponent.getRenderTree(), []);
        // but we want to return a single string
        return buffer.join('');
    },

    // Regular containers implements this method to call finishRender for each of their
    // child, and we need to do the same for the component to display smoothly
    finishRenderChildren: function() {
        this.callParent(arguments);
        this.childComponent.finishRender();
    },

    // --- Resizing ---
    onResize: function(w, h) {
        this.callParent(arguments);
        this.childComponent.setSize(w - this.getLabelWidth(), h);
    },

    // --- Value handling ---
    setValue: function(values) {
        var data = [];
        if (values) {
            Ext.each(values, function(value) {
                data.push({value: value});
            });
        }
        this.grid.getStore().loadData(data);
    },

    getValue: function() {
        var data = [];
        this.grid.getStore().each(function(record) {
            data.push(record.get('value'));
        });
        return data;        
    },

    getSubmitValue: function() {
        return this.getValue();
    }
});

/* workaround for zenoss 4.1.1 */
} catch (err) {

function renderMySQLConnectionString(value) {
    result = [];
    try {
        var v = JSON.parse(value);
        Ext.each(v, function (val) {
            result.push(val.user + ":" + "*".repeat(val.passwd.length) + ":" + val.port);
        })
    } catch (err) {
        result.push("ERROR: Invalid connection string!");
    }
    return result.join(';');
}
/* configPropertyPanel.js override */
var router = Zenoss.remote.DeviceRouter,
    ConfigPropertyGrid,
    ConfigPropertyPanel,
    zpropertyConfigs = {};

Ext.ns('Zenoss.zproperties');
Ext.apply(zpropertyConfigs, {
    'int': {
        xtype: 'numberfield',
        allowDecimals: false
    },
    'float': {
        xtype: 'numberfield'
    },
    'string': {
        xtype: 'textfield'
    },
    'lines': {
        xtype: 'textarea'
    },
    'severity': {
        xtype: 'severity'
    },
    'boolean': {
        xtype: 'checkbox'
    },
    'password': {
        xtype: 'password'
    },
    'options': {
        xtype: 'combo',
        editable: false,
        forceSelection: true,
        autoSelect: true,
        triggerAction: 'all',
        mode: 'local'
    },
    'zSnmpCommunity': {
        xtype: Zenoss.Security.doesNotHavePermission('Manage Device') ? 'password' : 'textfield'
    },
    'zEventSeverity': {
        xtype: 'severity'
    },
    'zFailSeverity': {
        xtype: 'severity'
    },
    'zWinEventlogMinSeverity': {
        xtype: 'reverseseverity'
    }
});

/**
 * Allow zenpack authors to register custom zproperty
 * editors.
 **/
Zenoss.zproperties.registerZPropertyType = function(id, config){
    zpropertyConfigs[id] = config;
};

function showEditConfigPropertyDialog(data, grid) {
    var handler, uid, config, editConfig, dialog, type;
    uid = grid.uid;
    type = data.type;
    // Try the specific property id, next the type and finall default to string
    editConfig = zpropertyConfigs[data.id] || zpropertyConfigs[type] || zpropertyConfigs['string'];

    // in case of drop down lists
    if (Ext.isArray(data.options) && data.options.length > 0 && type == 'string') {
        // make it a combo and the options is the store
        editConfig = zpropertyConfigs['options'];
        editConfig.store = data.options;
    }

    // set the default values common to all configs
    Ext.apply(editConfig, {
        fieldLabel: _t('Value'),
        value: data.value,
        ref: 'editConfig',
        checked: data.value,
        name: data.id
    });

    // lines come in as comma separated and should be saved as such
    if (type == 'lines' && Ext.isArray(editConfig.value)){
        editConfig.value = editConfig.value.join('\n');
    }

    handler = function() {
        // save the junk and reload
        var values = dialog.editForm.getForm().getFieldValues(),
            value = values[data.id];
        if (type == 'lines') {
            // send back as an array separated by a new line
            value = value.split('\n');
        }

        Zenoss.remote.DeviceRouter.setZenProperty({
            uid: grid.uid,
            zProperty: data.id,
            value: value
        }, function(response){
            if (response.success) {
                var view = grid.getView();
                view.updateLiveRows(
                    view.rowIndex, true, true);

            }
        });

    };

    // form config
    config = {
        submitHandler: handler,
        minHeight: 300,
        autoHeight: true,
        width: 500,
        title: _t('Edit Config Property'),
        listeners: {
            show: function() {
                dialog.editForm.editConfig.focus(true, 500);
            }
        },
        items: [{
                xtype: 'displayfield',
                name: 'name',
                fieldLabel: _t('Name'),
                value: data.id
            },{
                xtype: 'displayfield',
                name: 'path',
                ref: 'path',
                fieldLabel: _t('Path'),
                value: data.path
            },{
                xtype: 'displayfield',
                name: 'type',
                ref: 'type',
                fieldLabel: _t('Type'),
                value: data.type
            }, editConfig
        ],
        // explicitly do not allow enter to submit the dialog
        keys: {

        }
    };
    dialog = new Zenoss.SmartFormDialog(config);

    if (Zenoss.Security.hasPermission('Manage DMD')) {
        dialog.show();
    }
}

ConfigPropertyGrid = Ext.extend(Zenoss.FilterGridPanel, {
    constructor: function(config) {
        config = config || {};
        var view;
        if (!Ext.isDefined(config.displayFilters)
            || config.displayFilters
           ){
            view = new Zenoss.FilterGridView({
                rowHeight: 22,
                nearLimit: 100,
                loadMask: {msg: _t('Loading. Please wait...')}
            });
        }else {
            view = new Ext.ux.grid.livegrid.GridView({
                nearLimit: 100,
                rowHeight: 22,
                getState: function() {
                    return {};
                },
                applyState: function(state) {

                },
                loadMask: {msg: _t('Loading...'),
                      msgCls: 'x-mask-loading'}

            });
        }
        // register this control for when permissions change
        Zenoss.Security.onPermissionsChange(function() {
            this.disableButtons(Zenoss.Security.doesNotHavePermission('Manage DMD'));
        }, this);

        Ext.applyIf(config, {
            autoExpandColumn: 'value',
            stripeRows: true,
            stateId: config.id || 'config_property_grid',
            autoScroll: true,
            sm: new Zenoss.ExtraHooksSelectionModel({
                singleSelect: true
            }),
            border: false,
            tbar:[
                 {
                    xtype: 'tbtext',
                    text: _t('Configuration Properties')
                },
                '-',
                {
                xtype: 'button',
                iconCls: 'customize',
                disabled: Zenoss.Security.doesNotHavePermission('Manage DMD'),
                ref: '../customizeButton',
                handler: function(button) {
                    var grid = button.refOwner,
                        data,
                        selected = grid.getSelectionModel().getSelected();
                    if (!selected) {
                        return;
                    }
                    data = selected.data;
                    showEditConfigPropertyDialog(data, grid);
                }
                }, {
                xtype: 'button',
                iconCls: 'refresh',
                ref: '../refreshButton',
                disabled: Zenoss.Security.doesNotHavePermission('Manage DMD'),
                handler: function(button) {
                    var grid = button.refOwner;
                    var view = grid.getView();
                    view.updateLiveRows(
                        view.rowIndex, true, true);
                }
                },{
                    xtype: 'button',
                    ref: '../deleteButton',

                    text: _t('Delete Local Copy'),
                    handler: function(button) {
                        var grid = button.refOwner,
                            data,
                            selected = grid.getSelectionModel().getSelected();
                        if (!selected) {
                            return;
                        }

                        data = selected.data;
                        if (data.islocal && data.path == '/') {
                            Zenoss.message.info(_t('{0} can not be deleted from the root definition.'), data.id);
                            return;
                        }
                        if (!data.islocal){
                            Zenoss.message.info(_t('{0} is not defined locally'), data.id);
                            return;
                        }
                        Ext.Msg.show({
                        title: _t('Delete Local Property'),
                        msg: String.format(_t("Are you sure you want to delete the local copy of {0}?"), data.id),
                        buttons: Ext.Msg.OKCANCEL,
                        fn: function(btn) {
                            if (btn=="ok") {
                                if (grid.uid) {
                                    router.deleteZenProperty({
                                        uid: grid.uid,
                                        zProperty: data.id
                                    }, function(response){
                                        var view = grid.getView();
                                        view.updateLiveRows(
                                            view.rowIndex, true, true);
                                    });
                                }
                            } else {
                                Ext.Msg.hide();
                            }
                        }
                    });
                    }
                }
            ],
            store: new Ext.ux.grid.livegrid.Store({
                bufferSize: 400,
                autoLoad: true,
                defaultSort: {field: 'id', direction:'ASC'},
                sortInfo: {field: 'id', direction:'ASC'},
                proxy: new Ext.data.DirectProxy({
                    directFn: Zenoss.remote.DeviceRouter.getZenProperties
                }),
                reader: new Ext.ux.grid.livegrid.JsonReader({
                    root: 'data',
                    totalProperty: 'totalCount',
                    idProperty: 'id'
                },[
                    {name: 'id'},
                    {name: 'islocal'},
                    {name: 'value'},
                    {name: 'category'},
                    {name: 'valueAsString'},
                    {name: 'type'},
                    {name: 'path'},
                    {name: 'options'}
                ])
            }),
            cm: new Ext.grid.ColumnModel({
                columns: [{
                    header: _t("Is Local"),
                    id: 'islocal',
                    dataIndex: 'islocal',
                    width: 60,
                    sortable: true,
                    filter: false,
                    renderer: function(value){
                        if (value) {
                            return 'Yes';
                        }
                        return '';
                    }
                },{
                    id: 'category',
                    dataIndex: 'category',
                    header: _t('Category'),
                    soheader: _t("Is Local"),rtable: true
                },{
                    id: 'id',
                    dataIndex: 'id',
                    header: _t('Name'),
                    width: 200,
                    sortable: true
                },{
                    id: 'value',
                    dataIndex: 'valueAsString',
                    header: _t('Value'),
                    width: 180,
                    renderer: function(v, row, record) {
                        // renderer for zMySQLConnectionString
                        if (record.id == 'zMySQLConnectionString' &&
                            record.get('value') !== "") {
                            return renderMySQLConnectionString(record.get('value'));
                        }
                        if (Zenoss.Security.doesNotHavePermission("Manage Device") &&
                            record.data.id == 'zSnmpCommunity') {
                            return "*******";
                        }
                        return v;
                    },
                    sortable: false
                },{
                    id: 'path',
                    dataIndex: 'path',
                    header: _t('Path'),
                    width: 200,
                    sortable: true
                }]
            }),
            view: view
        });
        ConfigPropertyGrid.superclass.constructor.apply(this, arguments);
        this.on('rowdblclick', this.onRowDblClick, this);
    },

    setContext: function(uid) {
        this.uid = uid;
        // set the uid and load the grid
        var view = this.getView();
        view.contextUid  = uid;
        this.getStore().setBaseParam('uid', uid);
        this.getStore().load();
        if (uid == '/zport/dmd/Devices'){
            this.deleteButton.setDisabled(true);
        } else {
            this.deleteButton.setDisabled(Zenoss.Security.doesNotHavePermission('Manage DMD'));
        }

    },
    onRowDblClick: function(grid, rowIndex, e) {
        var data,
            selected = grid.getSelectionModel().getSelected();
        if (!selected) {
            return;
        }
        data = selected.data;
        showEditConfigPropertyDialog(data, grid);
    },
    disableButtons: function(bool) {
        this.deleteButton.setDisabled(bool);
        this.customizeButton.setDisabled(bool);
    }
});

ConfigPropertyPanel = Ext.extend(Ext.Panel, {
    constructor: function(config) {
        config = config || {};
        Ext.applyIf(config, {
            layout: 'fit',
            autoScroll: 'y',
            height: 800,
            items: [new ConfigPropertyGrid({
                ref: 'configGrid',
                displayFilters: config.displayFilters
            })]

        });
        ConfigPropertyPanel.superclass.constructor.apply(this, arguments);
    },
    setContext: function(uid) {
        this.configGrid.setContext(uid);
    }
});

Ext.reg('configpropertypanel', ConfigPropertyPanel);
}

}());
