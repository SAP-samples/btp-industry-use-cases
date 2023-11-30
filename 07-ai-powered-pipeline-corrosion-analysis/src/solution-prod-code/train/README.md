Here you can find the Python code to execute the training of a simple Gradient Boosting Regressor for the prediction of the pipeline corrosion.
We generated an historical dataset to train it. For this use case we have imagined to measure several points along a pipeline in Germany and we imagined also that these points are affected by different corrosion rates. We have assumed also that our pipeline was installed in 2013 and that in the beginning it didn’t show any corrosion. Moreover, we assumed that the corrosion rates were constant in time. You can check the details in [this blog post](https://blogs.sap.com/2023/11/27/ai-powered-pipeline-corrosion-analysis-implementation-deep-dive/). The simulated dataset can be found [here](./data). You need to upload it into an object store (like an AWS S3 bucket) connected  to AI Core and register the dataset as an artefact in AI Core in order to consume it.

In order to execute this code in AI Core, first you need to tranform it into a Docker image and load it into the Docker registry connected to the AI Core instance.
In this folder you can find the needed Dockerfile and the list of dependencies. Below you can find the commands to generate and load the Docker image.

* docker login docker.io -u <YOUR_DOCKER_USERNAME>

* docker buildx build -o type=docker --platform=linux/amd64 -t <YOUR_DOCKER_USERNAME>/pipeline-corr-training:01 .

* docker push docker.io/<YOUR_DOCKER_USERNAME>/pipeline-corr-training:01

Another important point for running this piece of code is to instruct AI Core about how this Docker container has to be run. 
For this you need to use a workflow template. For some instructions refer to this [README](../../solution-prod-templates/README.md).
