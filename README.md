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

Profit?

## Credits
[SallyBot](https://github.com/DeSinc/SallyBot) - DeSinc's sally bot, my main inspiration for the bot  
[Sally.py](https://github.com/whois-hoeless/Sally.py) - whois-hoeless' port of SallyBot, little bits of prompting used in cogs/carl.py