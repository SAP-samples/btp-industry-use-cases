FROM python:3
ENV LANG C.UTF-8

RUN apt-get -y update
RUN pip3 install --upgrade pip

RUN apt install docker.io -y
RUN docker --version

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir -p /app/src/ && \
    mkdir -p /app/data/ && \
    mkdir -p /app/data/training && \
    mkdir -p /app/data/testing && \
    mkdir -p /app/credentials

COPY ci_cd_pipeline.py /app/src/
COPY server.py /app/src/

ENV DATA_SOURCE_TRAIN=/mnt/models/
ENV DATA_SOURCE_TEST=/mnt/models/
ENV CREDENTIALS_PATH=/mnt/models/

RUN chgrp -R 65534 /app && \
    chmod -R 770 /app

CMD ["gunicorn", "--chdir", "/app/src", "server:app", "-b", "0.0.0.0:9001"]