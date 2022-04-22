# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && \
    apt-get -y install gcc make && \
    rm -rf /var/lib/apt/lists/*

RUN cd SemanticAnalyzer && make && cp ssga ..

CMD [ "python3", "main.py", "--tcp" ]