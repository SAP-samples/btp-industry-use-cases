import os
import pandas as pd
import sys
import hana_ml
import json
import glob
import random
from os import environ
from hana_ml import dataframe
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class get_demand_forecast:
    def __init__(self) -> None:

        dbHost = environ["dbHost"]
        dbPort = environ["dbPort"]
        dbUser = environ["dbUser"]
        dbPwd = environ["dbPwd"]
        dbIngestionSchema = environ["dbIngestionSchema"]
        dbConsumptionSchema = environ["dbConsumptionSchema"]

        #print(dbHost1, dbPort1, dbUser1, dbPwd1, dbIngestionSchema1, dbConsumptionSchema1)
        
        self.conn = hana_ml.dataframe.ConnectionContext(
            dbHost,
            dbPort,
            dbUser,
            dbPwd, 
            encrypt='true',
            sslValidateCertificate='false'
        )

        self.blob_storage_connect_str = environ["blobStorageConnectStr"]


    def read_and_write_demand_forecast(self) -> None:

        blob_service_client = BlobServiceClient.from_connection_string(self.blob_storage_connect_str)
        container_client = blob_service_client.get_container_client("energygridcontainer")

        now = datetime.today()
        dt_string = now.strftime("%Y-%m-%d")
        print(dt_string)

        local_path = "/app/data"
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            download_file_path = os.path.join(local_path, blob.name.replace("/","-"))
            if(dt_string in download_file_path):
                #print("\nDownloading blob to \n\t" + download_file_path)
                with open(file=download_file_path, mode="wb") as download_file:
                    download_file.write(container_client.download_blob(blob.name).readall())

        files = glob.glob(local_path+"/*.json", recursive=True)

        columns = ["Timestamp","IoTHubName","DeviceName",\
           "Hour0","Hour1","Hour2","Hour3","Hour4","Hour5",\
           "Hour6","Hour7","Hour8","Hour9","Hour10","Hour11",\
           "Hour12","Hour13","Hour14","Hour15","Hour16","Hour17",\
           "Hour18","Hour19","Hour20","Hour21","Hour22","Hour23"
          ]
        demand_forecast_df = pd.DataFrame(columns=columns)

        demand_forecast_df.drop(demand_forecast_df.index, inplace=True)
        for single_file in files:
            print(single_file)
            with open(single_file, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    if("forecast" in data["Body"]):#to adjust to the final format
                        #print(data["EnqueuedTimeUtc"])
                        #print(data["Properties"]["DeviceLocation"])
                        #print(data["Properties"]["myIoTHub"])
                        #print(data["SystemProperties"]["connectionDeviceId"])
                        #print(data["Body"]["forecast"])
                        
                        properties = [data["EnqueuedTimeUtc"], data["Properties"]["myIoTHub"],\
                                data["SystemProperties"]["connectionDeviceId"]
                        ]
                        
                        data=data["Body"]["forecast"]

                        list= properties+data
                        demand_forecast_df.loc[len(demand_forecast_df)] = list

        df_remote = dataframe.create_dataframe_from_pandas(
            connection_context = self.conn, 
            pandas_df = demand_forecast_df, 
            table_name = 'daily_demand_forecast',
            force = False,
            replace = False,
            append = True
            #force = True,
            #replace = False,
            #drop_exist_tab = False
        )

        daily_demand_forecast_hour_df = demand_forecast_df.melt(id_vars=["Timestamp","IoTHubName","DeviceName"],\
            var_name="Hour")
        daily_demand_forecast_hour_df.rename(columns = {'value':'EnergyDemand'}, inplace = True)

        df_remote2 = dataframe.create_dataframe_from_pandas(
            connection_context = self.conn, 
            pandas_df = daily_demand_forecast_hour_df, 
            table_name = 'daily_demand_forecast_hour',
            #force = False,
            #replace = False,
            #append = True
            force = True,
            replace = False,
            drop_exist_tab = False
        )


if __name__ == '__main__':
    print ( "Starting retrieving and processing the demand forecasts from the Azure storage..." )
    get_demand_forecast = get_demand_forecast()
    get_demand_forecast.read_and_write_demand_forecast()
