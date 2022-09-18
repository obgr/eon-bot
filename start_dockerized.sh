#!/bin/bash
# Vars
CONTAINERNAME="eon-bot"
IMAGEVER="1.3.0"

# Build Image
docker build . -t ${CONTAINERNAME}:${IMAGEVER}
# Run Image
docker run -d \
 --mount type=bind,source=$PWD/src/.env,target=/app/src/.env,readonly \
 --restart unless-stopped \
 ${CONTAINERNAME}:${IMAGEVER}