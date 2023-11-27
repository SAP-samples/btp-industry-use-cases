# -*- coding: utf-8 -*-
import os
import requests, json
import pandas as pd
from datetime import date,datetime
import sys
import numpy as np
import boto3
from io import StringIO  # Required for reading/writing data as strings

from ai_core_sdk.ai_core_v2_client import AICoreV2Client
from ai_api_client_sdk.ai_api_v2_client import AIAPIV2Client, Authenticator
from sklearn.metrics import mean_squared_error, r2_score
from hdbcli import dbapi

import smtplib
from email.mime.text import MIMEText
import logging

FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
# Use filename="file.log" as a param to logging to log to a file
logging.basicConfig(format=FORMAT, level=logging.INFO)

class continuous_monitoring:
    
    def __init__(self) -> None:

        args = len(sys.argv) - 1
        pos = 1
        while (args >= pos):
            print ("Parameter at position %i is %s" % (pos, sys.argv[pos]))
            pos = pos + 1

        self.resource_group_dev = "dev"
        self.resource_group_test = "test"
        self.resource_group_prod = "prod"
        
        self.aic_service_key_path = "/app/src/aic_service_key.json" #path in docker
        #self.aic_service_key_path = "aic_service_key.json" #path in local execution
        print(self.aic_service_key_path)
        self.dataset_name = "pipeline-corr-data"
        
        self.hana_host = os.getenv("HANA_HOST")
        self.hana_port = int(os.getenv("HANA_PORT", 443))
        self.hana_user = os.getenv("HANA_USER")
        self.hana_password = os.getenv("HANA_PASSWORD")

        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.smtp_sender = os.getenv("SMTP_SENDER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        print(self.smtp_host, self.smtp_port, self.smtp_sender, self.smtp_password)
        #configurable parameters from the workflow passed into argv
        #optional target date string in format of yyyy-mm-dd, default as today if blank
        date_str = sys.argv[1]
        self.date = datetime.today().strftime('%Y-%m-%d') if date_str == None or len(date_str) == 0  \
                                                            else date_str
        self.resource_group = sys.argv[2]
        self.current_deployment_id = sys.argv[3]
        self.mse_threshold = float(sys.argv[4])
        self.incoming_dataset_s3_path = sys.argv[5]
        self.recipients = sys.argv[6].split(',') 
        print(self.recipients)
        
    
    ########################################################################
    # Step 0: Initiate an instance of the ai_core_sdk_client. Run once only.
    # Input Parameters: 
    #   resource_group - The target resource group to be monitored
    ########################################################################
    def create_api_client(self, resource_group) -> None:
        
        print("Step 0. Creating AI API client instance.")
        # Loads the service key file
        with open(self.aic_service_key_path) as ask: 
            aic_service_key = json.load(ask)

        # Creating an AI API client instance
        self.ai_core_v2_client = AIAPIV2Client(
            base_url=aic_service_key["serviceurls"]["AI_API_URL"] + "/v2",
            auth_url=aic_service_key["url"] + "/oauth/token",
            client_id=aic_service_key['clientid'],
            client_secret=aic_service_key['clientsecret'],
            resource_group=resource_group
        )

        # self.ai_authenticator = Authenticator(auth_url=aic_service_key["url"] + "/oauth/token",
        #     client_id=aic_service_key['clientid'],
        #     client_secret=aic_service_key['clientsecret'])
        
        print("AI API client instance created.")

    ########################################################################
    # Step 1: Read the incoming data of pipeline corrosion from AWS S3
    # Input Parameters: 
    #   dataset_file_name(csv) - The given file name of incoming dataset in s3
    # Return:  
    #   df - The dataframe of the given incoming dataset
    ########################################################################
    def read_incoming_data_in_s3(self, dataset_file_name):
        print('Step 1: Read the incoming data of pipeline corrosion from AWS S3')

        # Specify your AWS S3 bucket and file names
        bucket_name = 'ai-sustainability-dataset'
        incoming_dataset = f'pipeline-corrosion/data/incoming/{dataset_file_name}'
        print(incoming_dataset)
        # Read the CSV file from S3 into a DataFrame
        response = self.s3_client.get_object(Bucket=bucket_name, Key=incoming_dataset)
        data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(data))
        print(f'Total {len(df)} records read from {dataset_file_name}')

        return df
    
    ########################################################################
    # Step 2: Perform test of incoming data against pipeline corrosion 
    # prediction model. And calculate the metrics(mse and r2 score) of the test
    # Input Parameters: 
    #   df - The dataframe of the incoming dataset in s3
    #   dataset_file_name(csv) - The given file name of incoming dataset in s3
    # Return:  
    #   df - column pre_corr-dept(the predicted corrosion depth) is added to 
    #   the original df
    ########################################################################
    def perform_test(self, df, dataset_file_name):
        print('Step 2: Perform test of incoming data against pipeline corrosion prediction model.')
        X = df.drop(['corr_depth','date'], axis=1)

        # ai_core_v2_client return 403 error, and ai_api_v2_client return 404 error
        # deployment = self.ai_core_v2_client.deployment.get(self.current_deployment_id)
        # endpoint = f"{deployment.deployment_url}/v2/predict"
        # we'll make direct http call to the AI Core Rest API
        token = self.ai_core_v2_client.rest_client.get_token()
        #print(f'ai-core-sdk-client token: {token}')

        # token generated by authenticator is working fine. In continuous monitoring, authenticator is enough.
        # token = self.ai_authenticator.get_token()
        # print(f'token by authenticator: {token}')

        headers = {
                "Authorization": token,
                'ai-resource-group': self.resource_group,
                "Content-Type": "application/json"}
        
        get_deployment_url = f'{self.ai_core_v2_client.base_url}/lm/deployments/{self.current_deployment_id}'
        deploymet_resp = requests.get(url=get_deployment_url, headers=headers)
        deployment_url = deploymet_resp.json()['deploymentUrl']
        endpoint = f"{deployment_url}/v2/predict"
        print(endpoint)
        
        def apply_request(row):
            response = requests.post(endpoint, headers=headers, json=row.to_dict())
            index = int(row['loc_id'])
            #print(response.text)
            if index % 10 == 0:
                print(f'{index} records proceeded...')
            return response.json()[0]
        
        df['pred_corr_depth'] = X.apply(apply_request, axis=1)
        
        print('Calculating the performance metrics.')
        mse = mean_squared_error(df['corr_depth'],  df['pred_corr_depth'])
        r2 = r2_score(df['corr_depth'],  df['pred_corr_depth'])
        print(f'MSE of continuous monitoring model performance on {dataset_file_name}: {mse}')
        print(f'R2 Score of continuous monitoring model performance on {dataset_file_name}: {r2}')

        return df, mse, r2    
    
    ########################################################################
    # Step 3: Calculate the top n records contributing most to MSE
    # Input Parameters: 
    #   df_result - The result dataframe of step 2
    #   top_n - The desired top count of top mse contributors. default as 10
    # Return:  
    #   df_result - columns residuals(the square of variance between corr_dept
    #   and pred_corr_depth 
    #   mse_top_records - the dataframe of top mse contributors for the report
    ########################################################################
    def calc_top_mse_contributors(self, df_result, top_n=10):
        print('Step 3: Calculate the top n records contributing most to MSE')
        
        # Calculate residuals
        df_result['residuals'] = (df_result["corr_depth"] - df_result['pred_corr_depth']) ** 2
        
        # Create a DataFrame to store residuals along with the original data
        results = pd.DataFrame()
        results['loc_id'] = df_result['loc_id'] 
        results['corr_depth'] = df_result["corr_depth"]
        results['pred_corr_depth'] = df_result['pred_corr_depth']
        results['residuals'] = df_result['residuals'] 

        # Sort by squared residuals in descending order
        mse_sorted_results = results.sort_values(by='residuals', ascending=False)

        # Get the top 10 records with the largest squared residuals
        mse_top_records = mse_sorted_results.head(top_n)

        # Print or inspect these top 10 records
        print(f'The top {top_n} location id contribute the most of MSE:')
        print(mse_top_records)

        return df_result, mse_top_records

    ########################################################################
    # Helper function to get the public ip of the workflow executor in AIC.
    # In order to be able to write the metrics data back SAP Dataspere
    # The public ip of the workflow executor is needed to  add to trusted ip 
    # list of SAP Dataspere
    ########################################################################
    def get_public_ip(self):
        try:
            # Use a well-known service like ipinfo.io to get your public IP
            response = requests.get('https://ipinfo.io')
            if response.status_code == 200:
                data = response.json()
                return data.get('ip')
            else:
                return "Failed to retrieve public IP"
        except Exception as e:
            return str(e)
        
    ########################################################################
    # Step 4: Save the metrics to SAP Dataspere
    # As of current version, the metrics is saved to the open schema of
    # SAP Dataspere via direct DML. The better option should be using 
    # HDI container inside SAP Dataspere
    #
    # Input Parameters: 
    #   idx - The id index of the record as an integer representation of date
    #   for GradientBoosting model of pipeline corrosion prediction.
    #   date - The target date which decide its associated dataset.
    #   mse - The mean square value of the test, result from step 2
    #
    # Return:  
    #   df_result - columns residuals(the square of variance between corr_dept
    #   and pred_corr_depth 
    #   mse_top_records - the dataframe of top mse contributors for the report
    ########################################################################
    def save_metrics_to_hcs(self, idx, date, mse) -> None:
        print('Step 4: Save the metrics to SAP Dataspere')
        print(f'Public IP: {self.get_public_ip()}')

        conn =  None
        cursor = None
        try:
            conn = dbapi.connect(
            address=self.hana_host,
            port=self.hana_port,
            user=self.hana_user,
            password=self.hana_password)

            #Please replace <YOUR_HANA_SCHEMA> as your target schema, where has table pipe_dataset_for_sac_mse created
            sql = 'UPSERT <YOUR_HANA_SCHEMA>.pipe_dataset_for_sac_mse (idx, date, mse) VALUES (?, ?, ?) WHERE idx =?'
            cursor = conn.cursor()
            cursor.execute(sql, (idx, date, mse, idx))
        except Exception as error:
            print('error ocurred on saving metrics to SAP Dataspere')
            print(error)
        finally:
            if cursor != None:
                cursor.close()
            if conn != None and conn.isconnected():
                conn.close()
        print(f'Metrics record {idx}, {date}, {mse} saved to SAP Dataspere')

    ########################################################################
    # Send an email function via smtp
    #
    # Input Parameters: 
    #   subject - subject of email
    #   body - message body of email
    #   sender - sender's email
    #   recipients - the list of recipients
    ########################################################################
    def send_email(self, subject, body, sender, password, recipients) -> None:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")

    ########################################################################
    # Step 5: Send the continuous monitoring report to MLops team via email
    #
    # Input Parameters: 
    #   df - the dataframe of step 3
    #   mse - the mean square error of the test in step 2
    #   r2 - the r2 score of the test in step 2
    #   top_mse_records - the list of top mse contributors in step 4
    #   dataset_file_name - the given file of incoming dataset
    ########################################################################
    def send_report(self, df, mse, r2, top_mse_records, top_n, dataset_file_name) -> None:
        print('Step 5: Send the continuous monitoring result to MLops team via email')
        mse_threshold = self.mse_threshold
        r2_score_threshold = 0.5
        subject = "Continuous Monitoring Report of Pipeline Corrosion ML Model"
        body = f"Dear MLOps Team, Good day.\n\nContinuous Monitoring Pipeline has been successfully executed on {dataset_file_name} at {datetime.now()}.\nHere you have the continuous monitoring report of the Pipeline Corrosion Prediction Model.\nNumber of Total Records: {len(df)}\nMean Square Error: {mse}\nMSE Threshold: {mse_threshold}\nR2 Score: {r2}\nR2 Score Threshold: {r2_score_threshold}\nThe top {top_n} location id contributing to MSE:\n {top_mse_records.to_string(index=False)} \n\nThis is an auto-generated email. Please don't reply.\n\nKind Regards,\nML Operation Team"
        
        self.send_email(subject, body, self.smtp_sender, self.smtp_password, self.recipients)

    ########################################################################
    # Step 6: Save the prediction result and residuals from the working dataframe 
    # back to the dataset in S3
    #
    # Input Parameters: 
    #   df - the working dataframe from step 3
    #   dataset_file_name - The original incoming dataset
    ########################################################################
    def save_pred_to_s3_dataset(self, df, dataset_file_name):
        print('Step 6: Save the prediction result back to the dataset in S3')
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        # Specify AWS S3 bucket and file names
        bucket_name = 'ai-sustainability-dataset'
        incoming_dataset = f'pipeline-corrosion/data/incoming/{dataset_file_name}'

        # Put the modified data (CSV string) to the dataset in AWS S3
        self.s3_client.put_object(Bucket=bucket_name, Key=incoming_dataset, Body=csv_data)
        print(f"Prediction data written to '{incoming_dataset}' in S3.")

    ########################################################################
    # The facade function to orchestrate the whole process of continuous 
    # monitoring
    #
    # Input Parameters: 
    #   date_str - the date string in yyyy-mm-dd format to run the monitoring
    #   default as today
    ########################################################################
    def continuous_monitoring(self, date_str = date.today().strftime('%Y%m%d')) -> None:
        self.create_api_client("dev")

        # Step 1: Read the incoming dataset in AWS S3
        dataset_file_name = f"pipeline_corrosion_{date_str.replace('-','')}.csv"
        df = self.read_incoming_data_in_s3(dataset_file_name)

        # Step 2: Test the dataset on the current active model.
        df, mse, r2 = self.perform_test(df, dataset_file_name)
        
        # Step 3: Calculate the top MSE contributors 
        df, top_mse_contributers = self.calc_top_mse_contributors(df)

        # Step 4: Save the metrics of testing into SAP Dataspere
        idx =  int(df.loc[0, 'idx'])
        self.save_metrics_to_hcs(idx, date_str, mse)

        # Step 5: Notify the MLOp team about the test result via email.
        self.send_report(df, mse, r2, top_mse_contributers, 10, dataset_file_name)

        # Step 6: Optional write back the prediction for each record to the dataset for detail
        # Convert the filtered DataFrame back to CSV format as a string
        self.save_pred_to_s3_dataset(df, dataset_file_name)
    
if __name__ == "__main__":
    monitor = continuous_monitoring()
    monitor.continuous_monitoring(monitor.date)