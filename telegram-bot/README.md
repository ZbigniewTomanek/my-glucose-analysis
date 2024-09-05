# telegram-bot

This is a code of telegram bot which I used to log my food and drug data and store it in a sqlite database. It was deployed as a poetry project run by as systemd service on my Raspberry Pi 3B.

## Installation

1) Create .env file with the following content (use [botfather](https://telegram.me/BotFather) to get the API key):
```
TELEGRAM_BOT_API_KEY='<API KEY>'
MY_TELEGRAM_USER_ID='<USER_ID>'
READ_TIMEOUT_S=30
WRITE_TIMEOUT_S=30
```
2) [Install poetry](https://python-poetry.org/docs/)
3) Run `poetry install` to install dependencies
4) Run `run-as-systemd-service.sh` to run the bot as a systemd service called `my-telegram-bot.service`

### Available commands

 - `/log_food` - log the food entry
 - `/list_food` - list recent food entries
 - `/log_drug` - log the drug entry
 - `/list_drugs` - list recent drug entries