# Getting Started

Welcome to your new project.

It contains these folders and files, following our recommended project layout:

File or Folder | Purpose
---------|----------
`app/` | SAP Fiori Elment Applications for Customer Interaction, Interaction Insight etc.
`db/` | CDS domain models and data 
`srv/` | CDS service models and code 
`package.json` | project metadata and configuration
`readme.md` | this getting started guide

## Prerequistives
### GPT-3.5/GPT-4 Access
You must have access to GPT-3.5-Turbo or GPT-4 APIs either through Azure OpenAI Service or OpenAI, and obtain the api key and endpoint to access GTP APIs.
- Azure OpenAI Service: <br/>
Please follow [the quitstart of GPT-3.5-Turbo & GPT-4.0](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-javascript#prerequisites) to have access to Azure OpenAI Service, and retrieve api key and endpoint of Azure OpenAI Service
- OpenAI: <br/>
You may [sign up](https://platform.openai.com/signup) an OpenAI account, then Create an [API Key](https://platform.openai.com/account/api-keys) for API access
<br/>
### Prerequistive for Run locally
If you choose to [run locally](#option-1-run-locally), then please follow the instruction about [Setup for Local Development of CAP](https://cap.cloud.sap/docs/get-started/jumpstart#setup)

### Prerequistive for Clound Foundry Deployment and SAP HANA Cloud
Alternatively, deploy the solution on [SAP BTP, Cloud Foundry env and SAP HANA Cloud](#option-2-deploy-and-run-in-sap-btp-cloud-foundry-env). 
- Required Softwares:
    - SAP Business Studio Studio or Visual Studio Code 
    - If you don’t have a Cloud Foundry Trial subaccount and dev space on [SAP BTP](https://cockpit.hanatrial.ondemand.com/cockpit/) yet, create your [Cloud Foundry Trial Account](https://developers.sap.com/tutorials/hcp-create-trial-account.html) with US East (VA) as region and, if necessary [Manage Entitlements](https://developers.sap.com/tutorials/cp-trial-entitlements.html).
    - You’ve downloaded and installed the [cf command line client](https://github.com/cloudfoundry/cli#downloads) for Cloud Foundry as described in [the tutorial Install the Cloud Foundry Command Line Interface (CLI)](https://developers.sap.com/tutorials/cp-cf-download-cli.html).
    - You’ve downloaded and installed the [MBT Built Tool](https://sap.github.io/cloud-mta-build-tool/download/).
    - You’ve downloaded and installed the [MultiApps CF CLI plugin](https://github.com/cloudfoundry/multiapps-cli-plugin/blob/master/README.md).
- [Required BTP services](mta.yml): 
    - SAP HANA Cloud: You’ve to [Use an existing SAP HANA Cloud service instance](https://developers.sap.com/tutorials/btp-app-hana-cloud-setup.html#42a0e8d7-8593-48f1-9a0e-67ef7ee4df18) or [set up a new SAP HANA Cloud service instance](https://developers.sap.com/tutorials/btp-app-hana-cloud-setup.html#3b20e31c-e9eb-44f7-98ed-ceabfd9e586e) to deploy your CAP application.
    - CF Run-time with memory quota at least 256 MB

### Optional Services and Components 
Only required if you would like to have the end-to-end integration with SAP Field Service Management etc, which is used by [orchestrator-service](srv/orchestrator-service.js)
- Destinations: 
    - FSM: Destination to [SAP Field Service Management OData API](https://help.sap.com/docs/SAP_FIELD_SERVICE_MANAGEMENT/fsm_api_quick_start_guide/api-guide-overview.html)
    - BR: Destination to [Business Rule Service in SAP Build Process Automation](https://api.sap.com/api/SPA_Decision/overview)
- UAA
- SAP Field Service Management: Service Call to be created if the inbound customer message in the customer interaction is classified as Technical Issue. 
- Business Rule Service in SAP Build Process Automation: Rules about Message Classifications and Actions

## Download
Download the source code with commands below.
```sh
git clone https://github.com/SAP-samples/btp-industry-use-cases.git
cd 04-customer-interaction-gpt4
```

## Configuration
Setup the configuration to access the large language models(LLMs) in [srv/config.json](srv/config.json). The required configurations are
- api_base_url: The base url of LLM API. To be configured in [srv/config.json](srv/config.json)
    ```json
    #For OpenAI API
    "api_base_url": "https://api.openai.com"
    #For Azure OpenAI Service
    "api_base_url": "https://<YOUR_AZURE_OPENAI_INSTANCE_NAME>.openai.azure.com"
    ```
- auth_method: The authentication method of LLMs API to be configured in [srv/config.json](srv/config.json), which only supports api_key in current version, can be easily extended to support the other authentication method such as Basic Authentication, OAuth etc. in line#14 of [srv/llm-proxy-service.js](srv/llm-proxy-service.js)
    ```json
    #For OpenAI API
    "auth_method": "bearer-api-key"
    #For Azure OpenAI Service
    "auth_method": "api-key"
    ``` 
## Deployment Options
### Option 1-Run locally
- Configure the database type as "sql" in [package.json](package.json) 
    ```json
    "requires": {
        "db": {
            "kind": "sql"
        }
    }
    ```
- Configure api_key with Your private api_key to access llm, to be configured as a process env variable. Open a new terminal and run 
    ```sh
    #Local deployment: 
    ##macOS/Linux:
    export api_key="REPLACE_WITH_YOUR_OWN_API_KEY"

    ##Windows:
    ####Option 1-CMD 
    setx api_key "REPLACE_WITH_YOUR_OWN_API_KEY"
    ####Option 2-PowerShell
    Env:api_key="REPLACE_WITH_YOUR_OWN_API_KEY"
    ```  
- Run the following commands to install the dependency and run the cap app in the same terminal session above, which the environment variable api_key has been configured.
    ```sh
    cd 04-customer-customer-interaction-llm/src
    npm install
    #If you haven't installed cds command line tool, then install it, otherwise skip it
    npm i -g @sap/cds-dk
    cds watch
    ``` 
- Open its SAP Fiori Element Apps with url: [http://localhost:4004](http://localhost:4004) in the browser, then click [/fiori-apps.html](http://localhost:4004/fiori-apps.html) to open the Fiori Launchpad Home page.

### Option 2-Deploy and Run in SAP BTP, Cloud Foundry env
#### Step 1-Deploy to Cloud Foundry
You may choose either MTA approach or cf push approach to deploy the apps(customer-interaction-llm-db and customer-interaction-llm-srv)
- [Option 1: cf deploy MTA approach](https://cap.cloud.sap/docs/guides/deployment/to-cf#deploy)
    cd src
    #login to your cloud foundry env
    cf login
    mbt build -t mta_archives/
    cf deploy mta_archives/customer-interaction-llm_1.0.0.mtar
    ```
- [Option 2: cf push approach](https://cap.cloud.sap/docs/guides/deployment/to-cf#deploy-using-cf-push)
    ```sh
    cd src
    #login to your cloud foundry env
    cf login
    #build the solution for production
    cds build --production
    #deploy the solution with cf push
    cf push
    ```

#### Step 2-Configure and Run in Cloud Foundry
- Configure the environment variable <b>api_key</b> with your private api_key to access the llm within the same terminal session of [Deloyment to Cloud Foundry](#step-1-deploy-to-cloud-foundry) above
    ```sh
    #setup the api_key in the process variable
    cf set-env customer-interaction-llm-srv api_key "REPLACE_WITH_YOUR_OWN_API_KEY"
    #restart the customer-interaction-llm-srv to take effect of the env variable api_key
    cf restart customer-interaction-llm-srv
    #find out the url of customer-interaction-llm-srv
    cf apps
    ```
- Open the url of customer-interaction-llm-srv app in the browser. Please note that its fiori apps are not deployed. If you would like to access the fiori apps, please follow the [Hybrid Deployment](#option-3-hybrid-deployment) section.

### Option 3-Hybrid Deployment
We also can have the database (customer-interaction-llm-db) deployed to SAP HANA Cloud as per instruction of [Deploy and Run in SAP BTP, Cloud Foundry env](#option-2-deploy-and-run-in-sap-btp-cloud-foundry-env), while run the service app(customer-interaction-llm-srv) and fiori apps locally connecting to customer-interaction-llm-db in SAP HANA Cloud. Please follow the instructions below.
- Configure the database type as "hana-cloud" in [package.json](package.json) 
    ```json
    "requires": {
        "db": {
            "kind": "hana-cloud"
        }
    }
    ```
- Follow the rest of steps in [Run locally](#option-1-run-locally) except the step of configuring the database type, which is configured in last step.

## Test the APIs of customer-interaction-llm-srv
You may test the APIs of customer-interaction-llm-srv with [test/query.http](test/query.http), which requires [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) extension of Visual Studio Code.