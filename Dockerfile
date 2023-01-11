# Docker Image
FROM python:3.9-alpine3.13 

# Who is maintaining this docker container is defined below
LABEL maintainer="mirzahedali"

# Tells python to print any output directly to the console
ENV PYTHONBUFFERED 1




RUN mkdir /app
# WORDIR is default directory all the commands are going to run from on our docker image
WORKDIR /app
# Copies requirements file into the docker image
COPY ./requirements.txt  /tmp/requirements.txt

COPY ./requirements.dev.txt  /tmp/requirements.dev.txt
# Copies djnago app into the docker image
COPY ./app /app

# Expose port 8000 from our container to our machine when we run the container 
EXPOSE 8000

# Build Argument
ARG DEV=false
# This runs a command on alpine image that we are using when we are building our image
# If we add run on every line it keeps adding image layers for every RUN command, to break 
# line in one RUN command we use && \
# python -m venv /py - creates a virtual env that we use to store our dependencies
# /py/bin/pip install --upgrade pip - Install and upgrade pip on path "/py/bin/pip"
# /py/bin/pip install -r /tmp/requirements.txt - Install our requirements using pip inside our docker image by using requirements file
# rm -rf /tmp - Once rquirements are installed, remove tmp directory to keep docker image as lightweight as possible
# adduser \ - To not use rootuser of alpine image and only use django user, becuase root user has full access to everything in container
# no-create-home - to not create home directory for django-user

# if [ $DEV = "true" ];  shell scripting for installing dev dependencies when dev is true

# postgresql-client is the dependcy docker uses to connect with psycopg2 python module for postgresql
# Sets virtual depency package (directory) so that we can remove them later

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --home /app \
        djangoUser

# Define PATH Environment variable on linux, /py/bin is used as not to add it everytime we run any command using path
ENV PATH="/py/bin:$PATH"


# This should be the last line of docker-file which specifies the user we are switching to
USER djangoUser