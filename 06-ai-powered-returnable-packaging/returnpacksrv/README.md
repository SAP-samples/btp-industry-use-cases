The source code in this folder corresponds to the implementation of our SAP Kyma Serverless Function.
If you want to learn more details about our Kyma Serverless Function please check the blog []().
Please note is is one of the components of the [AI-powered returnable packaging prototype](../readme.md).

## Prerequisites
In order to deploy the Kyma Serverless function implementation shared here you need an SAP BTP subaccount with the following:
- SAP Kyma environmment
Please check the tutorial to [Enable SAP BTP, Kyma Runtime](https://developers.sap.com/tutorials/cp-kyma-getting-started.html).
- SAP HANA Cloud instance 
You can find more details about how to consume SAP HANA Cloud from the SAP BTP Kyma environment on the blog [Consuming SAP HANA Cloud from the Kyma environment](https://blogs.sap.com/2022/12/15/consuming-sap-hana-cloud-from-the-kyma-environment/)
- [Helm Chart](https://helm.sh/). 
The Kyma serverless function has been build as a Helm Chart, please check the [Helm Chart](https://helm.sh/) link for more details on how to get it installed.

## Learn
Whatch the following [SAP Business Technology Platform - Serverless Functions SAP HANA Academy](https://www.youtube.com/playlist?list=PLkzo92owKnVyyemLABuRYmyc29crnvxn3) to learn more about Serverless Functions and how to get a code generator that will facilitate new implementations.

## Configuration
- enter your SAP Kyma cluster id in the file [./helm/returnpacksrv-srv/values.yaml]()./helm/returnpacksrv-srv/values.yaml).
- configure your destination's details to your SAP Returnable Packaging industry cloud solution as well as to your AI-Core deployed model APIs in the [./helm/returnpacksrv-srv/templates/service-dest.yaml]()./helm/returnpacksrv-srv/templates/service-dest.yaml) file or configure them after deployment of the serverless function in the Kyma cockpit.

## Deploy and Run
The Kyma serverless function has been build as a [Helm Chart](https://helm.sh/), check the [Helm Chart](https://helm.sh/) link for more details on how to get it installed.

To deploy the function on your SAP BTP Kyma environment run the command:
```sh
make helm-deploy
```

to undeploy the function run the command:
```sh
make helm-undeploy
```
