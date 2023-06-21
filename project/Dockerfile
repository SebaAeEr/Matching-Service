# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN set -ex; \
    apt-get update; \
    apt-get install -y ffmpeg; \
    apt-get install git -y;

RUN python -m spacy download en_core_web_lg;
RUN pip install git+https://github.com/openai/whisper.git

# copy project
COPY . .
