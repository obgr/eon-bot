# eon-bot
<img src="images/logo.png" >

Discord dice roller bot for Eon, a tabletop RPG by Helmgast.
Rolls regular dice as well as whats known as an ob die (d6/t6) or infinite die (replace rolled six with two additional dice).

Written for python 3.10

# Licencing and acknowledgements
The project is published under the [MIT Licence](LICENSE.md).

The data bundled in [app/data/helmgast/](app/data/helmgast/) is created and owned by Helmgast AB.</br>
Permission has been granted by representatives of Helmgast AB to extract the hit table & damage table data from the books and bundle them in this project.

# Usage

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
mkdir venv \
  && python3.10 -m venv venv \
  && source venv/bin/activate \
  && pip3 install -r requirements.txt \
  && python3 -m pip install -U py-cord --pre
```

# CONFIGURATION!
Create a ```app/.env``` file based on ```app/.env.example```
generate an api token from [discord's developer portal](https://discord.com/developers/).
Join bot to your discord server from the developer portal.

https://discord.com/developers/

# RUN 

## Run Manually
```
cd ~/git/eon-bot
source venv/bin/activate
python3 app/main.py
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
docker build . -t eon-bot:1.4.0
# Run
docker run -d \
 --mount type=bind,source=$PWD/app/.env,target=/eon-bot/app/.env,readonly \
 --restart unless-stopped \
 --name eon-bot \
 eon-bot:1.4.0

```

# Using the bot.
Slash commands! You may use discord's slash commands in order to use the bot.

## Syntax
### /about - About
eon-bot will send a link to the Github page.

### /cs - Change status
eon-bot will change it's status to a random preset.

### /dm - Direct message
eon-bot will send a direct message to the user.
Useful for secret dice rolls or lookups.

### /Ping - send Latency
eon-bot will send a message containing the ping of the bot.

### /roll - Scalable dice
Format has to be in NtN+N, NtN, NdN+N or NdN.

Can also be written with capital letters: ie NT6+N

Example
```
# Regular scalable dice
/roll 1d100
/roll 2T20+2
/roll 3d6+3

Output example:

```

### /ob or /inf - Infinite dice
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
/ob 4t8 +3

Output example:
Rolled : 4T6+3
No. Sixes.... : 2
Rolls............ : 2, 1, 3, 3, 4, 4+ 3
Total............ : 20
```

### /fight - Fight assistant
Will roll ob +t100 dice for use in a fight.
User runs ```/fight <diceroll of weapon> <weapon_type> <aim> ```

Example:
```
/fight 2t6+2 range

Output example:
OB Sixes ....: 1
OB Rolls ....: 5️⃣,2️⃣,5️⃣+ 2
OB Total ....: 14
D100 Total : 94

Aim: normal
Weapon type: range
Target: Höger ben, Vad
d100 Total...: 35
```

### /lookup - Lookup hit tables
Work in progress - for now hit tables, damage tables to be added.
Supply your weapon type, aim (will rename this, normal, high, low) and the value of a rolled t100 and get where you hit.

Example:
```
/lookup <weapon_type> <aim> <t100>

weapon_type : slash/blunt/range/pierce
        or  : s/b/r/p
target      : normal/high/low
        or  : n/h/l
t100        : 1-100

Output example:
Command : /lookup weapon_type:r aim:l, t100:7
Target  : Torso, Bröstkorg

```

# Limitations
This bot is limited by the size of discord messages as well as sizes of some data types. Therefor, by design of the infinite dice, you may reroll a d6 500 times and hit these limits.


This is a known bug.

Accidentally summoning a cosmic horror monster on the outskirts of a semi-large town is not always appreciated by the dungeon master.

