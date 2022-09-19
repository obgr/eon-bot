#!/bin/bash

# Functions
source_venv() {
   . /eon-bot/venv/bin/activate
}
#get_latest_release() {
#   curl --silent "https://api.github.com/repos/$1/releases/latest" | grep -Po '"tag_name": "\K.*?(?=")' # Consult github api and grep/sed out result
#}
#download_latest_release() {
#   # Download release
#   echo "Downloading $FILE from github."
#   wget -q https://github.com/${REPO}/releases/download/${TAG}/${FILE}
#}
start_bot() {
   # Start Bot
   pwd
   echo "Starting $FILE."
   python3 -u $FILE
}

# Variables
#REPO="obgr/eon-bot"
#TAG=$(get_latest_release ${REPO})
FILE=app/main.py


if [ -f $FILE ]; then
   echo "File $FILE exists."
   source_venv
   start_bot
else
   echo "File $FILE does not exist."
   echo "Exiting"
   exit
fi