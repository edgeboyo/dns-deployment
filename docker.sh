#!/bin/bash

if (( $# == 0 )) || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]
then
    echo "$0 -b/--build -c/--create -d/--deploy -h/--help"
    echo "---------------------------------------------------------------"
    echo "-b/--build - Build docker image from source"
    echo "-c/--create - Create new docker container"
    echo "-p/--publish - Publish this image to a docker repository (required login to repo)"
    echo "-d/--download - Download the image from the docker repository (required login to repo)"
    echo "-n/--network - Set up internal network for the containers"
    echo "-u/--up - Set up both required containers and remove previous versions"
    echo "-h/--help - Show this message"
    echo "---------------------------------------------------------------"
    exit 1
fi

for var in "$@"
do
    if [[ $var == '-b' ]] || [[ $var == '--build' ]]
    then
        docker build --tag dns-deployment .
    elif [[ $var == '-c' ]] || [[ $var == '--create' ]] 
    then
        docker run -d --network deployment-network --name=dns-deployment -p 53:53/tcp -p 53:53/udp -p 80:80 dns-deployment
    elif [[ $var == '-p' ]] || [[ $var == '--publish' ]]
    then
        docker tag dns-deployment registry.digitalocean.com/part3-project/dns-deployment
        docker push registry.digitalocean.com/part3-project/dns-deployment
    elif [[ $var == '-d' ]] || [[ $var == '--download' ]]
    then
        docker pull registry.digitalocean.com/part3-project/dns-deployment
        docker tag registry.digitalocean.com/part3-project/dns-deployment dns-deployment:latest
    elif [[ $var == '-i' ]] || [[ $var == '--influx-db' ]]
    then
        docker run -d --network deployment-network --name=influx-db -p 8086:8086 \
      -v "$PWD/data":/var/lib/influxdb2 \
      -v "$PWD/config":/etc/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME="superuser" \
      -e DOCKER_INFLUXDB_INIT_PASSWORD="superuser_passwd" \
      -e DOCKER_INFLUXDB_INIT_ORG="part3" \
      -e DOCKER_INFLUXDB_INIT_BUCKET="p3-bucket" \
      -e DOCKER_INFLUXDB_INIT_RETENTION=1w \
      -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN="secret-auth-token" \
      influxdb:2.0
    elif [[ $var == '-n' ]] || [[ $var == '--network' ]]
    then
        docker network create deployment-network
    elif [[ $var == '-u' ]] || [[ $var == '--up' ]]
    then
        docker container stop dns-deployment influx-db
        docker container rm dns-deployment influx-db
        $0 -i
        echo "Waiting 30 seconds for db startup..."
        sleep 30
        $0 -c
    else
        echo "Unknown command: $var"
        echo "Check usage..."
        exit 2
    fi
done
