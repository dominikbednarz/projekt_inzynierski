FROM cecp-registry.cadc.pl/kafka/alpine:3.16

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --upgrade bash \
    && apk add --update python3 py3-pip \
    && apk add python3-dev build-base linux-headers pcre-dev \
    && pip3 install kafka-python \
    && mkdir /app \
    && mkdir /config

WORKDIR /app
