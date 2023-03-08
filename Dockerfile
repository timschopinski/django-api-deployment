FROM --platform=linux/amd64 python:3.10-slim
MAINTAINER Tim Schopinski

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt


RUN pip3 install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user