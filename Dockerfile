FROM --platform=linux/amd64 python:3.10

LABEL author="Johnny Villegas"
LABEL version="1.0"

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt
