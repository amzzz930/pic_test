FROM python:3.10.11

WORKDIR /home

COPY requirements.txt /home
COPY utils /home/utils

RUN pip install -r requirements.txt