# Specify which base layers (default dependencies) to use
# You may find more base layers at https://hub.docker.com/
FROM python:3.9
#
# Creates directory within your Docker image
RUN mkdir -p /app/src/
# Don't place anything in below folders yet, just create them
RUN mkdir -p /app/data/
RUN mkdir -p /app/model/
#
# Copies file from your Local system TO path in Docker image
COPY train.py /app/src/
COPY requirements.txt /app/src/  
#
# Installs dependencies within you Docker image
RUN pip3 install -r /app/src/requirements.txt
#
# Enable permission to execute anything inside the folder app
RUN chgrp -R 65534 /app && \
    chmod -R 777 /app
