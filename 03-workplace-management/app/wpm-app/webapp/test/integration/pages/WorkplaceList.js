sap.ui.define(['sap/fe/test/ListReport'], function(ListReport) {
    'use strict';

    var CustomPageDefinitions = {
        actions: {},
        assertions: {}
    };

    return new ListReport(
        {
            appId: 'wpmapp',
            componentId: 'WorkplaceList',
            entitySet: 'Workplace'
        },
        CustomPageDefinitions
    );
});