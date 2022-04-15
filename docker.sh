#!/bin/bash

if (( $# == 0 )) || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]
then
    echo "$0 -b/--build -c/--create -d/--deploy -h/--help"
    echo "---------------------------------------------------------------"
    echo "-b/--build - Build docker image from source"
    echo "-c/--create - Create new docker container"
    echo "-d/--deploy - Deploy image to docker repository (required login to repo)"
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
        docker container create dns-deployment
    elif [[ $var == '-d' ]] || [[ $var == '--deploy' ]]
    then
        docker tag dns-deployment registry.digitalocean.com/part3-project/dns-deployment
        docker push registry.digitalocean.com/part3-project/dns-deployment
    else
        echo "Unknown command: $var"
        echo "Check usage..."
        return 2
    fi
done