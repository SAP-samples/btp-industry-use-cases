Here you can find the Python code and all the other ingredients to execute the cloud-to-edge and edge-to-cloud pipelines in AI Core. These two pipelines are used to create a bidirectional data flow from BTP to the edge devices as shown in the animations below.

<h2>Cloud-to-Edge</h2>
  
![Nov-24-2023 15-09-48](https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/4ddb1a2f-be7d-4659-a162-f01b5d654bf7)

<h2>Edge-to-Cloud</h2>
  
![Nov-24-2023 15-11-20](https://github.com/SAP-samples/btp-industry-use-cases/assets/1317854/7a5b1c14-e012-4753-b56a-53f497d3b7d5)

In order to execute the pipelines in AI Core, first you need to tranform the relative code into a Docker image and load it into the Docker registry connected to the AI Core instance. In the two folders here, you can find the needed Dockerfile and the list of dependencies. 
Below you can find the commands to generate and load the Docker image:

* docker login docker.io -u <YOUR_DOCKER_USERNAME>

* docker buildx build -o type=docker --platform=linux/amd64 -t <YOUR_DOCKER_USERNAME>/<PIPELINE_NAME>:01 .

* docker push docker.io/<YOUR_DOCKER_USERNAME>/<PIPELINE_NAME>:01

Another important point for running these pipelines e is to instruct properly AI Core about how the Docker containers have to be run. 
For this you need to use the workflow templates that are described in this [README](../dataflows-templates/README.md).
