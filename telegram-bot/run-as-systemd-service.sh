#!/bin/bash

service_path="/etc/systemd/system/my-telegram-bot.service"

if ! systemctl list-units --full --all | grep 'my-telegram-bot.service'; then
  echo "[Unit]
  Description=My telegram bot

  [Service]
  ExecStart=poetry run python telegram_bot/main.py
  Restart=always
  User=$(whoami)
  Group=$(whoami)
  Environment=PATH=/usr/bin:/usr/local/bin
  WorkingDirectory=$(pwd)

  [Install]
  WantedBy=multi-user.target" >$service_path

  sudo systemctl daemon-reload
  echo "Installed 'my-telegram-bot.service"
fi

echo "Start my-telegram-bot.service"
sudo systemctl enable my-telegram-bot
sudo systemctl start my-telegram-bot
