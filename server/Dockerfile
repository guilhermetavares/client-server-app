FROM ubuntu:latest
FROM python:latest
ENV PYTHONUNBUFFERED 1

MAINTAINER Guilherme Tavares "zetavares.rib@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

RUN export FLASK_APP=app.py

ADD app /app
WORKDIR /app
RUN pip install -r requirements.txt