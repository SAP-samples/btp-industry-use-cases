Here you can find the Python code for the serving application that will serve your pipeline corrosion predictive model once it has been trained.
This server has to be started in AI Core and the result of this deployment operation will be a deployment URL, an endpoint that will expose your model on the internet for consumption. Under the hood the server will manage the incoming inference requests.

In order to start this server and deploy the model in AI Core, first you need to tranform the Python code into a Docker image and load it into the Docker registry connected to the AI Core instance. In this folder you can find the needed Dockerfile and the list of dependencies. Below you can find the commands to generate and load the Docker image.

* docker login docker.io -u <YOUR_DOCKER_USERNAME>

* docker buildx build -o type=docker --platform=linux/amd64 -t <YOUR_DOCKER_USERNAME>/pipeline-corr-serving:01 .

* docker push docker.io/<YOUR_DOCKER_USERNAME>/pipeline-corr-serving:01

Another important point for running this piece of code is to instruct AI Core about how this Docker container has to be run. For this you need to use a workflow template. For some instructions refer to this [README](../../solution-prod-templates/README.md).
