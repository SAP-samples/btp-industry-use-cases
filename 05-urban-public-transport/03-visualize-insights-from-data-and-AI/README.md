# Overview

In every end-to-end solution visualization is crucial to consume data, get insights and support decision making. In our use case the data we acquired and we prepared can be used already to build several types of dashboards targeting different personas. In particular a monitoring dashboard for the bus service in the city of London and a simple anomaly detection tool can be immediately developed on top of this data.

There are many possibilities for developing the front-end of a solution like the one we propose, anyway we are considering as first option SAP Analytics Cloud, the most user-friendly one that allows already to create appealing and interactive dashboards without requiring extensive technical expertise.

Here we provide the story we built in SAC for the Urban Public Transport use case in the form of a [".package" file](./sap-analytics-cloud/stories) that can be imported in your SAC instance in order to reproduce what we developed. NB: it is not guaranteed the file can be imported (for example because of version incompatibilities) and that all the objects will be able to work, they might need some adjustments.


## Prerequisites

- SAP Analytics Cloud (consult the [Discovery Center](https://discovery-center.cloud.sap/viewServices?category=freetierservices))
- The analytic models described [here](../02-data-harmonization-and-modeling/README.md)
- A live connection to Datasphere (see [here](https://help.sap.com/docs/SAP_ANALYTICS_CLOUD/00f68c2e08b941f081002fd3691d86a7/ad4281e2875949f0b4d45d1072ff4c38.html?locale=en-US))


## Brief description of the export content

The exported story contains the following pages:

1. **Location Monitoring:** A geo map widget showing the real-time position and speed of the buses in the city of London. It displays also the bus stops and road disruptions information.
2. **Speed Monitoring:** A page for a deeper analysis of the status and speed of the buses serving in the city of London.
3. **Speed Analysis:** Charts diplaying the buses average speed versus day hour and week day. 
4. **Events from Social Media:** A page showing how the data ingested and processed from social media can be used to get a global picture of the on-going events in the city.
5. **Road Disruptions:** Details about the current or planned road disruptions in the city of London.
6. **Vehicle Information:** Information about the fleet: masterdata and planned maintenance interventions.
7. **Timetables:**: A page showing the timetables of the bus services in the city of London as reconstructed from the acquired GTFS feeds.


## How to import the .package file

1. Download the [".package" file](./sap-analytics-cloud/stories) from this GitHub repository;
2. Go to "Transport" at the bottom left and click on "Export" and then on "My Content";
   
  <img width="1662" alt="Screenshot 2023-08-24 at 10 12 38" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/0ce18983-71c9-4537-bd3d-de4d286434a0">

3. Load the .package file by clicking on the "Load" button and selecting the file from your local disk;

  <img width="1661" alt="Screenshot 2023-08-24 at 10 12 58" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/7c7f3488-1ffc-4cf6-a653-5206801388e9">

4. Go to Transport/Import. In My Content it will appear the content you uploaded (refresh if it does not), click on it;
   
  <img width="1657" alt="Screenshot 2023-08-24 at 10 13 54" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/362d8008-faf1-48e0-b1c9-a20b7e7a3e45">

5. In the "Import options" select the options that apply and all the objects, then click on Import.


## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
