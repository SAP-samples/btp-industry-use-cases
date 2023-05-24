sap.ui.define(["sap/m/MessageBox",
	"sap/ui/model/Filter",
	"sap/ui/model/FilterOperator",
	"sap/suite/ui/commons/TimelineFilterType", 
	"sap/ui/model/odata/v4/ODataModel", 
	"sap/ui/model/json/JSONModel",
	"sap/suite/ui/commons/TimelineItem"],
	function (MessageBox, Filter, FilterOperator, TimelineFilterType, ODataModel, JSONModel, TimelineItem) {
		"use strict";

		return {
			formatDecToPercentage: function (val) {
				//  return val * 100;
				//  removed this as value is as per percentage
				return val;
			},
			formatDecToPercentageDiscount: function (val) {
				return -val * 100;
			},

			directionIcon: function (sDirection) {
				switch (sDirection) {
				  case "Inbound":
					return "sap-icon://travel-request";
				  case "Outbound":
					return "sap-icon://response";
				  default:
					return "sap-icon://machine";
				}
			},

			userIcon: function (sDirection) {
				switch (sDirection) {
				  case "Virtual Assistant":
					return "sap-icon://feedback";
				  default:
					return "sap-icon://user";
				}
			},

			sentimentColour: function (sStatus) {
				switch (sStatus) {
				  case "Positive":
					return "Success";
				  case "N/A":
					return "Warning";	// Warning
				  case "Negative":
					return "Error";
				  default:
					return "";
				}
			},

			onReset: function (oEvent) {
				// MessageBox.alert("pressed");
				var y = sap.ui.getCore().byId("customerinteraction::CustomerInteractionObjectPage--fe::CustomSubSection::CustomMessageTimeline--msInteractionSelection").getText();
				// console.log("test");
				console.log(y);

				// sap.ui.getCore().byId("customerinteraction::CustomerInteractionObjectPage--fe::CustomSubSection::CustomMessageTimeline--msInteractionSelection").setText("asd");

				var x = sap.ui.getCore().byId("customerinteraction::CustomerInteractionObjectPage--fe::CustomSubSection::CustomMessageTimeline--idTimeline");
				console.log(x);
				console.log(x.getContent());
				console.log(x.getAggregation());	// null
				console.log(x.getCurrentFilter());	// nothing
				console.log(x.getCustomFilter());	// null
				console.log(x.getFilterList());		// nothing

				// location.reload();
				// x.reset();
				// x.destroyFilterList();
				// console.log(x.getFilterList());

				var filter = null;
				filter = new Filter({
					path: "interactionID",
					value1: y,
					operator: FilterOperator.EQ,
				});

				x.setModelFilter({
					type: TimelineFilterType.Data,
					filter: filter,
				});

				// x.setCustomModelFilter(
				// 	"statusFilter",
				// 	new Filter({
				// 		path: "interactionID",
				// 		value1: y,
				// 		operator: FilterOperator.EQ,
				// 	})
				// );

				// test - odata binding approach - sync broken
				// var oModel = new ODataModel("http://services.odata.org/V3/Northwind/Northwind.svc/", true);
				// var oModel = new ODataModel("/admin/", true);
				
				// var oModel = new JSONModel(
				// 	"/admin/PlantConditions?$top=3000&$orderby=ID%20desc&$select=ID,plantStatus,recStartedAt,recEndedAt,date,shift,yield,defectiveProd,energyCons"
				//   );
				// var oModel = new JSONModel("/admin/", true);
				// var oItem = new TimelineItem({
				// 	// dateTime: "{createdAt}",
				// 	title: "{summary}",
				// 	text: "{message}",
				// 	userName: "{name}"
				// });
				// x.bindAggregation("content", {
				// 	path: "/MessageThread",
				// 	template: oItem
				// });
				// x.setModel(oModel);

				// no binding approach - works
				// x.setContent([new TimelineItem({
				// 	dateTime: new Date(2016, 1, 1),
				// 	icon: "sap-icon://accept",
				// 	title: "Title 1",
				// 	text: "Some comment"
				// }),
				// new TimelineItem({
				// 	dateTime: new Date(2015, 2, 2),
				// 	icon: "sap-icon://decline",
				// 	title: "Title 2",
				// 	text: "Some comment"
				// })]);


			}
		};
	});
