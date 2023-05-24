sap.ui.require(
    [
        'sap/fe/test/JourneyRunner',
        'wpmapp/test/integration/FirstJourney',
		'wpmapp/test/integration/pages/WorkplaceList',
		'wpmapp/test/integration/pages/WorkplaceObjectPage'
    ],
    function(JourneyRunner, opaJourney, WorkplaceList, WorkplaceObjectPage) {
        'use strict';
        var JourneyRunner = new JourneyRunner({
            // start index.html in web folder
            launchUrl: sap.ui.require.toUrl('wpmapp') + '/index.html'
        });

       
        JourneyRunner.run(
            {
                pages: { 
					onTheWorkplaceList: WorkplaceList,
					onTheWorkplaceObjectPage: WorkplaceObjectPage
                }
            },
            opaJourney.run
        );
    }
);