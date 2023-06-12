# CarlBot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rwf93/CarlBot/blob/master/LICENSE)

CarlBot is a discord bot used for interacting with the Vladmandic's [Stable Diffusion Web UI](https://github.com/vladmandic/automatic) fork and oobabooga's [text-generation-webui](https://github.com/oobabooga/text-generation-webui).

## Installation

Copy the .env.sample to .env and populate it with the requirered values.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the deps.

```bash
python -m venv venv
pip install -r requirements.txt
```
### Windows
```
python main.py
```
### *NIX
```
python3 main.py
```

## Docker

You can use the docker-compose:  
```
docker compse up
```

or alternatively pull the [prebuilt container](https://github.com/rwf93/CarlBot/pkgs/container/carlbot): 

```
docker pull ghcr.io/rwf93/carlbot:master
docker --env-file .env run ghcr.io/rwf93/carlbot:master
```

Note: for passing in endpoints to either Stable Diffusion or oobabooga, use 172.17.0.1 if using docker or 10.88.0.1 if using podman.  

This is because the host machine isn't accessed by using the local loopback address as that is reserved for referencing the container.

Profit?

## Credits
[SallyBot](https://github.com/DeSinc/SallyBot) - DeSinc's sally bot, my main inspiration for the bot  
[Sally.py](https://github.com/whois-hoeless/Sally.py) - whois-hoeless' port of SallyBot, little bits of prompting used in cogs/carl.py