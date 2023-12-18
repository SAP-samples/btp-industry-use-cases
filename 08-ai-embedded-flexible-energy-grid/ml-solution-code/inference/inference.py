import pandas as pd
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
import keras as keras
import tensorflow as tf
import pickle

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

if __name__ == "__main__":
    
    # read model (this should be produced by SAP AI Core training)
    model = tf.keras.models.load_model('neural_network')
    
    # read scaler (this is required to normalize input variables. It should be also produced by SAP AI Core training)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # INPUT DATA

    # Here I am reading weather predictors from a local csv file, but this array should arrive as a message from IoT Hub
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