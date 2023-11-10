import requests
import pandas as pd
import hana_ml
from hana_ml import dataframe
import numpy as np

from bods_client.client import BODSClient
from bods_client.models import BoundingBox, GTFSRTParams
from bods_client.models import Siri, SIRIVMParams

import haversine as hs
import pytz

def calc_distance(lon_x, lat_x, lon_y, lat_y):
    loc1=(lon_x,lat_x)
    loc2=(lon_y,lat_y)
    return hs.haversine(loc1,loc2)

def on_input(data):
    
    conn = hana_ml.dataframe.ConnectionContext(
        api.config.hanaConnection['connectionProperties']['host'],
        api.config.hanaConnection['connectionProperties']['port'],
        api.config.hanaConnection['connectionProperties']['user'],
        api.config.hanaConnection['connectionProperties']['password'],
        encrypt='true',
        sslValidateCertificate='false'
    )
    
    #Load vehicle locations of the previous round
    df_prev_load = (conn.table('GTFS_RT_LAST_LOAD', schema='URBANPUBLICTRANSPORT#DI'))
    df_prev_load = df_prev_load.collect()
    
    #New request
    API_KEY = "abc"
    bods = BODSClient(api_key=API_KEY)
    
    operator_refs = ["TFLO"] #this maybe can become a parameter?
    params = SIRIVMParams(operator_refs=operator_refs)
    siri_response = bods.get_siri_vm_data_feed(params=params)
    siri = Siri.from_bytes(siri_response)
    vehicle_activities = siri.service_delivery.vehicle_monitoring_delivery.vehicle_activities
    
    df = pd.DataFrame([t.__dict__ for t in vehicle_activities ])
    df = df.drop('monitored_vehicle_journey', axis=1)
    
    df2 = pd.DataFrame([t.monitored_vehicle_journey.__dict__ for t in vehicle_activities ])
    df2 = df2.drop('vehicle_location', axis=1)

    df3 = pd.DataFrame([t.monitored_vehicle_journey.vehicle_location.__dict__ for t in vehicle_activities ])
    result = pd.concat([df, df2, df3], axis=1)
    result['load_date'] = pd.Timestamp('now')
    
    #We save this iteration for the next round
    df_remote1 = dataframe.create_dataframe_from_pandas(
        connection_context = conn, 
        pandas_df = result, 
        table_name = 'GTFS_RT_LAST_LOAD', #this maybe can become a parameter?
        force = True,
        replace = False,
        drop_exist_tab = False #To be changed to False once the table structure is definitive
    )
    
    output = result.merge(df_prev_load,\
        on=['vehicle_ref','direction_ref','vehicle_journey_ref','published_line_name','destination_ref', 'destination_name',\
        'direction_ref','line_ref','operator_ref'],\
        how='left')
        
    final_time   = pd.DatetimeIndex(pd.to_datetime(output['recorded_at_time_x'], utc=True)).tz_convert('Europe/Berlin')
    initial_time = pd.DatetimeIndex(pd.to_datetime(output['recorded_at_time_y'], utc=True)).tz_convert('Europe/Berlin')
    
    output['delta_time_sec'] = (final_time -initial_time).total_seconds()
    output['delta_time_sec'] = output['delta_time_sec'].fillna(0)
                    
    output['distance_km'] = \
        output.apply(lambda x: calc_distance(x.longitude_x,x.latitude_x,x.longitude_y,x.latitude_y), axis=1)
    output['distance_km'] = output['distance_km'].fillna(0)
    
    output['avg_speed'] = output["distance_km"].divide((output["delta_time_sec"]/(60*60)))
    output['avg_speed'] = output['avg_speed'].fillna(-1)
    output.replace([np.inf, -np.inf], -1, inplace=True)
    
    #For testing, to be deleted once the development is completed
    df_remote3 = dataframe.create_dataframe_from_pandas(
        connection_context = conn, 
        pandas_df = output, 
        table_name = 'GTFS_RT_SPEEDS',
        force = True,
        replace = False,
        drop_exist_tab = False
    )

    result = result.merge(output[['vehicle_ref','delta_time_sec','distance_km','avg_speed']], on=['vehicle_ref'], how='left')
    
    df_remote2 = dataframe.create_dataframe_from_pandas(
        connection_context = conn, 
        pandas_df = result, 
        table_name = 'GTFS_RT',
        force = False,
        replace = False,
        append = True
        #force = True,
        #replace = False,
        #drop_exist_tab = False
    )

    api.send('result', api.Message( 'dummy' ))
    
api.set_port_callback('trigger', on_input)
