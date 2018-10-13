FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./chck.py", "-f", "tcp://recv:14638", "-t", "tcp://send:14639", "-p", "tcp://prst:14640" ]
