FROM python:3.6-stretch

MAINTAINER Narunas Krasauskas <narun4sk@gmail.com>

ENV PYTHONUNBUFFERED 1
ARG app_path=/opt/ratestask_app/

COPY ./requirements.txt ${app_path}
WORKDIR ${app_path}
RUN apt-get update && apt-get install -y --no-install-recommends\
 netcat-openbsd\
 less &&\
 rm -rf /var/lib/apt/lists/* &&\
 rm -rf /var/cache/apt/archives/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["./wait_for_db.sh", "ratestask_db", "5432", "./app.py"]
