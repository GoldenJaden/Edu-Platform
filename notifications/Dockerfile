FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . /app
