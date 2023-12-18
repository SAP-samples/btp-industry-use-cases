# ====================================================================================================
# AI-Embedded Flexible Energy Grid Use Case: [Predictor Module]
# - This module helps in handling inference API call to the local ML model at the edge.
# - The ML model is stored in the neural_network folder.
# ====================================================================================================
# Process Flow:
# 1. In this predictor > app.py handler, the 24hr forecast should be returned as a JSON format.
# 2. It will pass through to transporter > main.py > main method.
# 3. send_to_hub will be called in main.py above.
# 4. In sendFrameForProcessing method, the response will be the 24hr forecast.
# 5. Which then this data should be routed to Blob Storage.
# ====================================================================================================
# Prototype: Note that this scope is a prototype showcase, thus please follow the to-do to make it more realistic:
# To-Do: 1) Each Smart Home Hub should be tagged as a Device ID and this info should be synced with a core system e.g. SAP Cloud for Energy.
# To-Do: 2) Weather information should be real-time retrieval on the point of inference. And it should be region-based on the device's location.
# To-Do: 3) ...
# ====================================================================================================

import json
import logging
import numpy as np 
import pandas as pd
import keras as keras
import tensorflow as tf
import pickle
from sklearn.preprocessing import MinMaxScaler

# Imports for the REST API
from flask import Flask

# Initialisation of load prediction model
nsteps=24

def inverse_scale(X,y,my_scaler):
    inverted=np.concatenate((X[:,0,:], y),axis=1)
    inverted=my_scaler.inverse_transform(inverted)
    return inverted

def make_prediction(X,my_model,my_scaler):
    yhat = my_model.predict(X)
    yhat = inverse_scale(X, yhat, my_scaler)
    yhat = yhat[:,-nsteps:]
    return yhat

# read model (this should be produced by SAP AI Core training)
model = tf.keras.models.load_model('neural_network')

# read scaler (this is required to normalize input variables. It should be also produced by SAP AI Core training)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# yhat is the load forecast for the next 24h. We should remove the following print-out and add here the code to send it to IoT Hub
# print("24h load forecast " , yhat)

app = Flask(__name__)

# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

# Default route just shows simple text
@app.route('/')
def index():
    return 'IoT Edge ML model host harness'

@app.route('/loadpredictor', methods=['POST'])
@app.route('/<project>/loadpredictor', methods=['POST'])
@app.route('/<project>/loadpredictor/nostore', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/loadpredictor', methods=['POST'])
@app.route('/<project>/classify/iterations/<publishedName>/loadpredictor/nostore', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/loadpredictor', methods=['POST'])
@app.route('/<project>/detect/iterations/<publishedName>/loadpredictor/nostore', methods=['POST'])
def predict_handler(project=None, publishedName=None):
    try:
        # INPUT DATA

        # Here I am reading weather predictors from a local csv file, but this array should arrive as a message from IoT Hub
        # ToDo #2: Weather Data
        weather_predictors = np.loadtxt('weather_message.csv', delimiter=',')

        # I am reading load predictors exctracting them randomly from a local csv file. We can leave it as is, as these data should be come from the smart meter.  
        meter_df=pd.read_csv('smart_meter_dataset.csv')
        meter_df=meter_df.sample(1).reset_index(drop=True)
        meter_predictors=meter_df.iloc[0,:]

        # Merging the predictors together
        predictors=np.concatenate( ( meter_predictors, weather_predictors) ).reshape(1, -1)

        # Scale and reshape predictors
        predictors=scaler.transform(np.concatenate( ( predictors, np.zeros((1,24))),axis=1 ) )
        predictors=predictors[:,:-nsteps]
        predictors=predictors.reshape((predictors.shape[0], 1, predictors.shape[1]))

        # MODEL INFERENCE
        yhat=make_prediction(predictors,model,scaler)

        # SEND RESULTS TO THE CLOUD

        # Convert the result from a numpy array to a list. 
        yhat= yhat[0].tolist()

        # Create the dictionary
        output_message={'forecast':yhat}
        # yhat is the load forecast for the next 24h. We should remove the following print-out and add here the code to send it to IoT Hub
        print("24h load forecast " , output_message)
        return json.dumps(output_message)
    except Exception as e:
        print('EXCEPTION:', str(e))
        return 'Error processing image', 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=80)