#!/bin/bash
# Vars
ENVPATH="app/.env"
CONTAINERNAME="eon-bot"
IMAGEVERSION="1.4.1"

# Color variables
red='\033[0;31m'
green='\033[0;32m'
yellow='\033[0;33m'
blue='\033[0;34m'
magenta='\033[0;35m'
cyan='\033[0;36m'
# Clear the color
clear='\033[0m'

# Check if script runs as root
if [ "$EUID" -ne 0 ]
then
    echo -e "${yellow}Not running as root${clear}"
    echo "assuming user has access to files and to docker socket if running docker."
    echo
else
    echo "Running script as ${cyan}root${clear}"
    echo
fi


# Check if podman (and podman-docker) or docker is installed
echo "Looking for a container runtime"
if command -v podman &> /dev/null
then
    echo "podman found"
    CONTAINERRUNTIME="podman"
elif command -v docker &> /dev/null
then
    echo "docker found"
    CONTAINERRUNTIME="docker"
else
    echo "No Container runtime found. please install docker or podman"
fi
echo

# Check if inventory file exists
if [ -f "$ENVPATH" ]; then
    echo "$ENVPATH exists."
else 
    echo "$ENVPATH does not exist."
    echo "Creating from example file"
    cp $ENVPATH.example $ENVPATH
    echo "Please edit ${ENVPATH}, the bot will not work without a token."
    read -p "Press enter to continue"
fi
echo

# Stop and Remove running bot
echo "Stopping eon-bot if running with same name."
$CONTAINERRUNTIME stop ${CONTAINERNAME}
echo "Removing eon-bot container."
$CONTAINERRUNTIME rm ${CONTAINERNAME}

# Delete built image if same IMAGEVER
echo "Deleting image if image exists with the same tag."
$CONTAINERRUNTIME rmi ${CONTAINERNAME}:${IMAGEVERSION}

# Build Image
echo "Building image"
$CONTAINERRUNTIME build . --no-cache -t ${CONTAINERNAME}:${IMAGEVERSION}

# Run Image
echo "Run image"
$CONTAINERRUNTIME run -d \
 --mount type=bind,source=$PWD/app/.env,target=/eon-bot/app/.env,readonly \
 --restart unless-stopped \
 --name ${CONTAINERNAME} \
 ${CONTAINERNAME}:${IMAGEVERSION}

# Sleep 3 seconds
sleep 3

# Print running containers
echo "Container status"
$CONTAINERRUNTIME ps -a