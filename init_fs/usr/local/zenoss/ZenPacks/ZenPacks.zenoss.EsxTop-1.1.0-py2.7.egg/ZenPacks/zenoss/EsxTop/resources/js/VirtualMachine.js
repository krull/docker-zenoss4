/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2010, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


(function(){

var ZC = Ext.ns('Zenoss.component');

var ZEvActions = Zenoss.events.EventPanelToolbarActions;

ZC.VirtualMachinePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            autoExpandColumn: 'name',
            componentType: 'VirtualMachine',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{ 
                id: 'name',
                dataIndex: 'name',
                header: _t('VM Name'),
                width: 160
            }]
        });
        ZC.VirtualMachinePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('VirtualMachinePanel', ZC.VirtualMachinePanel);
ZC.registerName('VirtualMachine', _t('Virtual Machine'), _t('Virtual Machines'));

})();
