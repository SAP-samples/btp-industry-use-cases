import os
import pandas as pd
import sys
import uuid
import hana_ml
from datetime import datetime
from hana_ml import dataframe
from os import environ
from azure.iot.hub import IoTHubRegistryManager


class send_messages_c2d:
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
        
        weather_raw_data_vw = (self.conn.table('weather_raw_data_vw', schema='FLEXIBLEENERGYGRID'))
        weather_raw_data_vw = weather_raw_data_vw.collect()
        
        iot_components_vw = (self.conn.table('iot_components_vw', schema='FLEXIBLEENERGYGRID'))
        iot_components_vw = iot_components_vw.collect()
        
        self.CONNECTION_STRING = str(iot_components_vw["hub_primary_connection_string"].values[0])
        #print(self.CONNECTION_STRING)
        self.IOTHUB_IDS = iot_components_vw["iot_hub_name"].values.tolist()
        self.DEVICE_IDS = iot_components_vw["iot_device_name"].values.tolist()
        print(self.IOTHUB_IDS)
        print(self.DEVICE_IDS)

        self.column_names=[
         'temp-h-3',
         'temp-h-6',
         'temp-h-12',
         'temp-h-24',
         'hum-h-3',
         'hum-h-6',
         'hum-h-12',
         'hum-h-24',
         'temp-d-minus-2',
         'temp-d-minus-3',
         'temp-d-minus-4',
         'temp-d-minus-5',
         'temp-d-minus-6',
         'temp-d-minus-7',
         'temp-d-minus-8',
         'hum-d-minus-2',
         'hum-d-minus-3',
         'hum-d-minus-4',
         'hum-d-minus-5',
         'hum-d-minus-6',
         'hum-d-minus-7',
         'hum-d-minus-8',
         'avg_temp-w1',
         'avg_temp-w2',
         'avg_temp-w3',
         'avg_temp-w4',
         'avg_hum-w1',
         'avg_hum-w2',
         'avg_hum-w3',
         'avg_hum-w4'
        ]


    def iothub_messaging_sample_run(self) -> None:

        processed_weather_data_df = pd.read_csv("/app/data/weather_sample.csv")
        processed_weather_data_df=processed_weather_data_df.sample(1).reset_index(drop=True)
        processed_weather_data_list=processed_weather_data_df.iloc[0,:].values.tolist()

        try:
            # Create IoTHubRegistryManager
            registry_manager = IoTHubRegistryManager(self.CONNECTION_STRING)

            for i in range(0, len(self.DEVICE_IDS)):
                print ( 'Sending message for device: '+str(self.DEVICE_IDS[i]))
                data = str(processed_weather_data_list)

                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                #print("date and time =", dt_string)

                props={}
                # optional: assign system properties
                props.update(messageId = uuid.uuid4())
                #props.update(correlationId = "correlation_%d" % i)
                props.update(contentType = "application/json")

                # optional: assign application properties
                props.update(IoTHubName = self.IOTHUB_IDS[i])
                props.update(DeviceName = self.DEVICE_IDS[i])
                props.update(Timestamp = dt_string)

                registry_manager.send_c2d_message(self.DEVICE_IDS[i], data, properties=props)

        except Exception as ex:
            print ( "Unexpected error {0}" % ex )
            return
        except KeyboardInterrupt:
            print ( "IoT Hub C2D Messaging service sample stopped" )


if __name__ == '__main__':
    print ( "Starting the Python IoT Hub C2D Messaging service sample..." )
    send_messages_c2d = send_messages_c2d()
    send_messages_c2d.iothub_messaging_sample_run()
