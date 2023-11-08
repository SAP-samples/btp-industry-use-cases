COMING SOON - WORK IN PROGRESS
# AI-powered returnable packaging

The source code shared in this repository corresponds to the AI-powered returnable packaging BTP industry use case, please have a look to this [blog]() for more details.

## Description 
The prototyped solution is composed by 3 main blocks:
- SAP AI Core - AI Model in SAP AI Core to detect the packaging type.
-	SAP Kyma – Serverless Function, consuming the AI Core model as well as other BTP Services to implement our AI-returnable packaging backend business logic.
-	SAP Build Apps - user interface allowing the customer to check his/her loyalty points and sustainability goals.

<img width="468" alt="returnpack_architecture" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/18447094/bf0c953e-2cd0-4313-a32b-91cede9b2cf6">

We have organized the source code shared here in 3 main folders corresponding to the 3 main components implemented in our prototype:
File or Folder | Component | Purpose
---------|----------|----------
[/]() | AI Core | 
[returnpacksrv/](./returnpacksrv/) | SAP Kyma | Kyma serverless function source code
[/myPacksUI](./myPacksUI/) | SAP Build Apps | 


## Deploy and Run
Please refer to the instructions on each one of the prototype components.

## How to obtain support
[Create an issue](https://github.com/SAP-samples/btp-industry-use-cases/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
