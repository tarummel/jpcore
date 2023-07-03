# pull image
FROM python:3.11.1-slim-bullseye

# set ports
EXPOSE 8008

# set env vars
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and memcached prereqs
RUN apt -y update
RUN apt -y install libpq-dev python3-dev cmake memcached

# set project dir in docker image
WORKDIR /jpcore

# copy project from pc -> image
COPY . .

# install dependencies
RUN pip install -r requirements.txt
