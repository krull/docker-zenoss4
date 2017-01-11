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
var ERROR_MESSAGE = "ERROR: Invalid connection string!";

/*
 * Friendly names for the components.
 */
ZC.registerName('MySQLServer', _t('MySQL Server'), _t('MySQL Servers'));
ZC.registerName('MySQLDatabase', _t('MySQL Database'), _t('MySQL Databases'));

/* Helper function to get the number of stars returned for the password */
String.prototype.repeat = function(num) {
    return new Array(isNaN(num)? 1 : ++num).join(this);
};

Ext.ns('Zenoss.form');

// Ext.version will be defined in ExtJS3 and undefined in ExtJS4
// Ext.panel throws an error in ExtJS3
if (Ext.version === undefined) {
    /*
     * @class Zenoss.form.MultilineCredentials
     * @extends Ext.panel.Panel
     * A display field that renders MySQL connection credentials as a grid
    */
    Zenoss.form.MultilineCredentials = Ext.extend(Ext.panel.Panel, {
        constructor: function (config) {
            var me = this;
            config.width = 450;
            config = Ext.applyIf(config || {}, {
                title: _t("MySQL Connection Credentials"),
                id: 'creds',
                layout: 'fit',
                listeners: {
                    afterrender: function() {
                        this.setValue(config.value);
                    },
                    scope: this
                },
                items: [ {
                    xtype: 'hidden',
                    name: config.name,
                    itemId: 'hiddenInput',
                    value: config.value
                },{
                    xtype: 'grid',
                    hideHeaders: true,
                    columns: [{
                        dataIndex: 'value',
                        flex: 1,
                        renderer: function(value) {
                            try {
                                return Ext.String.format(
                                    "{0}:{1}:{2}", value.user,
                                    "*".repeat(value.passwd.length),
                                    value.port
                                );
                            } catch (err) {
                                return ERROR_MESSAGE;
                            }
                        }
                    }],

                    store: {
                        fields: ['value'],
                        data: []
                    },

                    height: this.height || 150,
                    width: 450,

                    tbar: [{
                        itemId: 'user',
                        xtype: "textfield",
                        ref: "editConfig",
                        scope: this,
                        width: 70,
                        emptyText:'User'
                    },{
                        itemId: 'password',
                        xtype: "password",
                        ref: "editConfig",
                        scope: this,
                        width: 70,
                        emptyText:'Password',
                        value: '' //to avoid undefined value
                    },{
                        itemId: 'port',
                        xtype: "textfield",
                        ref: "editConfig",
                        scope: this,
                        width: 50,
                        emptyText:'Port',
                        value: '' //to avoid undefined value
                    },{
                        text: 'Add',
                        scope: this,
                        handler: function() {
                            var user = this.down("textfield[itemId='user']");
                            var password = this.down("textfield[itemId='password']");
                            var port = this.down("textfield[itemId='port']");

                            var grid = this.down('grid');
                            var value = {
                                'user': user.getValue(),
                                'passwd': password.getValue(),
                                'port': port.getValue()
                            };
                            if (user.value) {
                                grid.getStore().add({value: value});
                            }

                            user.setValue("");
                            password.setValue("");
                            port.setValue("");
                            this.updateHiddenField();
                        }
                    },{
                        text: "Remove",
                        itemId: 'removeButton',
                        disabled: true, // initial state
                        scope: this,
                        handler: function() {
                            var grid = this.down('grid'),
                                selModel = grid.getSelectionModel(),
                                store = grid.getStore();
                            store.remove(selModel.getSelection());
                            this.updateHiddenField();
                        }
                    }],

                    listeners: {
                        scope: this,
                        selectionchange: function(selModel, selection) {
                            var removeButton = me.down('button[itemId="removeButton"]');
                            removeButton.setDisabled(Ext.isEmpty(selection));
                        }
                    }
                }]
            });
            Zenoss.form.MultilineCredentials.superclass.constructor.apply(this, arguments);
        },

        updateHiddenField: function() {
            this.down('hidden').setValue(this.getValue());        
        },

        setValue: function(values) {
            var grid = this.down('grid');
            var data = [];
            values = Ext.JSON.decode(values, true);

            if (values) {
                Ext.each(values, function(value) {
                    data.push({value: value});
                });
            }
            grid.getStore().loadData(data);
        },

        getValue: function() {
            var grid = this.down('grid');
            var data = [];
            grid.getStore().each(function(record) {
                data.push(record.get('value'));
            });
            return JSON.stringify(data);
        }
    });
    Zenoss.zproperties.registerZPropertyType('multilinecredentials', {
        xtype: 'multilinecredentials'
    });
    Ext.reg('multilinecredentials', 'Zenoss.form.MultilineCredentials');
} else {
    // The form does not work in ExtJS3 and zenoss 4.1.1
    // Ext.reg('multilinecredentials', Zenoss.form.MultilineCredentials);
}

/* Zenoss.ConfigProperty.Grid */
/* Render zMySQLConnectionString property on the grid */
var MySQLConnectionStringRenderer = function(value) {
    var result = [];
    try {
        var val = JSON.parse(value);
        Ext.each(val, function(v) {
            result.push(
                [v.user, "*".repeat(v.passwd.length), v.port].join(':'));
        });
    } catch (err) {
        result.push('');
    }
    return result.join('; ');
};

/* Find a velue column and override a renderer for it */
var overrideRenderer = function(configpanel, columns) {
    var value_column = false;
    for (var el in columns) {
        if ((/^value/).test(columns[el].dataIndex)) {
            value_column = columns[el];
        }
    }
    if (!value_column) {
        return false;
    }
    // make backup for the existing renderer
    rend_func = value_column.renderer;
    // override renderer
    value_column.renderer = function(v, row, record) {
        // renderer for zMySQLConnectionString
        if ((record.internalId == 'zMySQLConnectionString' ||
                record.id == 'zMySQLConnectionString') &&
                record.get('value') !== "") {
            return MySQLConnectionStringRenderer(record.get('value'));
        }
        try {
            // return the default renderer vor the value
            return rend_func(v, row, record);
        } catch (err) {
            return v;
        }
    };
};

/* Override function for configpanel */
var panelOverride = function(configpanel) {
    try {
        if (Ext.version === undefined) {
            var columns = configpanel.configGrid.columns;
            overrideRenderer(configpanel, columns);
        } else {
            /* workaround for zenoss 4.1.1 */
            var columns = configpanel.items[0].colModel.columns;
            overrideRenderer(configpanel, columns);
        }
    } catch (err) {}
};

/* Zenoss.ConfigProperty.Grid override (for device) */
Ext.ComponentMgr.onAvailable('device_config_properties', function() {
    var configpanel = Ext.getCmp('device_config_properties');
    panelOverride(configpanel);
});

/* Zenoss.ConfigProperty.Grid override (for zenoss details) */
Ext.ComponentMgr.onAvailable('configuration_properties', function() {
    var configpanel = Ext.getCmp('configuration_properties');
    panelOverride(configpanel);
});

}());
