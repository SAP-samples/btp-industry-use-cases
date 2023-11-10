-- SQL statement for deleting old data from the Data Lake

DELETE FROM krisztian.VEHICLE_ACTIVITY WHERE "load_date" < TODAY(*)