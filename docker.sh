#!/bin/bash

echo "$#"

if (( $# == 0 )) || [[ $1 == "-h" ]] || [[ $1 == "--help" ]]
then
    echo "Display help message"
    return 1
fi

# Going to finish this tomorrow