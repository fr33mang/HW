FROM python:3.8-slim-buster AS finder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

FROM finder AS finder_dev

RUN pip3 install -r requirements.dev.txt
