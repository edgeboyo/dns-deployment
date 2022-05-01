#!/bin/bash

if (( $# == 0 )) || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]
then
    echo "$0 -b/--build -c/--create -d/--deploy -h/--help"
    echo "---------------------------------------------------------------"
    echo "-b/--build - Build docker image from source"
    echo "-c/--create - Create new docker container"
    echo "-p/--publish - Publish this image to a docker repository (required login to repo)"
    echo "-d/--download - Download the image from the docker repository (required login to repo)"
    echo "-h/--help - Show this message"
    echo "---------------------------------------------------------------"
    return 1
fi

for var in "$@"
do
    if [[ $var == '-b' ]] || [[ $var == '--build' ]]
    then
        docker build --tag dns-deployment .
    elif [[ $var == '-c' ]] || [[ $var == '--create' ]] 
    then
        docker run -p 80:80 -p 53:53/tcp -p 53:53/udp -d dns-deployment
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
        docker run -d -p 8086:8086 \
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
    else
        echo "Unknown command: $var"
        echo "Check usage..."
        return 2
    fi
done
