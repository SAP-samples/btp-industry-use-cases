# Overview

This project includes NodeJS samples of using [Chat API](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference#chat-completions) of GPT-3.5 onward models and [Embedding API](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference#embeddings) of text-embedding-ada-002 (Version 2) models in Azure OpenAI Service through four options.
- [langchain](https://js.langchain.com/docs/)
- [@azure/openai](https://www.npmjs.com/package/@azure/openai) module
- [azure-openai](https://www.npmjs.com/package/azure-openai) module
- direct http call with [axios](https://github.com/axios/axios) module

File or Folder | Purpose
---------|----------
`chat-api/` | noode.js samples of chat completion api for GPT-3.5 onward
`embedding-api/` | noode.js samples embedding api for GPT-3.5 onward
`package.json` | project metadata and configuration
`readme.md` | this getting started guide

## Prerequisitive
- Chat API: Follow the [Quickstart: Get started using ChatGPT and GPT-4 with Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-studio) to provision your Azure OpenAI Service, and obtain its instance name and api key.
- Embedding API: Follow the [Tutorial: Explore Azure OpenAI Service embeddings and document search](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/tutorials/embeddings?tabs=command-line)

## How to Run 
- Install the dependencies in [package.json](package.json) 
    ```sh
    npm install
    ```
- Configure the following environment variables with [instructions](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/chatgpt-quickstart?tabs=command-line&pivots=programming-language-javascript#environment-variables). 
    - AZURE_OPENAI_INSTANCE_NAME: The resource name of your Azure OpenAI Service. e.g. for an API endpoint as https://xxxx.openai.azure.com/, then xxxx as AZURE_OPENAI_INSTANCE_NAME
    - AZURE_OPENAI_API_KEY
    - GPT_MODEL_DEPLOYMENT_NAME: Required by chat api samples. 
    - EMBEDDING_MODEL_DEPLOYMENT_NAME: Required by embedding api samples
        
- Run the sample
    ```sh
    node chat-api/chat-opt2-azure-openai.js
    ``` 
## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.