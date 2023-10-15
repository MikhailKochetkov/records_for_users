FROM python:3.10-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

RUN apt-get -y update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg