# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
# ====================================================================================================
# Background:
# This prototype has been adapted from the following tutorial.
# https://learn.microsoft.com/en-us/azure/iot-edge/tutorial-deploy-custom-vision
# ====================================================================================================
# AI-Embedded Flexible Energy Grid Use Case: [Transporter Module]
# - This module helps in processing inputs from various smart home hubs and outputs from other sources such as weather information.
# - Then it communicates back to the IoT Hub, through message routing query to a Blob Storage.
# ====================================================================================================
# High-Level Logic Flow:
# 1. IoT Edge Device Runtime is on standby in receiving any messages from the provider (cloud) - on_message_received
# 2. Upon receiving the trigger from the provider, message_handler is called.
# 3. Data from provider is passed on the API call to the predictor module through the method sendFrameForProcessing.
# 4. In the predictor module, a local ML model is inferenced against the related data from the provider and the Smart Home Hub.
# 5. Once processing is completed, the results is sent back to the hub for further analysis.
# 6. send_to_hub is called to route output to a Blob Storage. The query for this trigger is level=storage property.
# Tips:
# - IoT Hub connection string should be retrieved programatically, but not for this prototype.
# Resources:
# - C2D Messaging Python: https://learn.microsoft.com/en-us/azure/iot-hub/c2d-messaging-python
# ====================================================================================================
# Prototype: Note that this scope is a prototype showcase, thus please follow the to-do to make it more realistic:
# To-Do: 1) ...
# ====================================================================================================
# PLEASE READ BEFORE PROCEEDING
# dev iothub
# CONNECTION_STRING = "abc"

# [energy grid iothub]

# device connection string for 249a01f4
# transporter:0.0.1
# CONNECTION_STRING = "abc"

# device connection string for 479899d1
# transporter:0.0.2
# CONNECTION_STRING = "abc"

# device connection string for 17ba4537
# transporter:0.0.3
# CONNECTION_STRING = "abc"

# device connection string for 7eb9a903
# transporter:0.0.4
# CONNECTION_STRING = "abc"
# ====================================================================================================
# CONNECTION_STRING <== make sure you enter the IoT Edge Device connection string.
# ====================================================================================================

import time
import os
import requests
import json
import time
from azure.iot.device import IoTHubModuleClient, IoTHubDeviceClient, Message

# global client
CLIENT = None
DEVICECLIENT = None

# Retrieve the load predictor endpoint from container environment
LOAD_PREDICTOR_ENDPOINT = os.getenv('LOAD_PREDICTOR_ENDPOINT', "")

# c2d message
RECEIVED_MESSAGES = 0

# device connection string for 479899d1
# transporter:0.0.2
CONNECTION_STRING = "HostName=energy-grid-iothub.azure-devices.net;DeviceId=berlin-ami123-479899d1-meter;SharedAccessKey=vWyunDBz43C+LIaJDnb9SsLoFX6hej9ocAIoTE8hPQo="

def message_handler(message):
    global RECEIVED_MESSAGES
    RECEIVED_MESSAGES += 1
    print("")
    print("Message received, triggered from SAP AI Core execution:")

    for property in vars(message).items():
        print ("    {}".format(property))
    print("Total calls received: {}".format(RECEIVED_MESSAGES))

    loadprediction = sendDataForProcessing(LOAD_PREDICTOR_ENDPOINT)
    if loadprediction:
        send_to_hub(loadprediction)

# Send a message to IoT Hub
# Route output1 to $upstream in deployment.template.json
def send_to_hub(strMessage):
    message = Message(bytearray(strMessage, 'utf8'))
    message.custom_properties["level"] = "storage"
    message.custom_properties["location"] = "berlin"
    message.custom_properties["myIoTHub"] = "energy-grid-iothub"
    message.content_encoding = "utf-8"
    message.content_type = "application/json"
    CLIENT.send_message_to_output(message, "output1")
    print("")
    print("Message has been processed and sent to hub. Note: Message routing should be enabled with query level=storage, to store in Blob Storage.")
    print("Important: If message routing has been enabled, the message will be intercepted and would not be displayed in Azure IoT Explorer.")

# Return the JSON response from the server with the prediction result
def sendDataForProcessing(loadPredictorEndpoint):
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(loadPredictorEndpoint, headers = headers)
        print("")
        print("Response from load predictor: " + json.dumps(response.json()) + "\n")
    except Exception as e:
        print(e)
        print("No response from predictor service.")
        return None

    return json.dumps(response.json())

def main():
    try:
        try:
            # Instantiate the client
            global CLIENT
            CLIENT = IoTHubModuleClient.create_from_edge_environment()
            DEVICECLIENT = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
            DEVICECLIENT.on_message_received = message_handler
            print ("Waiting for Provider (Cloud-2-Device) messages...")
        except Exception as iothub_error:
            print ( "Unexpected error {} from IoTHub".format(iothub_error) )
            return

        while True:
            time.sleep(150)

    except KeyboardInterrupt:
        print ( "IoT Edge Transporter stopped" )

if __name__ == '__main__':
    main()
