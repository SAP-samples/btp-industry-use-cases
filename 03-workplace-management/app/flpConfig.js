window["sap-ushell-config"] = {
	defaultRenderer: "fiori2",
	bootstrapPlugins: {
		KeyUserPlugin: {
			component: "sap.ushell.plugins.rta",
		},
		PersonalizePlugin: {
			component: "sap.ushell.plugins.rta-personalize",
		}
	},
	applications: {
		"workplace-display": {
			title: "Workplace Management",
			description: "Manage Bookings",
			icon: "sap-icon://add",
			additionalInformation: "SAPUI5.Component=com.alteaup.solutions.accessrights",
			applicationType: "URL",
			url: "./wpm-app/webapp",
			navigationMode: "embedded",
		},
		"workspace-display": {
			title: "Facilities Management",
			description: "Manage Workspaces",
			icon: "sap-icon://add",
			additionalInformation: "SAPUI5.Component=com.alteaup.solutions.accessrights",
			applicationType: "URL",
			url: "./wpm-adm/webapp",
			navigationMode: "embedded",
		}
	}
};