# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import json
from git import Repo
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

from ai_api_client_sdk.ai_api_v2_client import AIAPIV2Client, Authenticator
from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus
from ai_api_client_sdk.models.parameter_binding import ParameterBinding
from ai_api_client_sdk.models.input_artifact_binding import InputArtifactBinding

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
        self.resource_group_mlops = "mlops"

        self.git_repo_name = None
        self.git_repo_url = None
        self.git_repo_username = None
        self.git_repo_password = None
        
        self.ai_core_v2_client = None
        self.token = None
        self.headers = None
        self.aic_service_key = environ["CREDENTIALS_PATH"] + "/aic_service_key.json"

        self.dataset_name = "pipeline-corr-data"
        self.model_name = "pipelinecorrmodel" #Taken from the GitHub template
        self.scenario_id = "pipeline-corrosion-analytics" #Taken from the GitHub template
        self.executable_name = "training-pipeline" #Taken from the GitHub template
        
        self.data_source_train = environ["DATA_SOURCE_TRAIN"]
        self.data_source_test = environ["DATA_SOURCE_TEST"]
        self.credentials_path = environ["CREDENTIALS_PATH"] + "/git_setup.json"
        self.dataset_path_train = sys.argv[4] #This must become a parameter

        self.current_deployment_id = sys.argv[1]
        self.serving_executable_name = "server-pipeline" #Taken from the GitHub template
        self.metric_threshold = float(sys.argv[2])
        
        self.artifact_resp = None
        self.artifact_id = sys.argv[3]
        self.execution_id = None
        self.train_config_resp = None
        self.serve_config_resp = None
        self.execution_resp = None
        self.training_output = None
        self.metric_resp = None
        self.deployment_resp = None
        
        self.dataset_all = None
        
    
    def get_github_credentials(self) -> None:

        print("Getting GitHub credentials.")
        # Loads your git_setup.json
        with open(self.credentials_path) as gs:
            setup_json = json.load(gs)

        repo_json = setup_json["repo"]
        self.git_repo_name = repo_json["name"]
        self.git_repo_url = repo_json["url"]
        self.git_repo_username = repo_json["username"]
        self.git_repo_password = repo_json["password"]

        #print(self.git_repo_name, self.git_repo_url, self.git_repo_username, self.git_repo_password)

    
    def get_temp_conf(self) -> None:

        print("1. Retrieving configuration from the GitHub repository.")

        username = self.git_repo_username
        token = self.git_repo_password
        repo_name = self.git_repo_name

        folder = "solution-prod-templates" #This must become a parameter
        train_temp_path = folder+"/training_template.yaml?ref=main" #This must become a parameter
        serve_temp_path = folder+"/serving_template.yaml?ref=main" #This must become a parameter

        train_temp_url = "https://api.github.com/repos/"+username+"/"+repo_name+"/contents/"+train_temp_path
        serve_temp_url = "https://api.github.com/repos/"+username+"/"+repo_name+"/contents/"+serve_temp_path
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


    def create_api_client(self, resource_group) -> None:
        
        print("2. Creating AI API client instance.")
        # Your service key JSON file relative to your aicore instance
        aic_service_key_path = self.aic_service_key

        # Loads the service key file
        with open(aic_service_key_path) as ask:
            aic_service_key = json.load(ask)

        # Creating an AI API client instance
        self.ai_core_v2_client = AIAPIV2Client(
            base_url=aic_service_key["serviceurls"]["AI_API_URL"] + "/v2",
            auth_url=aic_service_key["url"] + "/oauth/token",
            client_id=aic_service_key['clientid'],
            client_secret=aic_service_key['clientsecret'],
            resource_group=resource_group
        )

        #print("TOKEN")
        self.token = self.ai_core_v2_client.rest_client.get_token()
        #print(self.token)

        self.headers = {
                "Authorization": self.token,
                'ai-resource-group': resource_group,
                "Content-Type": "application/json"}

        print("2. AI API client instance created.")


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

        
    def read_and_validate_dataset(self, data_source) -> None:
        
        print("3. Reading and validating input dataset.")      
        logging.info(f"{data_source}")

        csv_files = glob.glob(os.path.join(data_source, "*.csv"))
        dfs = []

        for csv in csv_files:
            df = pd.read_csv(csv)
            dfs.append(df)

        self.dataset_all = pd.concat(dfs, ignore_index=True)
        self.dataset_all = self.dataset_all.sample(frac=1).reset_index(drop=True)
        print(f"No. of training examples: {self.dataset_all.shape[0]}")
        
        errors = self.csv_validation(self.dataset_all)
        if len(errors) == 0:
            print("3. Dataset validation succeeded!")
        else:
            print("3. Dataset validation failed! Number of identified issues: "+str(len(errors)))
            #print("Check the log for the details about the identified issues.") #Logging to be implemented
            exit(1)
        
    
    def register_artifact(self, artifact_s3_path, artifact_type, description) -> None:
        
        print("4. Registering artifact.")
        # Set the artifact configuration
        artifact = {
                "name": self.dataset_name,
                "kind": artifact_type, #For example Artifact.Kind.DATASET
                "url": "ai://default"+artifact_s3_path,  
                "description":  description,
                "scenarioId": self.scenario_id
        }

        # Store the artifact response to retrieve the id for the training configuration

        artifact_url = f'{self.ai_core_v2_client.base_url}/lm/artifacts'
        resp = requests.post(url=artifact_url, json=artifact, headers=self.headers)
        self.artifact_resp = resp.json()
        print(self.artifact_resp)
        
        if self.artifact_resp['id'] is not None:
            self.artifact_id = self.artifact_resp['id']
            print(self.artifact_id)
            print("4. Artifact registered.")
        else:
            print("4. Registering artifact failed!")
            exit(1)

    
    def create_training_conf(self) -> None:
        
        print("5. Creating training configuration.")
        #scenarios = self.ai_core_v2_client.scenario.query()

        train_configuration = {
            "name": "pipeline-corr-train-conf",
            "scenarioId": self.scenario_id,
            "executableId": self.executable_name,
            "parameterBindings": [],
            "inputArtifactBindings": [       
                {
                  "key": self.dataset_name,
                  "artifactId": self.artifact_id
                }
            ]
        }

        # Store the configuration response to access the id to create an execution

        conf_url = f'{self.ai_core_v2_client.base_url}/lm/configurations'
        resp = requests.post(url=conf_url, json=train_configuration, headers=self.headers)
        self.train_config_resp = resp.json()

        print(self.train_config_resp)
        
        if self.train_config_resp['id'] is not None:
            print("5. Creating training configuration.")
        else:
            print("5. Creating training configuration failed!")
            exit(1)

    
    def start_execution(self) -> None:
        
        print("6. Starting training execution.")
        
        execution_url = f'{self.ai_core_v2_client.base_url}/lm/configurations/'\
            +self.train_config_resp['id']+"/executions"
        resp = requests.post(url=execution_url, headers=self.headers)
        self.execution_resp = resp.json()
        print(self.execution_resp)
        
        if self.execution_resp['id'] is not None:
            print("6. Training execution started.")
        else:
            print("6. Training execution failed!")
            exit(1)
        

    def get_execution_status(self) -> None:
        
        print("7. Checking execution status.")
        status = None
        execution_id = self.execution_resp["id"]
        while status != "COMPLETED" and status != "DEAD":
            # Sleep for 5 secs to avoid overwhelming the API with requests
            time.sleep(5)
            # Clear outputs to reduce clutter
            #clear_output(wait=True)
            status_url = f'{self.ai_core_v2_client.base_url}/lm/executions/{execution_id}'

            resp = requests.get(url=status_url, headers=self.headers)
            execution = resp.json()
            #print(execution['status'])

            status = execution['status']
            print('...... Execution status ......', flush=False)
            print(f"Training status: {status}")

        if status == "COMPLETED":
            print(f"Training complete for execution [{execution_id}]!")
            output_artifact = execution["outputArtifacts"][0]
            self.training_output = {
                "id": output_artifact["id"],
                "name": output_artifact["name"],
                "url": output_artifact["url"]
            }
            print(self.training_output)
        else:
            print(f"Training failed for execution [{execution_id}]!")
            exit(1)
    
    
    def get_execution_metrics(self) -> None:
        
        print("8. Retrieving execution metrics.")
        execution_id = self.execution_resp["id"]
        
        metric_url = f'{self.ai_core_v2_client.base_url}/lm/metrics?executionIds={execution_id}'
        resp = requests.get(url=metric_url, headers=self.headers)
        #print(resp)
        self.metric_resp = resp.json()
        #print(self.metric_resp)

        for m in self.metric_resp["resources"]:
            for metric in m["metrics"]:
                print(metric["name"])
                print(metric["value"])
        print("8. Execution metrics retrieved.")
                
        
    def create_serving_conf(self, resource_group) -> None:
        
        print("9. Creating deployment configuration to test the new model.")
        self.headers["ai-resource-group"] = resource_group
        #print(self.model_name, self.training_output["id"])

        serve_configuration = {
            "name": "pipeline-corr-serving-conf",
            "scenarioId": self.scenario_id,
            "executableId": self.serving_executable_name,
            "parameterBindings": [
                {
                "key": "greetmessage", 
                "value": "Hi AI Core server"
                }
            ],
            "inputArtifactBindings": [       
                {
                    "key": self.model_name,
                    "artifactId": self.training_output["id"]
                }
            ]
        }
        
        serve_conf_url = f'{self.ai_core_v2_client.base_url}/lm/configurations'
        resp = requests.post(url=serve_conf_url, json=serve_configuration, headers=self.headers)
        self.serve_config_resp = resp.json()
        #print(self.serve_config_resp)
        
        if self.serve_config_resp["id"] is not None:
            print(self.serve_config_resp)
            print("9. Deployment configuration created.")
        else:
            print("9. Deployment configuration creation failed!")
            exit(1)

                
    def deploy_model(self, resource_group) -> None: #To be used to test the model deployment
        
        print("10. Deploying new model.")
        self.headers["ai-resource-group"] = resource_group
        metrics = self.metric_resp["resources"][0]["metrics"]
        metric_value = metrics[0]["value"]
        print("MSE: "+str(metric_value))
        
        if(metric_value < float(self.metric_threshold)): 
        
            self.create_serving_conf(resource_group) ## Create serving configuration
            
            deployment_url = f'{self.ai_core_v2_client.base_url}/lm/configurations/{self.serve_config_resp["id"]}/deployments'
            #print(deployment_url)
            resp = requests.post(url=deployment_url, headers=self.headers)
            self.deployment_resp = resp.json()
            print(self.deployment_resp)
            
            status = self.check_deployment(self.deployment_resp["id"])
            if status == "DEAD":
                print("10. Deployment failed! Check the logs for more details.")
                exit(1)
        
        else:
            print("10. Deployment is not possible because of model lower accuracy!")
            exit(1)
            
    
    def check_deployment(self, deployment_id):
        
        # Poll deployment status
        status = None
        elapsed_time = 0
        while status != "RUNNING" and status != "DEAD" and status != "STOPPED":
            start = time.time()
            time.sleep(5)
            #clear_output(wait=True)
            
            status_url = f'{self.ai_core_v2_client.base_url}/lm/deployments/{deployment_id}'
            #print(status_url)
            resp = requests.get(url=status_url, headers=self.headers)
            deployment = resp.json()
            
            status = deployment["status"]
            print('...... Deployment status ......', flush=False)
            print(deployment["status"])
            #print(deployment.status_details)
            end = time.time()
            elapsed_time += (end-start)
            
            if elapsed_time > 600:
                print("Deployment pending for too long. Stopping...")
                break

            if deployment["status"] == "RUNNING":
                print(f"Deployment with {deployment_id} complete!")

        # Allow some time for deployment URL to get ready
        time.sleep(10)
        return status

            
    def test_deployment(self, resource_group, deployment_id) -> None:
        
        print("11. Testing the deployment.")
        self.headers["ai-resource-group"] = resource_group
        X, y = self.dataset_all.drop(['corr_depth','date'], axis=1),\
            self.dataset_all[['corr_depth']].values.ravel()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.001, random_state=13)
        print("Number of test records: "+str(X_test.size))
        
        get_deployment_url = f'{self.ai_core_v2_client.base_url}/lm/deployments/{deployment_id}'
        deploymet_resp = requests.get(url=get_deployment_url, headers=self.headers)
        deployment_url = deploymet_resp.json()['deploymentUrl']
        endpoint = f"{deployment_url}/v2/predict"
        print(endpoint)

        def apply_request(row):
            #print(row)
            response = requests.post(endpoint, headers=self.headers, json=row.to_dict())
            #print(response.json())
            return response.json()[0]
        
        X_test['pred'] = X_test.apply(apply_request, axis=1)
        #print(X_test)
        
        mse = mean_squared_error(y_test, X_test['pred'])
        print('Inference result:', mse)
        
        if mse < float(self.metric_threshold):
            print("11. Deployment validation passed!")
        else:
            print("11. Deployment validation failed!") #Stop execution and pipeline
            self.stop_deployment(resource_group)
            exit(1)

    
    def stop_deployment(self, resource_group) -> None:
        
        print("12. Stopping the deployment.")
        self.headers["ai-resource-group"] = resource_group
        
        delete_config = {
            "targetStatus": "STOPPED"
        }
        
        stop_url = f'{self.ai_core_v2_client.base_url}/lm/deployments/{self.deployment_resp["id"]}'
        resp = requests.patch(url=stop_url, json=delete_config, headers=self.headers)
        delete_resp = resp.json()
        
        status = self.check_deployment(delete_resp["id"])
        
        if status == "STOPPED":
            print("12. Deployment stopped gracefully.")
        else:
            print("12. Something went wrong stopping the deployment!")
            #exit(1)

    
    def switch_model(self, resource_group) -> None:
        
        print("13. Switching the model under the current deployment.")
        self.headers["ai-resource-group"] = resource_group
        metrics = self.metric_resp["resources"][0]["metrics"]
        metric_value = metrics[0]["value"]
        print("MSE: "+str(metric_value))
        
        if(metric_value < float(self.metric_threshold)):
                    
            self.create_serving_conf(resource_group)
            
            patch_config = {
                "configurationId": self.serve_config_resp["id"]                
            }
            
            patch_url = f'{self.ai_core_v2_client.base_url}/lm/deployments/{self.current_deployment_id}'
            resp = requests.patch(url=patch_url, json=patch_config, headers=self.headers)
            patch_resp = resp.json()

            print(patch_resp)
            status = self.check_deployment(patch_resp["id"])
            if status == "RUNNING":
                print("13. Deployment update completed successfully!")
            if status == "DEAD":
                print("13. Deployment update failed!")
                exit(1)
            
        else:
            print("13. Deployment update is not possible because of model lower accuracy!")
            exit(1)

                
    def run_workflow(self) -> None:
        """
        Run the pipeline with all the necessary steps
        """
        cond1 = self.artifact_id == "None" and self.dataset_path_train == "None"
        cond2 = self.artifact_id != "None" and self.dataset_path_train != "None"
        if (not(cond1 or cond2)):

            ## Initialize parameters with prod templates content
            self.get_github_credentials()
            
            self.get_temp_conf()

            ## Create API client
            self.create_api_client(self.resource_group_dev)

            ## Register a new dataset if needed
            if (self.artifact_id == "None" and len(self.dataset_path_train) != "None"):
                self.register_artifact(self.dataset_path_train, \
                                       "dataset", "Pipeline corrosion dataset")

            ## Create a new training configuration
            self.create_training_conf()

            ## Start a new execution/training
            self.start_execution()

            ## Get execution status
            self.get_execution_status()

            ## Get the metrics of the last execution
            self.get_execution_metrics()

            ## It deploys the new trained model for testing purpose
            self.deploy_model(self.resource_group_dev)

            ## Read and validate the test dataset
            self.read_and_validate_dataset(self.data_source_test)

            ## Test the previous deployment in a test resource group
            self.test_deployment(self.resource_group_dev, self.deployment_resp["id"])

            ## Once the test is completed the deployment is stopped
            self.stop_deployment(self.resource_group_dev)

            ## Update the current deployment in the prod resource group
            self.switch_model(self.resource_group_dev) #If the previous test is ok,
                                                        #then it updates the current deployment

        elif cond1:
            print("Missing parameters! Input Artifact ID and path cannot be empty!")
        elif cond2:
            print("Too many parameters! Specify the Input Artifact ID or path!")


if __name__ == "__main__":
    train_obj = ct_cd_pipeline()
    train_obj.run_workflow()
