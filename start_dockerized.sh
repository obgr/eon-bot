#!/bin/bash
# Vars
CONTAINERNAME="eon-bot"
IMAGEVERSION="1.4.0"

# Stop and Remove running bot
docker stop ${CONTAINERNAME}
docker rm ${CONTAINERNAME}
# Delete built image if same IMAGEVER
docker rmi ${CONTAINERNAME}:${IMAGEVERSION}
# Build Image
docker build . --no-cache -t ${CONTAINERNAME}:${IMAGEVERSION}
# Run Image
docker run -d \
 --mount type=bind,source=$PWD/app/.env,target=/eon-bot/app/.env,readonly \
 --restart unless-stopped \
 --name ${CONTAINERNAME} \
 ${CONTAINERNAME}:${IMAGEVERSION}
 