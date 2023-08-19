#!/bin/sh

# Functions
source_venv() {
   . /eon-bot/venv/bin/activate
}

start_bot() {
   # Start Bot
   echo "Starting $FILE."
   python3 -u $FILE
}

# Variables
FILE=app/main.py

pwd
if [ -f $FILE ]; then
   echo "File $FILE exists."
   source_venv
   start_bot
else
   echo "File $FILE does not exist."
   echo "Exiting"
   exit
fi
