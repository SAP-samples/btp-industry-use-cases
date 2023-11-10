-- SQL statement to retrieve the data to move from the HANA Cloud table

SELECT "recorded_at_time","item_identifier","valid_until_time","bearing","block_ref","framed_vehicle_journey_ref","vehicle_journey_ref","destination_name","destination_ref","origin_name","origin_ref","origin_aimed_departure_time","direction_ref","published_line_name","line_ref","operator_ref","vehicle_ref","longitude","latitude","load_date","delta_time_sec","distance_km","avg_speed" FROM "GTFS_RT" WHERE "load_date" < (SELECT MAX("load_date") FROM "GTFS_RT")


-- SQL statement to determine the timestamp of the most recent records moved to the Data Lake

SELECT MAX("load_date") max_load_date FROM "krisztian"."VEHICLE_ACTIVITY"


-- Deletetion of the data already moved from the HANA Cloud table based on the timestamp determined in the previous step

DELETE FROM "GTFS_RT" WHERE 
TO_TIMESTAMP(TO_NVARCHAR("GTFS_RT"."load_date", 'YYYY-MM-DD HH24:MI:SS')) <= 
(SELECT TO_TIMESTAMP(TO_NVARCHAR("vehicle_activity_last_update"."max_load_date", 'YYYY-MM-DD HH24:MI:SS')) FROM "vehicle_activity_last_update")