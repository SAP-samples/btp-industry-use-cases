# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import json
from git import Repo
import docker #pip install docker
from docker.errors import APIError, TLSParameterError
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


class ci_cd_pipeline():
    
    def __init__(self) -> None:

        #args = len(sys.argv) - 1
        #pos = 1
        #while (args >= pos):
        #    print ("Parameter at position %i is %s" % (pos, sys.argv[pos]))
        #    pos = pos + 1

        self.git_setup_file_path = environ["CREDENTIALS_PATH"] + "git_setup.json"
        self.docker_secret_file_path = environ["CREDENTIALS_PATH"] + "docker_secret.json"
        
        self.git_repo_name = None
        self.git_repo_url = None
        self.git_repo_username = None
        self.git_repo_password = None
        
        self.docker_secret_name = None
        self.docker_secret_username = None
        self.docker_secret_password = None
        
        self.client = None

        print(self.git_setup_file_path)
        print(self.docker_secret_file_path)
        
        
    def get_github_credentials(self) -> None:

        print("Getting GitHub credentials.")
        # Loads your git_setup.json
        with open(self.git_setup_file_path) as gs:
            setup_json = json.load(gs)

        repo_json = setup_json["repo"]
        self.git_repo_name = repo_json["name"]
        self.git_repo_url = repo_json["url"]
        self.git_repo_username = repo_json["username"]
        self.git_repo_password = repo_json["password"]

        #print(self.git_repo_name, self.git_repo_url, self.git_repo_password)
        
        
    def get_docker_credentials(self) -> None:

        # Loads the json file
        print("Getting Docker credentials.")
        with open(self.docker_secret_file_path) as dsf:
            docker_secret = json.load(dsf)

        self.docker_secret_name = docker_secret["name"]
        self.docker_secret_username = json.loads(docker_secret["data"][".dockerconfigjson"])\
        ["auths"]["docker.io"]["username"]
        self.docker_secret_password = json.loads(docker_secret["data"][".dockerconfigjson"])\
        ["auths"]["docker.io"]["password"]

        #print(self.docker_secret_name, self.docker_secret_username, self.docker_secret_password)
        
    
    def get_githup_repo(self, repo_dest_dir) -> None:

        print("Cloning GitHub repository.")
        git_url = "https://"+self.git_repo_password+\
            "@github.com/sap-btp-ai-sustainability-bootcamp/pipeline-corrosion-repo.git"
        repo_dest_dir = repo_dest_dir

        if not os.path.exists(repo_dest_dir):
            Repo.clone_from(git_url, repo_dest_dir)
        else:
            repo = Repo(repo_dest_dir)
            repo.remotes[0].pull()
        print("GitHub repository cloned.")
        
    
    def set_docker_client(self) -> None:

        print("Creating Docker client.")
        try:
            self.client = docker.from_env()
            self.client.login(username=self.docker_secret_username, password=self.docker_secret_password\
                         #,registry="https://index.docker.io/v1/"
                        )
            print("Docker client created.")
        except (APIError, TLSParameterError) as err:
            print("Error creating Docker client!")
        
    
    def docker_build(self, path, dockerfile, platform, tag) -> None:
        
        print("Building Docker image " + tag)
        self.client.images.build(\
                    path = path,\
                    dockerfile = dockerfile,\
                    platform = platform,\
                    tag = tag)
        print("Docker image built " + tag)
        
    
    def docker_push(self, repository, tag):
        
        print("Pushing Docker image to Docker registry " + repository)
        push_resp = self.client.images.push(\
                    repository = repository,\
                    tag = tag
                    )
        print("Docker image pushed to Docker registry " + repository)
        return push_resp


    def run_workflow(self) -> None:
        """
        Run the pipeline with all the necessary steps
        """
        self.get_github_credentials()
        self.get_docker_credentials()
        self.get_githup_repo("./app/pipeline-corrosion-repo")
        #self.set_docker_client()
        #self.docker_build("./app/pipeline-corrosion-repo/solution-prod-code/train/",\
        #                  "Dockerfile", "linux/amd64", "yoshidj/pipeline-corr-training:test")
        #self.docker_push("yoshidj/pipeline-corr-training", "test")
        #self.docker_build("./app/pipeline-corrosion-repo/solution-prod-code/infer/",\
        #                  "Dockerfile", "linux/amd64", "yoshidj/pipeline-corr-serving:test")
        #self.docker_push("yoshidj/pipeline-corr-serving", "test")
        
        
    
if __name__ == "__main__":
    train_obj = ci_cd_pipeline()
    train_obj.run_workflow()
