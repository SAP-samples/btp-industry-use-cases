# -*- coding: utf-8 -*-

from io import StringIO
import numpy as np
import pandas as pd
import json
from datetime import datetime
import logging
import joblib
import os
import random
import sys
import time
import yaml
import glob
from IPython.display import clear_output
from os.path import exists
from joblib import load, dump
from os import makedirs, environ
import base64
import requests
from requests.auth import HTTPBasicAuth
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, InListValidation,\
IsDistinctValidation, DateFormatValidation, CustomElementValidation

from sklearn import datasets, ensemble
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split

from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_core_sdk.models import Artifact, Status, TargetStatus, ParameterBinding, InputArtifactBinding

import boto3

FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
# Use filename="file.log" as a param to logging to log to a file
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ct_cd_pipeline:
    
    def __init__(self) -> None:

        args = len(sys.argv) - 1
        pos = 1
        while (args >= pos):
            print ("Parameter at position %i is %s" % (pos, sys.argv[pos]))
            pos = pos + 1

        self.resource_group_dev = "dev"
        self.resource_group_test = "test"
        self.resource_group_prod = "prod"
        
        #self.ai_core_v2_client = AICoreV2Client(base_url='')
        self.ai_core_v2_client = None
        #self.aic_service_key = "/app/src/aic_service_key.json"
        self.aic_service_key = "app/aic_service_key.json"

        self.dataset_name = "pipeline-corr-data"
        self.model_name = "pipelinecorrmodel" #Taken from the GitHub template
        self.scenario_id = "pipeline-corrosion-analytics" #Taken from the GitHub template
        self.executable_name = "training-pipeline" #Taken from the GitHub template
        
        self.data_source_train = os.getenv("DATA_SOURCE_TRAIN")
        self.data_source_test = os.getenv("DATA_SOURCE_TEST")
        self.dataset_path_train = "/data/training" #This must become a parameter
        self.dataset_path_test = "/data/training" #This must become a parameter

        #self.current_deployment_id = sys.argv[1]
        self.current_deployment_id = os.getenv("CURRENT_DEPLOYMENT_ID")
        self.serving_executable_name = "server-pipeline"  #Taken from the GitHub template
        #self.metric_threshold = sys.argv[2]
        self.metric_threshold = float(os.getenv("METRIC_THRESHOLD"))

        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        self.artifact_resp = None
        self.execution_id = None
        self.train_config_resp = None
        self.serve_config_resp = None
        self.execution_resp = None
        self.training_output = None
        self.metric_resp = None
        self.deployment_resp = None
        
        self.dataset_all = None
        
    def create_api_client(self, resource_group) -> None:
        
        print("0. Creating AI API client instance.")
        # Your service key JSON file relative to your aicore instance
        aic_service_key_path = self.aic_service_key

        # Loads the service key file
        with open(aic_service_key_path) as ask:
            aic_service_key = json.load(ask)

        # Creating an AI API client instance
        self.ai_core_v2_client = AICoreV2Client(
            base_url=aic_service_key["serviceurls"]["AI_API_URL"] + "/v2",
            auth_url=aic_service_key["url"] + "/oauth/token",
            client_id=aic_service_key['clientid'],
            client_secret=aic_service_key['clientsecret'],
            resource_group=resource_group
        )
        print("2. AI API client instance created.")

    def create_aws_s3_client(self) -> None:
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

    def get_temp_conf(self) -> None:

        print("1. Retrieving configuration from the GitHub repository.")
        username = environ["GITHUB_USER"]
        token = environ["GITHUB_ACCESS_TOKEN"]
        repo_name = environ["GITHUB_REPO_NAME"]
        train_temp_path = environ["TRAIN_TEMPLATE_PATH"] #This must become a parameter
        serve_temp_path = environ["SERVE_TEMPLATE_PATH"] #This must become a parameter

        train_temp_url = f"https://api.github.com/repos/{username}/{repo_name}/contents{train_temp_path}?ref=main"
        serve_temp_url = f"https://api.github.com/repos/{username}/{repo_name}/contents{serve_temp_path}?ref=main"
        #print(train_temp_url, serve_temp_url)
        
        req_train_temp = requests.get(train_temp_url, auth = HTTPBasicAuth(username, token))
        req_serve_temp = requests.get(serve_temp_url, auth = HTTPBasicAuth(username, token))
        
        if req_train_temp.status_code == requests.codes.ok:
            #print(req_train_temp.status_code)
            req_train_temp = req_train_temp.json()
            content = base64.b64decode(req_train_temp['content'])
            #print(content)
            training_workflow = yaml.safe_load(content)
            #print(training_workflow)
        else:
            print('Content was not found.') #This has to stop the execution
            exit(1)
        
        if req_serve_temp.status_code == requests.codes.ok:
            #print(req_serve_temp.status_code)
            req_serve_temp = req_serve_temp.json()
            content = base64.b64decode(req_serve_temp['content'])
            #print(content)
            serving_workflow = yaml.safe_load(content)
            #print(serving_workflow)
        else:
            print('Content was not found.') #This has to stop the execution
            exit(1)

        # From the training template
        self.scenario_id = training_workflow['metadata']['labels']['scenarios.ai.sap.com/id']
        self.dataset_name = training_workflow['spec']['templates'][0]['inputs']['artifacts'][0]['name']
        self.executable_name = training_workflow['metadata']['name']
        print(self.scenario_id, self.dataset_name, self.executable_name)
        
        self.model_name = serving_workflow['spec']['inputs']['artifacts'][0]['name']
        self.serving_executable_name = serving_workflow['metadata']['name']
        print(self.scenario_id, self.model_name, self.serving_executable_name)
        print("1. Configuration retrieved from the GitHub repository.")


    def csv_validation(self, df_from_csv):
        
        # Statistical properties used to generate the dataset
        # Mean, std, min, max
        v01 = [45.98, 17.29, 21, 74] # Temperature
        v02 = [0.13, 0.1, 0.01, 0.61] # CO2 Partial Pressure
        v03 = [7.6, 0.64, 6.21, 8.57] # pH
        v04 = [34.31, 20.37, 2, 70] # Sulphate ion concentration
        v05 = [3168.79, 2382.86, 66, 7571.14] # Chloride ion concentration
        v06 = [0.42, 0.34, 0.01, 0.9] # Basic sediment and water
        v07 = [8.54, 5.17, 0.2, 17.54] # Million Cubic Feet per day of gas
        v08 = [684.48, 337.45, 125, 1565.97] # Barrel of Oil production per day
        v09 = [1269.38, 1965.96, 1, 9328] # Barrel of Water production per day
        v10 = [1.17, 0.97, 0.04, 2.79] # Iron content
        v11 = [2404.93, 1161.44, 152.5, 4209] # Total Alkalinity as HCO_3
        v12 = [880.93, 569.82, 65, 2050] # Operating pressure
        v13 = [1.11, 0.79, 0.02, 2.56] # Calcium concentration
        
        decimal_validation = [CustomElementValidation(lambda d: isinstance(d, float), 'is not decimal')]
        int_validation = [CustomElementValidation(lambda i: isinstance(i, int), 'is not integer')]
        null_validation = [CustomElementValidation(lambda d: d is not None, 'this field cannot be null')]

        #Maximum offset applied to the variables is 25%
        schema = Schema([
            Column('loc_id', [InRangeValidation(0,1000)]+null_validation+int_validation),
            Column('idx', [InRangeValidation(0,1000)]+null_validation+int_validation),
            Column('date', [DateFormatValidation('%Y-%m-%d')]+null_validation),
            Column('corr_depth', [InRangeValidation(0,50)]+null_validation+decimal_validation),
            Column('v01', [InRangeValidation(v01[2],v01[3]*1.25)]+null_validation+decimal_validation),
            Column('v02', [InRangeValidation(v02[2],v02[3]*1.25)]+null_validation+decimal_validation),
            Column('v03', [InRangeValidation(v03[2],v03[3]*1.25)]+null_validation+decimal_validation),
            Column('v04', [InRangeValidation(v04[2],v04[3]*1.25)]+null_validation+decimal_validation),
            Column('v05', [InRangeValidation(v05[2],v05[3]*1.25)]+null_validation+decimal_validation),
            Column('v06', [InRangeValidation(v06[2],v06[3]*1.25)]+null_validation+decimal_validation),
            Column('v07', [InRangeValidation(v07[2],v07[3]*1.25)]+null_validation+decimal_validation),
            Column('v08', [InRangeValidation(v08[2],v08[3]*1.25)]+null_validation+decimal_validation),
            Column('v09', [InRangeValidation(v09[2],v09[3]*1.25)]+null_validation+decimal_validation),
            Column('v10', [InRangeValidation(v10[2],v10[3]*1.25)]+null_validation+decimal_validation),
            Column('v11', [InRangeValidation(v11[2],v11[3]*1.25)]+null_validation+decimal_validation),
            Column('v12', [InRangeValidation(v12[2],v12[3]*1.25)]+null_validation+decimal_validation),
            Column('v13', [InRangeValidation(v13[2],v13[3]*1.25)]+null_validation+decimal_validation)
        ])
        
        errors = schema.validate(df_from_csv)
        return errors

        
    def read_and_validate_dataset(self, data_source, dataset_path) -> None:
        
        print("2. Reading and validating input dataset.")
        data_path = data_source + dataset_path        
        logging.info(f"{data_path}")

        # Specify the S3 bucket and path
        bucket_name = 'ai-sustainability-dataset'
        training_dataset = f'pipeline-corrosion{data_source}/'
        # List objects in the specified S3 path
        response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=training_dataset)
        # Initialize an empty list to store DataFrames
        dfs = []
        # Loop through the objects and read CSV files
        for obj in response.get('Contents', []):
            file_name = obj['Key']
        
            # Check if the object is a CSV file (you can add more file type checks if needed)
            if file_name.endswith('.csv'):
            # Read the CSV file from S3
                obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_name)
                csv_data = obj['Body'].read().decode('utf-8')
                
                # Create a DataFrame from the CSV data
                df = pd.read_csv(StringIO(csv_data))
                
                # Append the DataFrame to the list
                dfs.append(df)
        # Concatenate all DataFrames into a single DataFrame
        if len(dfs) > 0:
            self.dataset_all = pd.concat(dfs, ignore_index=True)
            self.dataset_all = self.dataset_all.sample(frac=1).reset_index(drop=True)
            print(f"No. of training examples: {self.dataset_all.shape[0]}")
        else:
            print("No CSV files found in the specified S3 path.")
        
        errors = self.csv_validation(self.dataset_all)
        if len(errors) == 0:
            print("2. Dataset validation succeeded!")
        else:
            print("2. Dataset validation failed! Number of identified issues: "+str(len(errors)))
            #print("Check the log for the details about the identified issues.") #Logging to be implemented
            exit(1)   
    
    def register_artifact(self, artifact_s3_path, artifact_type, description) -> None:
        
        print("3. Registering artifact.")
        # Set the artifact configuration
        artifact = {
                "name": self.dataset_name,
                "kind": artifact_type, #For example Artifact.Kind.DATASET
                "url": "ai://default"+artifact_s3_path,  
                "description":  description,
                "scenario_id": self.scenario_id
            }
        # Store the artifact response to retrieve the id for the training configuration
        self.artifact_resp = self.ai_core_v2_client.artifact.create(**artifact)
        print(vars(self.artifact_resp))
        
        if self.artifact_resp.id is not None:
            print("3. Artifact registered.")
        else:
            print("3. Registering artifact failed!")
            exit(1)

    
    def create_training_conf(self) -> None:
        
        print("4. Creating training configuration.")
        scenarios = self.ai_core_v2_client.scenario.query()
        
        artifact_binding = {
            "key": self.dataset_name,
            "artifact_id": vars(self.artifact_resp)['id']
        }

        train_configuration = {
            "name": "pipeline-corr-train-conf",
            "scenario_id": self.scenario_id,
            "executable_id": self.executable_name,
            "parameter_bindings": [],
            "input_artifact_bindings": [ InputArtifactBinding(**artifact_binding) ]
        }

        # Store the configuration response to access the id to create an execution
        self.train_config_resp = self.ai_core_v2_client.configuration.create(**train_configuration)
        print(vars(self.train_config_resp))
        
        if self.train_config_resp.id is not None:
            print("4. Creating training configuration.")
        else:
            print("4. Creating training configuration failed!")
            exit(1)

    
    def start_execution(self) -> None:
        
        print("5. Starting training execution.")
        self.execution_resp = self.ai_core_v2_client.execution.create(self.train_config_resp.id)
        print(vars(self.execution_resp))
        #Add a test to be sure it was registered properly based on the content of execution_resp
        
        if self.train_config_resp.id is not None:
            print("5. Training execution started.")
        else:
            print("5. Training execution failed!")
            exit(1)
        

    def get_execution_status(self) -> None:
        
        print("6. Checking execution status.")
        status = None
        while status != Status.COMPLETED and status != Status.DEAD:
            # Sleep for 5 secs to avoid overwhelming the API with requests
            time.sleep(5)
            # Clear outputs to reduce clutter
            clear_output(wait=True)

            execution = self.ai_core_v2_client.execution.get(self.execution_resp.id)
            status = execution.status
            print('...... Execution status ......', flush=True)
            print(f"Training status: {execution.status}")
            print(f"Training status details: {execution.status_details}")

        if execution.status == Status.COMPLETED:
            print(f"Training complete for execution [{self.execution_resp.id}]!")
            output_artifact = execution.output_artifacts[0]
            self.training_output = {
                "id": output_artifact.id,
                "name": output_artifact.name,
                "url": output_artifact.url
            }
        else:
            print(f"Training failed for execution [{self.execution_resp.id}]!")
            exit(1)
    
    
    def get_execution_metrics(self) -> None:
        
        print("7. Retrieving execution metrics.")
        #execution_resp_id = "e0b2c7a1233a0936" # For testing only
        filter_string = "executionId eq '" + self.execution_resp.id + "'"
        #filter_string = "executionId eq '" + execution_resp_id + "'"
        self.metric_resp = self.ai_core_v2_client.metrics.query(execution_ids=self.execution_resp.id)
        #self.metric_resp = self.ai_core_v2_client.metrics.query(execution_ids=execution_resp_id)

        for m in self.metric_resp.resources:
            for metric in m.metrics:
                print(metric.name)
                print(metric.value)
        print("7. Execution metrics retrieved.")
                
        
    def create_serving_conf(self, resource_group) -> None:
        
        print("8. Creating deployment configuration to test the new model.")
        print(self.model_name, self.training_output["id"])
        self.serve_config_resp = self.ai_core_v2_client.configuration.create(
            name = "pipeline-corr-serving-conf",
            scenario_id = self.scenario_id,
            executable_id = self.serving_executable_name,
            input_artifact_bindings = [
                #InputArtifactBinding(key = "pipelinecorrmodel",\
                #                     artifact_id = "846f909d-d14a-46f5-942b-d33ed656213b") # For testing only
                InputArtifactBinding(key = self.model_name, artifact_id = self.training_output["id"])
            ],
            parameter_bindings = [
                ParameterBinding(key = "greetmessage", value = "Hi AI Core server")
            ],
            resource_group = resource_group
        )
        
        if self.serve_config_resp.id is not None:
            print(self.serve_config_resp.__dict__)
            print("8. Deployment configuration created.")
        else:
            print("8. Deployment configuration creation failed!")
            exit(1)

                
    def deploy_model(self, resource_group) -> None: #To be used to test the model deployment
        
        print("9. Deploying new model.")
        metrics = self.metric_resp.resources[0].metrics
        metric_value = metrics[0].value
        print("MSE: "+str(metric_value))
        
        if(metric_value < self.metric_threshold): 
        
            self.create_serving_conf(resource_group)
            self.deployment_resp = self.ai_core_v2_client.deployment.create(self.serve_config_resp.id)
            print(vars(self.deployment_resp))
            status = self.check_deployment(self.deployment_resp.id)
            if status == Status.DEAD:
                print("9. Deployment failed!")
                exit(1)
        
        else:
            print("9. Deployment is not possible because of model lower accuracy!")
            exit(1)
            
    
    def check_deployment(self, deployment_id):
        
        # Poll deployment status
        status = None
        elapsed_time = 0
        while status != Status.RUNNING and status != Status.DEAD:
            start = time.time()
            time.sleep(5)
            clear_output(wait=True)
            deployment = self.ai_core_v2_client.deployment.get(deployment_id)
            status = deployment.status
            print('...... Deployment status ......', flush=True)
            print(deployment.status)
            print(deployment.status_details)
            end = time.time()
            elapsed_time += (end-start)
            
            if elapsed_time > 600:
                print("Deployment pending for too long. Stopping...")
                break

            if deployment.status == Status.RUNNING:
                print(f"Deployment with {deployment_id} complete!")

        # Allow some time for deployment URL to get ready
        time.sleep(10)
        return status

            
    def test_deployment(self, resource_group, deployment_id) -> None: #For this we need to define 
                                                                        #input artifact in the relative template
        
        print("10. Testing the deployment.")
        X, y = self.dataset_all.drop(['corr_depth','date'], axis=1),\
            self.dataset_all[['corr_depth']].values.ravel()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.001, random_state=13)
        print("Number of test records: "+str(X_test.size))
        
        deployment = self.ai_core_v2_client.deployment.get(deployment_id)
        endpoint = f"{deployment.deployment_url}/v2/predict"
        print(endpoint)

        headers = {
                "Authorization": self.ai_core_v2_client.rest_client.get_token(),
                'ai-resource-group': resource_group,
                "Content-Type": "application/json"}

        def apply_request(row):
            #print(row)
            response = requests.post(endpoint, headers=headers, json=row.to_dict())
            #print(response.json())
            return response.json()[0]
        
        X_test['pred'] = X_test.apply(apply_request, axis=1)
        #print(X_test)
        
        mse = mean_squared_error(y_test, X_test['pred'])
        print('Inference result:', mse)
        
        if mse < self.metric_threshold:
            print("10. Deployment validation passed!")
        else:
            print("10. Deployment validation failed!") #Stop execution and pipeline
            self.stop_deployment(resource_group)
            exit(1)

    
    def stop_deployment(self, resource_group) -> None:
        
        print("11. Stopping the deployment.")
        delete_resp = self.ai_core_v2_client.deployment.modify(self.deployment_resp.id,\
                                                               target_status=TargetStatus.STOPPED)
        status = self.check_deployment(delete_resp.id)
        
        if status == Status.STOPPED:
            print("11. Deployment stopped gracefully.")
        else:
            print("11. Something went wrong stopping deployment!")
            #exit(1)

    
    def switch_model(self, resource_group) -> None:
        
        print("12. Switching the model under the current deployment.")
        metrics = self.metric_resp.resources[0].metrics
        metric_value = metrics[0].value
        print("MSE: "+str(metric_value))
        
        if(metric_value < self.metric_threshold): 
        
            self.create_serving_conf(resource_group)

            patch_resp = self.ai_core_v2_client.deployment.modify(
                deployment_id = self.current_deployment_id, # existing deployment
                configuration_id = self.serve_config_resp.id, # new configuration ID
                resource_group = resource_group
            )

            print(patch_resp.__dict__)
            status = self.check_deployment(patch_resp.id)
            #Log the status especially if it is DEAD or PENDING etc.
            if status == Status.DEAD:
                print("12. Deployment update failed!")
                exit(1)
            
        else:
            print("12. Deployment update is not possible because of model lower accuracy!")
            exit(1)

                
    def run_workflow(self) -> None:
        """
        Run the pipeline with all the necessary steps
        """
        ## 0.Create AI Core Client and AWS S3 Client
        self.create_api_client(self.resource_group_dev)
        self.create_aws_s3_client()

        ## 1.Initialize parameters with prod templates content
        self.get_temp_conf()

        ## 2.Read and test dataset
        self.read_and_validate_dataset(self.data_source_train, "") #To be changed

        ## 3.Register a new dataset if needed
        self.register_artifact(self.dataset_path_train, Artifact.Kind.DATASET, "Pipeline corrosion dataset")

        ## 4.Create a new training configuration
        self.create_training_conf()

        ## 5.Start a new execution/training
        self.start_execution()

        ## Get execution status
        self.get_execution_status()

        ## 6.Get the metrics of the last execution
        self.get_execution_metrics()

        ## 7.It deploys the new trained model for testing purpose
        self.create_serving_conf(self.resource_group_dev)
        
        ## 8.
        self.deploy_model(self.resource_group_dev)

        ## 9.Test the previous deployment in a test resource group
        self.test_deployment(self.resource_group_dev, self.deployment_resp.id)
        #self.test_deployment(self.resource_group_dev, self.current_deployment_id) #Only for testing
                                            #The test should be performed on the model deployed for testing
        ## 10.Once the test is completed the deployment is stopped
        self.stop_deployment(self.resource_group_dev)

        ## Update the current deployment in the prod resource group
        self.switch_model(self.resource_group_dev) #If the previous test is ok,
                                                    #then it updates the current deployment
        
        return None


if __name__ == "__main__":
    train_obj = ct_cd_pipeline()
    train_obj.run_workflow()
