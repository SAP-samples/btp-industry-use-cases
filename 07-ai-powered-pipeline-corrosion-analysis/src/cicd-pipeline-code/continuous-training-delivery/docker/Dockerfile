FROM python:3
ENV LANG C.UTF-8

RUN apt-get -y update
RUN pip3 install --upgrade pip

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/src/ && \
    mkdir -p /app/data/ && \
    mkdir -p /app/data/training && \
    mkdir -p /app/data/testing

COPY ct_cd_pipeline.py /app/src/

ENV DATA_SOURCE_TRAIN=/app/data/training/
ENV DATA_SOURCE_TEST=/app/data/testing/

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app