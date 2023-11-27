# -*- coding: utf-8 -*-
"""
Training script to showcase the end-to-end training and evaluation script.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import logging
import joblib
import os
import random
import sys
import pickle
import glob

from os.path import exists
from joblib import load, dump
from os import makedirs, environ

from sklearn import datasets, ensemble
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_api_client_sdk.models.metric import Metric
from ai_api_client_sdk.models.metric_custom_info import MetricCustomInfo
from ai_api_client_sdk.models.metric_tag import MetricTag

FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
# Use filename="file.log" as a param to logging to log to a file
logging.basicConfig(format=FORMAT, level=logging.INFO)


class TrainSKInterface:
    def __init__(self) -> None:
        # Set the params for the training below
        self.model = None
        self.dataset_all = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.dataset_name = "pipeline_corrosion_dataset"
        self.model_name = "gradient_boosting_regressor.pkl"
        self.output_path = environ["OUTPUT_PATH"]
        self.data_source = environ["DATA_SOURCE"]
        self.execution_id = environ["AICORE_EXECUTION_ID"]
        self.api_base_url = environ['AICORE_TRACKING_ENDPOINT']
        self.loss, self.val_loss, self.accuracy, self.val_accuracy, self.mse = None, None, None, None, None
        self.training_history = None
        self.params = None
        self.ai_core_v2_client = None
        self.aic_service_key = "/app/src/aic_service_key.json"
    

    def read_dataset(self) -> None:
        
        data_path = self.data_source    
        logging.info(f"{data_path}")

        csv_files = glob.glob(os.path.join(data_path, "*.csv"))
        dfs = []

        for csv in csv_files:
            df = pd.read_csv(csv)
            dfs.append(df)

        self.dataset_all = pd.concat(dfs, ignore_index=True)
        self.dataset_all = self.dataset_all.sample(frac=1).reset_index(drop=True)
        print(f"No. of training examples: {self.dataset_all.shape[0]}")
        
        return None


    def split_dataset(self) -> None:
        """
        Split the dataset into train, validate and test

        Raises:
            Error: if dataset_train and dataset_test are not set
        """

        if self.dataset_all is None:
            raise Exception("Train or test data not set")

        X, y = self.dataset_all.drop(['corr_depth','date'], axis=1), self.dataset_all[['corr_depth']].values.ravel()

        #Change splitting proportions
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.1, random_state=13)
        #self.train, self.val = train_test_split(self.dataset_all, test_size=0.3, random_state=25)
        #self.val, self.test = train_test_split(self.val, test_size=0.5, random_state=25)

        print(f"No. of training examples: {self.X_train.shape[0]}")
        #print(f"No. of validation examples: {self.val.shape[0]}")
        print(f"No. of test examples: {self.X_test.shape[0]}")

        return None

    
    def init_model(self):
        
        self.params = {
            "n_estimators": 500,
            "max_depth": 4,
            "min_samples_split": 5,
            "min_samples_leaf": 5,
            "learning_rate": 0.05,
            "loss": "squared_error"
        }
        
        self.model = ensemble.GradientBoostingRegressor(**self.params)
        return None


    def train_model(self) -> None:
        """
        Train and save the model
        """

        # Initialize model
        self.init_model()
        self.model.fit(self.X_train, self.y_train)

        test_score = np.zeros((self.params["n_estimators"],), dtype=np.float64)
        for i, y_pred in enumerate(self.model.staged_predict(self.X_test)):
            test_score[i] = mean_squared_error(self.y_test, y_pred)

        self.loss = [np.arange(self.params["n_estimators"]) + 1, self.model.train_score_]
        self.val_loss = [np.arange(self.params["n_estimators"]) + 1, test_score]
        self.mse = mean_squared_error(self.y_test, self.model.predict(self.X_test))

        return None


    def save_model(self) -> None:
        """
        Saves the model to the local path
        """
        
        logging.info(f"Writing tokenizer into {self.output_path}")
        if not exists(self.output_path):
            makedirs(self.output_path)
        # Save the Tokenizer to pickle file

        with open(self.output_path+'/'+self.model_name, 'wb') as f:
            pickle.dump(self.model, f)
        #self.model.save(self.output_path+'/'+self.model_name)

        return None


    def get_model(self) -> None:
        """
        Get the model if it is available locally
        """
        
        if exists(f"{self.output_path}/{self.model_name}"):
            logging.info(f"Loading model from {self.output_path}")
            #self.model = models.load_model(self.output_path+'/'+self.model_name, 
            #                      custom_objects = {"iou_loss": self.iou_loss, "IoUCustom": IoUCustom})
            file = open(self.output_path+'/'+self.model_name,'rb')
            pickle.load(file)
            file.close()
        else:
            logging.info(f"Model has not been trained yet!")

        return None


    def model_metrics(self):
        """
        Perform an inference on the model that was trained
        """
        if self.model is None:
            self.get_model()
        
        #Infer model on the test set and evaluate accuracy
        score = self.mse

        metric = [
            {"name": "Model MSE",
            "value": float(score),
            "labels":[{"name": "dataset", "value": "test set"}]}
            ]

        # Define an AI Core Client. 
        # When the code is executed in AI Core, there is no need to specify the AI Core tenant credentials
        self.ai_core_v2_client =  AICoreV2Client(base_url='')

        # Register the accuracy as a metric with the modify API.
        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        metrics=[   
                    {   "name": "MSE", 
                        "value": float(score),
                        "timestamp": timestamp ,
                        "labels": [ {
                            "name": "dataset",
                            "value": "test set"
                        }]
                    },                     
            ]
        body = {'execution_id': self.execution_id,
                'metrics': [Metric.from_dict(m) for m in metrics],
        }
        self.ai_core_v2_client.metrics.modify(**body)
        
        
        # Register custom informations as metrics. 
        # Custom information can contain anything as long as it is encoded as a string

        # Registering Training History (Loss and Accuracy curves during training)
        self.training_history = [
                    {'loss': str(self.loss)},
                    {'val_loss': str(self.val_loss)}
                ]
        custom_info_1 = [{"name": "training_history", 
                          "value": str(self.training_history)}]

        logging.info(f"custom_info")
        body = {'execution_id': self.execution_id,
                 'custom_info': [ MetricCustomInfo.from_dict(mcid) for mcid in custom_info_1]        
        }
        self.ai_core_v2_client.metrics.modify(**body)

        return None


    def run_workflow(self) -> None:
        """
        Run the training script with all the necessary steps
        """
        self.read_dataset()
        self.split_dataset()
        self.get_model()
        if (self.model is None):
            # Train the model if no model is available
            logging.info(f"Training classifier and saving it locally")
            self.train_model()
            self.save_model()
        self.model_metrics()

        return None


if __name__ == "__main__":
    train_obj = TrainSKInterface()
    train_obj.run_workflow()
