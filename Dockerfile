FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
COPY ./fhirclient /usr/local/lib/python2.7/site-packages/fhirclient
#RUN ls -a /usr/local/lib/python2.7/site-packages/fhirclient
#RUN cat /usr/local/lib/python2.7/site-packages/fhirclient/models/humanname.py
