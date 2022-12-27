# HOSTING.md

- [HOSTING.md](#hostingmd)
  - [Requirements](#requirements)
    - [Requirements for Running dockerized](#requirements-for-running-dockerized)
    - [Requirements for Running manually - Linux/WSL](#requirements-for-running-manually---linuxwsl)
      - [Virtual Environment](#virtual-environment)
  - [Configuration](#configuration)
  - [Running the bot](#running-the-bot)
    - [Run Manually](#run-manually)
    - [Run Docker container](#run-docker-container)
      - [Scripted build/startup](#scripted-buildstartup)
      - [Building and Run Manually](#building-and-run-manually)
    - [Running on Windows - pre built EXE](#running-on-windows---pre-built-exe)
      - [Notes](#notes)

## Requirements

The requirements for running the bot differs depending on how you want to host the bot.
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

## Configuration

In order configure the bot, we use an ```.env``` file (environment file).
This file contains settings that the application uses. As an example, the discord token or api token is sensitive credentials that we do not want to spread on the internet, so instead of hardcoding the token into the bot, allow it for configuration in the ```.env``` file.

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

There are two ways of starting the bot
If you want to see the output if the app craches (or if unconfigured):

- open a powershell window, browse to the directory of the binary and start ```eon-bot.exe```. If .env is configured correctly, the bot should start up.

If you already configured the .env file correctly (if you have not configured the bot correctly, the window will just close)

- Double click ```eon-bot.exe```


```powershell
PS C:\eon-bot> .\eon-bot.exe
Logged in as kraken#7813
Latency is 0.12604310002643615
Activity is playing: with cosmic demons
Debug is False
```

#### Notes

I have noticed that sometimes anti virus software marks Pyinstaller packaged exe files as malicious.
This is known. If this happens, you might need to manually allow it.
The code is not digitally signed.

I recommend you to run eon-bot as container since it runs isolated and you have the possibillity to inspect the code in a raw format.
The exe is created for convenience.