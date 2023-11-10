# Overview

Here you can find the material to reproduce what we developed for ingesting the data for our use case: 
- the JSON files of the Data Intelligence pipelines
- the python scripts, in case you want to run them elsewhere


## Prerequisites
- SAP Data Intelligence
- SAP Datasphere (or a SAP HANA Cloud DB instance) and a SAP HANA Cloud Data Lake (consult the [Discovery Center](https://discovery-center.cloud.sap/viewServices?category=freetierservices))
- An account on the [UK Bus Open Data Service](https://www.bus-data.dft.gov.uk/) and the [TFL API service](https://api-portal.tfl.gov.uk/)
- Connections from Data Intelligence to [Datasphere](https://developers.sap.com/tutorials/data-warehouse-cloud-bi3-connect-dic.html) and [HDL](https://developers.sap.com/tutorials/hana-cloud-connection-guide-4.html)
- a DB user set in Datasphere (see [02-data-harmonization-and-modeling](../02-data-harmonization-and-modeling/README.md))

## Brief description of the pipelines

- **load_gtfs_rt_to_datasphere**
  
This pipeline is used to get data about the bus location in the city of London and it is based on a custom Python operator. In the figure below you can see the pipeline workflow.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-6-2.png" alt="drawing" width="700"/>
</p>

The pipeline starts retrieving the previous locations of all the buses from a technical table in the underlying HANA DB in Datasphere, this will be needed later for the average speed calculation. After that, we execute a new call to the API exposed by the UK Government to get the current bus locations. In the third step we transform and prepare the acquired data, and finally we proceed with the average bus speed calculation, and we save all the enriched data into a specific table created in the underlying HANA DB in Datasphere.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-3-2.png" alt="drawing" width="700"/>
</p>


- **load_gtfs_to_datasphere**

This pipeline takes care of retrieving the GTFS feeds from the UK Bus Open Data Service page and the road disruptions in the city of London by means of specific API provided by TFL. It is based again on a Python operator.

The first step of the pipeline downloads the GTFS feeds provided as a zipped file, it does decompress it and use the resulting cvs files are used to populate the entities representing all the transit information in the Datasphere underlying HANA DB.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Screenshot-2023-07-19-at-10.24.37.png" alt="drawing" width="500"/>
</p>

The second step of the pipeline is responsible of the ingestion of the London road disruptions. In this case the Python operator executes the following operations: it executes an API call to the API exposed by Transport for London, after that it prepares the data and in the last step it saves the data into a specific HANA DB table in Datasphere.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-4-1.png" alt="drawing" width="500"/>
</p>

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-7-1.png" alt="drawing" width="700"/>
</p>


- **move_gtfs_rt_to_datalake**

This pipeline is meant to perform some data tiering in HANA Cloud, in particular it is designed to move the vehicle acitvity data from the Datasphere underlying HANA DB to the HANA Cloud Data Lake. The pipeline is built with Data Intelligence standard operators (see [here](https://blogs.sap.com/2021/03/23/overview-of-sap-hana-operators-in-sap-data-intelligence/) for more details).

The figure below shows an example of how the pipeline looks like. We have several steps: in the first step we load the data we want to move from the HANA DB table. Then we write the data into a table with the same structure into the Data Lake. We take note of the timestamp of the data we have already moved into a HANA DB technical table and finally we make use of that timetable to delete the moved records in the HANA DB table.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-13-1.png" alt="drawing" width="700"/>
</p>


- **clean_datalake**

This pipeline is a maintenance pipeline and it is used to easily clean what is stored in the vehicle activity table created in the HANA Cloud Data Lake. It is made with Data Intelligence standard operators.


## How to create the pipelines in Data Intelligence

Below you can find some summary instructions on how to import the pipelines described above into your Data Intelligence instance. NB: it is possible that the pipes need to be adjusted due to the change of the DI version or the version of the operators.

1. Create a ML Scenario to manage all the pipelines related to this use case.
   <img width="1634" alt="Screenshot 2023-08-23 at 12 34 35" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/76f6b74f-a5c8-4dca-b02a-b70f81e17de8">

2. Create a new Blank pipeline.
   <img width="1622" alt="Screenshot 2023-08-23 at 12 37 30" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/804f3c58-8e40-4438-8167-4916c09df6c0">

3. Open the new pipeline in the modeler and click on the JSON button at the top right corner of the window. In the editor enter one of the JSON files provided, then go back to the diagram by clicking on the Diagram button.
   <img width="1661" alt="Screenshot 2023-08-23 at 12 39 20" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/417ad6de-98ad-4283-98f3-5e6857a22c34">

4. Save the pipeline and test it.


## How to schedule the pipeline execution in Data Intelligence

1. Click on the Monitoring tile available in the Data Intelligence launchpad.
   <img width="1582" alt="Screenshot 2023-08-23 at 12 41 39" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/75c17c04-dbfb-4b30-a64f-77673ca27d72">

2. Click on the Schedules button at the top left corner of the window and then click on the + button to create a new scheduling. Fill the needed information and click Create.
   <img width="1606" alt="Screenshot 2023-08-23 at 12 43 07" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/3fe45e3f-20f1-4869-8b5f-c95f9ea57db5">
   <img width="1627" alt="Screenshot 2023-08-23 at 12 43 25" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/fcf11d8f-bad1-47b5-98e0-f877f2f8d447">
   <img width="1636" alt="Screenshot 2023-08-23 at 12 43 37" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/c71b2927-424c-4267-a39b-376bc6f307fb">

3. From the instances tab you can monitor the executions of the pipeline you have scheduled and access to the information about the executions.
   <img width="1623" alt="Screenshot 2023-08-23 at 12 43 55" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/c736e4a1-c0df-4d16-a3e6-80be9ec3cdf2">


## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
