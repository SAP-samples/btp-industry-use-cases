import hana_ml
from hana_ml import dataframe
import numpy as np
from datetime import date
import urllib.request, json
import pandas as pd

def on_input(data):
    
    conn = hana_ml.dataframe.ConnectionContext(
        api.config.hanaConnection['connectionProperties']['host'],
        api.config.hanaConnection['connectionProperties']['port'],
        api.config.hanaConnection['connectionProperties']['user'],
        api.config.hanaConnection['connectionProperties']['password'],
        encrypt='true',
        sslValidateCertificate='false'
    )
    
    today = date.today()
    url = "https://api.tfl.gov.uk/Road/all/Street/Disruption?startDate="+str(today)+"&endDate="+str(today)
    
    hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
    }
    
    req = urllib.request.Request(url, headers=hdr)
    req.get_method = lambda: 'GET'
    response = urllib.request.urlopen(req)
    resp = json.loads(response.read())
        
    df_disruptions = pd.json_normalize(resp)
    df_disruptions = df_disruptions.drop(columns=['$type','recurringSchedules'])
    df_disruptions["load_date"] = today

    df_remote = dataframe.create_dataframe_from_pandas(
        connection_context = conn, 
        pandas_df = df_disruptions, 
        table_name = 'road_disruptions',
        force = True,
        replace = False,
        drop_exist_tab = True
    )
        
    api.send('output', api.Message("dummy"))

api.set_port_callback("trigger", on_input)
