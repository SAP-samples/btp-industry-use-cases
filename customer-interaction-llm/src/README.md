# Getting Started

Welcome to your new project.

It contains these folders and files, following our recommended project layout:

File or Folder | Purpose
---------|----------
`app/` | content for UI frontends goes here
`db/` | your domain models and data go here
`srv/` | your service models and code go here
`package.json` | project metadata and configuration
`readme.md` | this getting started guide


## Run locally
- Configure the database type as "sql" in [package.json](package.json) 
    ```json
    "requires": {
        "db": {
            "kind": "sql"
        }
        ...
    ```
- Maintain the configuration to access the large language models(LLMs) in [srv/config.json](srv/config.json). The required configurations are
    - api_base_url: The base url of LLM API. To be configured in [srv/config.json](srv/config.json)
        ```json
        #For OpenAI API
        "api_base_url": "https://api.openai.com"
        #For Azure OpenAI Service
        "api_base_url": "https://<YOUR_AZURE_OPENAI_INSTANCE>.openai.azure.com"
        ```
    - auth_method: The authentication method of LLMs API to be configured in [srv/config.json](srv/config.json), which only supports api_key in current version, can be easily extended to support the other authentication method such as Basic Authentication, OAuth etc. in line#14 of [srv/llm-proxy-service.js](srv/llm-proxy-service.js)
        ```json
        #For OpenAI API
        "auth_method": "bearer-api-key"
        #For Azure OpenAI Service
        "auth_method": "api-key"
        ``` 
    - api_key: Your private api_key to access llm, to be configured as a process env variable
        ```sh
        local deployment: export api_key="REPLACE_WITH_YOUR_OWN_API_KEY"
        cloud foundry deployment: cf set-env api_key "REPLACE_WITH_YOUR_OWN_API_KEY"
        ```  
- Open a new terminal and run 
    ```sh
    cd customer-customer-interaction-llm/src
    npm install
    npm i -g @sap/cds-dk
    cds watch
    ``` 
- (in VS Code simply choose _**Terminal** > Run Task > cds watch_)


## Learn More

Learn more at https://cap.cloud.sap/docs/get-started/.
