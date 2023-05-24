sap.ui.require(
    [
        'sap/fe/test/JourneyRunner',
        'fdt/app/fdtapp/test/integration/FirstJourney',
		'fdt/app/fdtapp/test/integration/pages/EmployeeList',
		'fdt/app/fdtapp/test/integration/pages/EmployeeObjectPage',
		'fdt/app/fdtapp/test/integration/pages/DriveHistoryObjectPage'
    ],
    function(JourneyRunner, opaJourney, EmployeeList, EmployeeObjectPage, DriveHistoryObjectPage) {
        'use strict';
        var JourneyRunner = new JourneyRunner({
            // start index.html in web folder
            launchUrl: sap.ui.require.toUrl('fdt/app/fdtapp') + '/index.html'
        });

       
        JourneyRunner.run(
            {
                pages: { 
					onTheEmployeeList: EmployeeList,
					onTheEmployeeObjectPage: EmployeeObjectPage,
					onTheDriveHistoryObjectPage: DriveHistoryObjectPage
                }
            },
            opaJourney.run
        );
    }
);