FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3-dev gcc python3-pip 

WORKDIR /spell-app

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

COPY ./requirements.txt /app/requirements.txt

COPY . /spell-app

COPY templates /spell-app/templates

RUN  pip3 install -r /app/requirements.txt 
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8080" ]