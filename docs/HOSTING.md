# HOSTING

## Requirements

The requirements for rinning the bot differs depending on how you want to host the bot.
For more permanent setups, i recommend hosting as a container with docker or podman.

### Requirements for Running dockerized

Docker:

```bash
# Install from repo or directly from docker.com
# https://docs.docker.com/engine/install/ubuntu/
sudo apt update \
&& sudo apt install -y \
                docker.io 
```

podman:
podman also works, its an easy way to run in WSL due to systemd. [podman.io](https://podman.io/)

```bash
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

[podman systemd examples](https://docs.podman.io/en/latest/markdown/podman-generate-systemd.1.html#examples)

### Requirements for Running manually - Linux/WSL

```bash
sudo apt update \
&& sudo apt install -y \
                python3 \
                python3-venv \
                python3-pip \

```

#### Virtual Environment

If you know your way around, you can adopt these steps for Windows as well.

```bash
mkdir venv \
  && python3.10 -m venv venv \
  && source venv/bin/activate \
  && pip3 install -r requirements.txt
```

## CONFIGURATION

Create a ```app/.env``` file based on ```app/.env.example```
generate an api token from [discord's developer portal](https://discord.com/developers/).
Join bot to your discord server from the developer portal.

## Running the bot

### Run Manually

```bash
cd ~/git/eon-bot
source venv/bin/activate
python3 app/main.py
```

### Run Docker container

make sure you have docker prereqs.

#### Scripted build/startup

```bash
chmod +x start_dockerized.sh
./start_dockerized.sh
```

#### Building and Run Manually

```bash
# Build
docker build . -t eon-bot:1.4.0
# Run
docker run -d \
 --mount type=bind,source=$PWD/app/.env,target=/eon-bot/app/.env,readonly \
 --restart unless-stopped \
 --name eon-bot \
 eon-bot:1.4.0

```

### Running on Windows - pre built EXE

I do not run the bot this way. I found out there was a request for it, so i attempted to build an exe.
The data structure is similar but a bit different. Do not forget to configure your ```.env``` file

```bash
.
└── eon-bot
    ├── app
    │   └── data
    │       ├── activities.json
    │       └── helmgast
    │           ├── data_en-us.sqlite3
    │           └── data_se-sv.sqlite3
    ├── .env
    ├── .env.example
    └── eon-bot.exe
```

Open a powershell window, browse to the directory of the binary. If .env is configured correctly, the bot should start up.

```powershell
PS C:\eon-bot> .\eon-bot.exe
Logged in as kraken#7813
Latency is 0.12604310002643615
Activity is playing: with cosmic demons
Debug is False
```
