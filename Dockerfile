# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

EXPOSE 53/tcp 53/udp 80

WORKDIR /app

RUN apt-get update && \
    apt-get -y install gcc make && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN cd SemanticAnalyzer && make && cp ssga ..

RUN python3 main.py --tcp --dry-run

CMD [ "python3", "main.py", "--tcp", "--udp" ]