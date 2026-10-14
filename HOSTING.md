# HOSTING.md

- [HOSTING.md](#hostingmd)
  - [Requirements](#requirements)
    - [Requirements for Running dockerized](#requirements-for-running-dockerized)
    - [Requirements for Running manually - Linux/WSL](#requirements-for-running-manually---linuxwsl)
      - [Virtual Environment](#virtual-environment)
  - [Configuration](#configuration)
  - [Running the bot](#running-the-bot)
    - [Run Manually](#run-manually)
    - [Docker Compose (recommended)](#docker-compose-recommended)
      - [Run multiple instances](#run-multiple-instances)
      - [Legacy launcher](#legacy-launcher)
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

### Docker Compose (recommended)

Docker Compose is the recommended way to deploy the bot. From the repository root, create and edit the environment file used by the default `bot1` service:

```bash
cp app/.env.example app/.env1
```

Start or update the service (this builds the image if needed):

```bash
docker compose up -d --build
```

Common service operations:

```bash
docker compose logs -f bot1
docker compose stop bot1
docker compose start bot1
docker compose restart bot1
docker compose down
```

`stop` keeps the container so `start` can bring it back. `down` stops and removes the Compose containers and network; it does not delete the image.

#### Run multiple instances

Each service can use its own environment file. To use a different file for `bot1`, set `BOT1_ENV_FILE` when invoking Compose:

```bash
BOT1_ENV_FILE=app/.env-production docker compose up -d --build bot1
BOT1_ENV_FILE=app/.env-production docker compose logs -f bot1
BOT1_ENV_FILE=app/.env-production docker compose stop bot1
```

The Compose file also includes commented `bot2` and `bot3` examples. Uncomment the services you need, create their environment files (for example, `app/.env2`), and use the matching variable such as `BOT2_ENV_FILE=app/.env2`. Each service runs under its own Compose service name.

#### Legacy launcher

`start_dockerized.sh` is retained for the legacy direct Docker/Podman workflow. For new deployments, use the Compose commands above.

```bash
./start_dockerized.sh
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