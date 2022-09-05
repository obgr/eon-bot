# eon-bot
Discord dice roller bot for Eon, a tabletop RPG by Helmgast.
Rolls regular dice as well as whats known as an ob die (d6/t6) or infinite die (replace rolled six with two additional dice).

Written for python 3.10

## Requirements
You can run manually or in a container.
### Requirements for Running dockerized
Docker:
```
# Install from repo or directly from docker.com
# https://docs.docker.com/engine/install/ubuntu/
sudo apt update \
&& sudo apt install -y \
                docker.io 
```

podman:
podman also works, its an easy way to run in WSL due to systemd. https://podman.io/
```
sudo apt update \
&& sudo apt install -y \
                podman \
                podman-docker

# You can now run docker commands "with podman".
$ podman --version
podman version 3.4.4
$ docker --version
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
podman version 3.4.4
```
For Autostarting podman containers generate a systemd init file with ```podman generate systemd```

https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html#examples

### Requirements for Running manually
```
sudo apt update \
&& sudo apt install -y \
                python3 \
                python3-venv \
                python3-pip \

```

## Virtual Environment
```
mkdir venv
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 -m pip install -U py-cord --pre
```

# CONFIGURATION!
write a .env file based from src/.env.example
generate an api token from [discord's developer portal](https://discord.com/developers/).
Join bot to your discord server from the developer portal.

https://discord.com/developers/

# RUN 

## Run Manually
```
cd ~/git/eon-bot
source venv/bin/activate
python3 src/main.py
```

## Run Docker container
make sure you have docker prereqs.
### Scripted build/startup
```
chmod +x start_dockerized.sh
./start_dockerized.sh
```

### Manual

```
# Build
docker build . -t eon-bot:1.2.0
# Run
docker run -d \
 --mount type=bind,source=$PWD/src/.env,target=/app/src/.env,readonly \
 --restart unless-stopped \
 --name eon-bot \
 eon-bot:1.2.0

```

# Using the bot.
Slash commands! You may use discord's slash commands in order to use the bot.

## Syntax
### /roll
Format has to be in NtN+N, NtN, NdN+N or NdN.

Can also be written with capital letters: ie NT6+N

Example
```
# Regular scalable dice
/roll 1d100
/roll 2T20+2
/roll 3d6+3
```

### /ob
Format has to be in Nt6+N, Nt6, Nd6+N or Nd6.

if anything else than a 6 is supplied, it will be ignored. T6/D6 dice are hardcoded for the ob dice.

Can also be written with capital letters: ie NT6+N

Example
```
# ob dice
/ob 1t6
/ob 2T6+2
/ob 4d6+3

# This example will still use a six sided die.
/ob 4t8 

```

### /fight
Will roll several dice for use in a fight.
User runs /fight <diceroll of weapon> <Where to hit. normal/high/low N/H/L>
Outputs:
ob result
qt100 hit table result

possible value lookup for t100 if supplied.