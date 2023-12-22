Here you can find the workflow template needed to instruct AI Core about how to run the training Docker container (in our use case we don't want to deploy the model in AI Core, instead we do it at the edge).

This template has to be placed in a folder of the GitHub repository connected to the AI Core instance. Then you need to create an application, that is you need to tell AI Core the folder to scan to find the template.

Once you have set everything, you will have a situation like the one shown below with one scenario and one executables for the training.

<img width="1646" alt="Screenshot 2023-12-22 at 14 02 48" src="https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/25643923-dd5e-4fd7-b7c9-d3991d52c0d2">
