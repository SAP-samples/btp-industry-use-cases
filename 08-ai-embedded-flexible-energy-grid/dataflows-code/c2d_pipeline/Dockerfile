FROM python:3
ENV LANG C.UTF-8

RUN apt-get -y update
RUN pip3 install --upgrade pip

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/src/ && \
    mkdir -p /app/data/

COPY c2d_pipeline.py /app/src/
COPY weather_sample.csv /app/data/

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app