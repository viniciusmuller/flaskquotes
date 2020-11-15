#!/bin/bash

app="flaskquotes"

# args
name="--name=${app}"
network='--network=host'
version="-v $PWD:/app ${app}"

docker build -t ${app} .
# TODO implement docker volumes
docker run -d -p 5000:5000 ${name} ${network} ${version}
