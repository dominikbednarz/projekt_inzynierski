FROM quay.io/d0min0/projekt_inzynierski:alpine-3.16

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk upgrade \
    && apk add --no-cache --upgrade bash \
    && apk add --update python3 py3-pip \
    && apk add python3-dev build-base linux-headers pcre-dev \
    && pip3 install kafka-python \
    && pip3 install django \
    && pip3 install tzdata \
    && mkdir -p /app/kafka_dashboard \
    && mkdir -p /app/hello

COPY kafka_dashboard /app/kafka_dashboard
COPY hello /app/hello
COPY db.sqlite3 /app/
COPY manage.py /app/

WORKDIR /app