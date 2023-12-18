import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import keras as keras
from numpy import concatenate
from pickle import dump
import tensorflow as tf
import os

def inverse_scale(X,y,my_scaler):
    inverted=np.concatenate((X[:,0,:], y),axis=1)
    inverted=my_scaler.inverse_transform(inverted)
    return inverted

def make_prediction(X,scaler):
    yhat = lin_model.predict(X)
    yhat = inverse_scale(X, yhat, scaler)
    yhat = yhat[:,-len(targets):]
    return yhat

if __name__ == "__main__":

    # SET VARIABLES
    DATA_PATH = 'app/data/df.csv'
    MODEL_PATH = 'app/model/neural_network'
    SCALER_PATH = 'app/model/scaler.pkl'
    
    # READ TRAINING DATASET  
    df=pd.read_csv(DATA_PATH)
    
    df=df.drop(columns=['year'])
    
    # count number of predictors and number of targets
    targets=['load-h-plus-'+str(i) for i in range(1,25)]
    predictors=[c for c in df.columns if c not in targets]
    n_predictors=df.shape[1]-24
    nsteps=len(targets)
    
    # make sure all values are float
    values = df.values
    values = values.astype('float32')

    # SPLIT TRAIN AND TEST SET
    n_train=1000
    n_test=200
    i_test=n_train+n_test
    train=values[:n_train,:]
    test=values[n_train:i_test,:]

    # NORMALIZE FEATURES
    scaler = MinMaxScaler(feature_range=(0, 1))
    train = scaler.fit_transform(train)
    test=scaler.transform(test)

    # SAVE THE SCALER
    dump(scaler, open(SCALER_PATH, 'wb'))

    # RESHAPE INPUT DATASET

    # separate predictors and targets
    X_train,y_train= train[:,:-len(targets)], train[:,-len(targets):]
    X_test,y_test= test[:,:-len(targets)], test[:,-len(targets):]

    # reshape in 3D
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # BUILD THE NEURAL NETWORK
    lin_model = keras.models.Sequential([
        keras.layers.Flatten(input_shape=[1, len(predictors)]), 
        keras.layers.Dense(128, activation=tf.keras.activations.relu),
        keras.layers.Dense(256, activation=tf.keras.activations.relu),
        keras.layers.Dense(256, activation=tf.keras.activations.relu),
        keras.layers.Dense(24, activation=tf.keras.activations.relu)
    ])

    optimizer = keras.optimizers.Adam(lr=0.0001)

    lin_model.compile(loss='mse',optimizer=optimizer)

    # TRAIN THE NEURAL NETWORK
    history_lin = lin_model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    # SAVE THE TRAINED MODEL
    lin_model.save(MODEL_PATH)




