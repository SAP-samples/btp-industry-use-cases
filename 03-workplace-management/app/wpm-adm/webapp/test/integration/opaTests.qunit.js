sap.ui.require(
    [
        'sap/fe/test/JourneyRunner',
        'wpmadm/test/integration/FirstJourney',
		'wpmadm/test/integration/pages/WorkspaceList',
		'wpmadm/test/integration/pages/WorkspaceObjectPage'
    ],
    function(JourneyRunner, opaJourney, WorkspaceList, WorkspaceObjectPage) {
        'use strict';
        var JourneyRunner = new JourneyRunner({
            // start index.html in web folder
            launchUrl: sap.ui.require.toUrl('wpmadm') + '/index.html'
        });

       
        JourneyRunner.run(
            {
                pages: { 
					onTheWorkspaceList: WorkspaceList,
					onTheWorkspaceObjectPage: WorkspaceObjectPage
                }
            },
            opaJourney.run
        );
    }
);