
# Specify the base layers (default dependencies) to use
FROM python:3.11
ENV LANG C.UTF-8

# Update the tools to download and install packages
RUN apt-get -y update
RUN pip3 install --upgrade pip

# Copies file from your Local system to path in Docker image
RUN mkdir -p /app/src/ 
COPY continuous_monitoring.py /app/src/
COPY aic_service_key.json /app/src/

# Installs dependencies within you Docker image
COPY requirements.txt /app/src/
RUN pip3 install -r /app/src/requirements.txt

# Setup the required env variable.
ENV DATA_SOURCE_TRAIN=/data/training
ENV DATA_SOURCE_TEST=/data/testing
ENV HANA_HOST="<YOUR_HANA_HOST>"
ENV HANA_PORT=443
ENV HANA_USER="<YOUR_HANA_USER>"
ENV HANA_PASSWORD="<YOUR_HANA_PASSWORD>"
ENV AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
ENV SMTP_HOST=smtp.gmail.com 
ENV SMTP_PORT=465
ENV SMTP_SENDER="YOUR_GMAIL_ACCOUNT"
ENV SMTP_PASSWORD="YOUR_GMAIL_PASSWORD"

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app