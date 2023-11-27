# This script automate the update of the docker image for continous monitoring, 
# when you need to refresh the image with a new version of continuous_monitoring.py

# Prerequisities: 
# Please assure to meet Prerequisities below before using this script.
# 1.Create docker account as per step 1 of  instruction: https://docs.docker.com/docker-hub/quickstart/ 
# 2.Install the docker cli as per step 3 of instruction: https://docs.docker.com/docker-hub/quickstart/ 
# 3.Obtain an access token as per instrunction: https://docs.docker.com/security/for-developers/access-tokens/#create-an-access-token

# To use this script:
# 1.Login docker account on the terminal with command "docker login -u YOUR_DOCKER_USER", Click enter, and enter access token
# 2.Please replace the placeholder <YOUR_DOCKER_USER> with your docker user.
# 3.The step 5~7 are optional, which keep only one version of the image:01.
# If you opt to have a new version of image every update, simply ignore step 5~7 and go to step 8 directly.

# Step 1: Create a container
docker run -it --name continuous-monitoring-container docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:01

# Step 2: Copy the new file into the running container
docker cp continuous_monitoring.py continuous-monitoring-container:/app/src

# Step 3: Commit the changes to create a new image
docker commit continuous-monitoring-container docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:02

# Step 4: Remove the temporary container
docker rm continuous-monitoring-container

# Step 5: Remove the old image (optional)
docker rmi docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:01

# Step 6: Tag the new image (optional)
docker tag docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:02 docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:01

# Step 7: Remove the old image (optional)
docker rmi docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:02

# Step 8: Push the docker image to docker hub
docker push docker.io/<YOUR_DOCKER_USER>/pipeline-corr-continuous-monitoring:01