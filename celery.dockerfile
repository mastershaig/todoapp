FROM python:3.6
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true

ENV APP_ROOT /src
ENV DEBUG False
RUN mkdir /src;

WORKDIR ${APP_ROOT}

RUN mkdir /config
ADD requirements.txt /config/
RUN pip install --no-cache-dir -r /config/requirements.txt

ADD . ${APP_ROOT}