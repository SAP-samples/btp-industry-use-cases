import hana_ml
from hana_ml import dataframe
import numpy as np
import pandas as pd

import zipfile
import urllib.request
import os

def on_input(data):
    
    conn = hana_ml.dataframe.ConnectionContext(
        api.config.hanaConnection['connectionProperties']['host'],
        api.config.hanaConnection['connectionProperties']['port'],
        api.config.hanaConnection['connectionProperties']['user'],
        api.config.hanaConnection['connectionProperties']['password'],
        encrypt='true',
        sslValidateCertificate='false'
    )
    
    urllib.request.urlretrieve("https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/london/", "gtfs.zip")
    with zipfile.ZipFile('./gtfs.zip', 'r') as zip_ref:
        zip_ref.extractall('./gtfs')

    list = os.listdir('./gtfs/')
    for file in list:
        if file.endswith('.txt'):
            name = "./gtfs/"+file
            df_tmp = pd.read_csv(name)
            df_tmp['load_date'] = pd.Timestamp('now')
            
            df_remote = dataframe.create_dataframe_from_pandas(
                connection_context = conn, 
                pandas_df = df_tmp, 
                table_name = file.replace(".txt",""),
                force = True,
                replace = False,
                drop_exist_tab = False
            )
            
            del df_tmp
            del df_remote
    
    api.send('output', 'dummy')

api.set_port_callback("trigger", on_input)
