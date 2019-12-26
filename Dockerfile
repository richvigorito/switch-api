FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y -q build-essential python-pip python-dev python-simplejson git vim 

RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv

RUN mkdir deployment

RUN git clone https://github.com/richvigorito/switch-api.git /deployment/
RUN virtualenv /deployment/env/
RUN /deployment/env/bin/pip install flask
RUN FLASK_DEBUG=1
WORKDIR /deployment
CMD env/bin/python app.py
