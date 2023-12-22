# Repository for the Flexible Energy Grid use case 
This repository hosts the components (python scripts, Dockerfiles, datasets) of the proof-of-concept developed for the AI-Embedded Flexible Energy Grid use case.
Please, have a look to the blog posts linked below for more details.

[AI-Embedded Flexible Energy Grid: introduction & architecture](https://blogs.sap.com/2023/12/19/ai-embedded-flexible-energy-grid-introduction-architecture/)

[AI-Embedded Flexible Energy Grid: implementation deep dive](https://blogs.sap.com/2023/12/19/ai-embedded-flexible-energy-grid-implementation-deep-dive/)

## Description 
blabla
Below you can find the reference architecture for the full solution we propose. The components highlighted in green are the ones we have prototyped and that you can find here in this repository.

<img width="800" alt="returnpack_architecture" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/18447094/bf0c953e-2cd0-4313-a32b-91cede9b2cf6">


We have organized the source code and the components in general in the folders described below.

File or Folder | Purpose
---------|----------
[dataflows-code/](./dataflows-code/) | Source code for the two pipelines to establish the communication between the cloud and the edge devices.
[dataflows-templates/](./dataflows-templates/) | Templates needed to configure AI Core to execute the communication pipelines.
[datasets/](./datasets/) | Datasets used to train and test the energy demand forecast model.
[development/](./development/) | Some resources we used to develop the poc.
[exports/](./exports/) | Exports of the components developed in SAP Datasphere and SAP Analytics Cloud.
[iot-hub-edge-deployment/](./iot-hub-edge-deployment/) | Source code for the "transported" and "predictor" that are deployed and executed on the edge devices.
[ml-solution-code/](./ml-solution-code/) | Source code to train and deploy the simple energy demeand forecast model in AI Core.
[ml-solution-templates/](./ml-solution-templates/) | Templates needed to configure AI Core to train and deploy the energy demaand forecast model in AI Core.

## Deploy and Run
Please refer to the instructions on each one of the prototype components.

## How to obtain support
[Create an issue](https://github.com/SAP-samples/btp-industry-use-cases/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).

## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## License
Copyright (c) 2023 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](../LICENSE) file.
