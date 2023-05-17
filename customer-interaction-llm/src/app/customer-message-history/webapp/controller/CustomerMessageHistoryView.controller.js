sap.ui.define([ "sap/ui/core/mvc/Controller", 'sap/m/MessageBox', 'sap/ui/model/Filter', "sap/suite/ui/commons/TimelineFilterType",
				"sap/ui/model/odata/v2/ODataModel", "sap/ui/model/FilterOperator", "sap/ui/core/util/MockServer", "sap/m/MessageToast"],
	function(Controller, MessageBox, Filter, TimelineFilterType, ODataModel, FilterOperator, MockServer, MessageToast) {
	"use strict";

	var oPageController = Controller.extend("customermessagehistory.controller.CustomerMessageHistoryView", {
		onInit: function() {
			//this._initMockServer();
			//var oModel = new ODataModel("/admin", true);
			//this.getView().setModel(oModel);
			this._timeline = this.byId("idTimeline");
			
		},

		onAfterRendering: function(){
			this._initBindingEventHandler();
		},

		onPressItems : function(evt) {
			MessageToast.show("The TimelineItem is pressed.");
		},

		_initBindingEventHandler: function() {
			var oBinding = this._timeline.getBinding("content");
			this._timeline.setNoDataText("Loading");

			oBinding.attachDataReceived(function() {
				this._timeline.setNoDataText("No data");
			}, this);

			this._timeline.attachFilterSelectionChange(function(oEvent) {
				var sType = oEvent.getParameter("type"),
					bClear = oEvent.getParameter("clear");

				// if (bClear) {
				// 	this.byId("idCustomerInput").setSelectedKey("All");
				// 	this.byId("chkCustomFilter").setSelected(false);
				// 	return;
				// }

				if (sType === TimelineFilterType.Search) {
					this._search(oEvent);
				}
				if (sType === TimelineFilterType.Data) {
					this._dataFilter(oEvent);
				}
				if (sType === TimelineFilterType.Time) {
					this._timeFilter(oEvent);
				}
			}, this);
		},

		_dataFilter: function(oEvent) {
			var aItems = oEvent.getParameter("selectedItems"),
				ctrlCustomFilter = this.byId("chkCustomFilter"),
				bNancyOnly = aItems && aItems.length === 1 && aItems[0].key === "Nancy";

			ctrlCustomFilter.setSelected(bNancyOnly);
		},

		_timeFilter: function(oEvent) {
			// you can set custom filter using method 'setModelFilter'
			if (oEvent.getParameter("from") != null && oEvent.getParameter("to") != null) {
				this._timeline.setModelFilterMessage(TimelineFilterType.Time, "Custom time filter message");
			}
		},

		_search: function(oEvent) {
			var aColumns = ["customer"],
				oFilter = null,
				sSearchTerm = oEvent.getParameter("searchTerm");

			if (sSearchTerm) {
				oFilter = new Filter(aColumns.map(function(sColName) {
					return new Filter(sColName, FilterOperator.Contains, sSearchTerm);
				}));
			}

			oEvent.bPreventDefault = true;

			this._timeline.setModelFilter({
				type: "Search",
				filter: oFilter
			});
		},

		sentimentChanged: function(oEvent) {
			var sSelectedItem = oEvent.getParameter("selectedItem").getKey();
			if (sSelectedItem === "All") {
				// clear country filter
				this._timeline.setCustomFilterMessage("");
				this._timeline.setCustomModelFilter("sentimentFilter", null);
			} else {
				this._timeline.setCustomFilterMessage("Sentiment (" + sSelectedItem + ")");
				this._timeline.setCustomModelFilter("sentimentFilter", new Filter({
					path: "sentiment",
					value1: sSelectedItem,
					operator: FilterOperator.EQ
				}));
			}
		},

		customFilterChecked: function(oEvent) {
			var sSelectedItem = oEvent.getParameter("selected"),
				filter = null,
				aSelectedDataItems = [];
			if (sSelectedItem) {
				filter = new Filter({
					path: "FirstName",
					value1: "Nancy",
					operator: FilterOperator.EQ
				});

				aSelectedDataItems = ["Nancy"];
			}

			this._timeline.setModelFilter({
				type: TimelineFilterType.Data,
				filter: filter
			});
			this._timeline.setCurrentFilter(aSelectedDataItems);
		},

		onExit: function() {
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

		onSearch: function (oEvent) {
			let customer = this.byId("idCustomerInput").getValue();
			let filter = null;
			filter = new Filter({
				path: "customer",
				value1: customer,
				operator: FilterOperator.Contains,
			});

			this._timeline.setModelFilter({
				type: TimelineFilterType.Data,
				filter: filter,
			});
		}
		
	});
	return oPageController;
});