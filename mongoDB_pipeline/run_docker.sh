#!/bin/bash

## Get the mongoDB image
docker pull mongo:latest

## Run the mongoDB container with the correct data volume mounted
docker run --name fungal-mongo -v /var/lib/mongodb:/data/db -d mongo:latest

## Build the query pipeline image
docker build -t fungal_mongo .

## Run the mongodb wrapper
docker run -t fungal_mongo /Clinical_Metagenomics_2015_Fall/mongoDB_pipeline/bin/mongodb_wrapper.sh --link fungal-mongo -i -v /home/raghav/MongoDB_Files/Clinical_Metagenomics_2015_Fall/patient_data:/data/ -c "/data/182V2B/"

## Remove any containers not running
#docker rm `docker ps -aq`
