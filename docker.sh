#!/bin/bash

echo "$#"

if (( $# == 0 )) || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]
then
    echo "Display help message"
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
    else
        echo "Unknown command: $var"
        echo "Check usage..."
        return 2
    fi
done

 # use later

# Going to finish this tomorrow