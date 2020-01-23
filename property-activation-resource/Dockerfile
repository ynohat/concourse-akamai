FROM python:3-alpine

RUN apk add --no-cache python3 python3-dev libffi-dev openssl-dev build-base && \
    pip3 install --upgrade pip && \
    pip3 install edgegrid-python

ADD property-activation-resource/check.py /opt/resource/check
ADD property-activation-resource/in.py /opt/resource/in
ADD lib/akamai /opt/resource/akamai

RUN chmod +x /opt/resource/*
