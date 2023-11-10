# Overview

We have used the SAP Data Intelligence for the data ingestion and orchestration (see [01-data-ingestion-and-orchestration](../01-data-ingestion-and-orchestration)). To  harmonize and model the acquired data, we have used SAP Datasphere which is a comprehensive data service responsible for Data Warehousing in BTP. We used it to build comprehensive views to be consumed in the front-end for specific analytics purposes (for example, to provide a global picture of London bus the service performance in real-time).

To this end, we have exploited the Datasphere integration capabilities (for instance the virtual access to remote table or remote table federation) and the possibility to bring in data by means of external data movement tools (in our case Data Intelligence). Moreover we have integrated, enriched, transformed and modeled the data in Datasphere through graphical views, SQL views and analytic models.

<p align="center">
<img src="https://blogs.sap.com/wp-content/uploads/2023/07/Picture-19-1.png" alt="drawing" width="700"/>
</p>

Here we provide all the objects created in Datasphere for the Urban Public Transport use case in the form of a [".package" file](./sap-datasphere) that can be imported in your Datasphere instance in order to reproduce what we developed. NB: it is not guaranteed the file can be imported (for example because of version incompatibilities) and that all the objects will be able to work (see the list of prerequisites below). The .package file contains:

- the space folder (named URBANPUBLICTRANSPORT);
- the remote tables definitions (from SAP Digital Vehicle Hub and the HANA Cloud Data Lake);
- the local tables definitions (created by Data Intelligence or target tables of the views);
- the graphical and SQL views;
- the analytic models.


## Prerequisites

- SAP Datasphere and a SAP HANA Cloud Data Lake (consult the [Discovery Center](https://discovery-center.cloud.sap/viewServices?category=freetierservices))
- Connection from Datasphere to the [HANA Cloud Data Lake](https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/40763e2e3e33440db0c37f6bcbe650f0.html?locale=en-US&q=export)
- a DB user set in Datasphere (see [here](https://developers.sap.com/tutorials/data-warehouse-cloud-intro8-create-databaseuser.html))

## Brief description of the export content

- **Local tables**

  Tables created by the Data Intelligence pipeline.
  - Feeded by **load_gtfs_rt_to_datasphere**:
  
    - GTFS_RT
    - GTFS_RT_SPEEDS
    
  - Feeded by **load_gtfs_to_datasphere**:
  
    - agency_di
    - calendar_dates_di
    - calendar_di
    - frequencies_di
    - road_disruptions
    - routes_di
    - shapes_di
    - stop_times_di
    - stops_di
    - trips_di
    
  - Populated by **move_gtfs_rt_to_datalake**:
    
    - vehicle_activity_last_update: technical table used for the data tiering
  
  - Not feeded by any pipeline:
    
    - simulation_social_media: it hosts the social media simulated data used to populate the relative dashboard in SAC


- **Remote tables**

  - VEHICLE_ACTIVITY: HANA Cloud Data Lake table with the historical data about the bus activity
  - plannedMaintenanceInterval: vehicle planned maintenance from Digital Vehicle Hub
  - registration: vehicle masterdata from Digital Vehicle Hub				
  - usage: vehicle usage information from Digital Vehicle Hub


- **Graphical views**

  - Used to build **Speed_Analysis_Model**:
    - vehicle_activity_for_speed_analysis_vw
   
  - Used to build **Digital_Vehicle_Hub_Model**:
    - vehicle_activity_vw
    - agency_vw
    - calendar_dates_vw
    - calendar_vw
    - find_latest_load_date
    - frequencies_vw
    - gtfs_rt_vw
    - routes_vw
    - shapes_vw
    - social_media_vw
    - stop_times_vw
    - stops_vw
    - trips_vw
  
  - Used to build **Digital_Vehicle_Hub_Model**:
    - dvh_planned_maintenance_vw
    - dvh_vehicle_masterdata_vw
    - dvh_vehicle_usage_vw
  
  - Used to build **Road_Data_Analytic_Model**:
    - road_disruptions_vw


- **Analytic models**

  - Digital_Vehicle_Hub_Model
  - Road_Data_Analytic_Model
  - Social_Media_Analytic_Model
  - Speed_Analysis_Model
  - Urban_Public_Transport_Model


## How to import the .package file

1. Download the [".package" file](./sap-datasphere) from this GitHub repository;
2. Go to "Transport" at the bottom left and click on "Export" and then on "My Content";
   
   <img width="1663" alt="Screenshot 2023-08-23 at 15 11 20" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/08751471-24e3-4f69-84f5-055eaf9aaedf">

3. Load the .package file by clicking on the "Load" button and selecting the file from your local disk;

   <img width="1660" alt="Screenshot 2023-08-23 at 17 15 40" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/6725db90-9424-497d-9054-0e31f4e7fb40">

4. Go to Transport/Import. In My Content it will appear the content you uploaded (refresh if it does not), click on it;
   
   <img width="1662" alt="Screenshot 2023-08-23 at 15 12 00" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/569ef48d-bd90-4bca-9a25-0dc873d1abc4">

5. In the "Import options" select the options that apply and all the objects, then click on Import;
   
   <img width="1392" alt="Screenshot 2023-08-23 at 15 12 25" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/3ba2a794-6100-49d4-82ba-ce1025aea8ab">

6. You can enable the automatic deployment in the import procedure. In case you don't do that, you will need to deploy the object one by one.


## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
