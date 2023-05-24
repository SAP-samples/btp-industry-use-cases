sap.ui.define(['sap/fe/test/ListReport'], function(ListReport) {
    'use strict';

    var CustomPageDefinitions = {
        actions: {},
        assertions: {}
    };

    return new ListReport(
        {
            appId: 'fdt.app.fdtapp',
            componentId: 'EmployeeList',
            entitySet: 'Employee'
        },
        CustomPageDefinitions
    );
});