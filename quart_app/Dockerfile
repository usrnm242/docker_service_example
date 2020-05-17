FROM python:3

RUN mkdir -p /usr/src/quart_app
# inside current container

WORKDIR /usr/src/quart_app

COPY . .

RUN pip install -r requirements.txt
