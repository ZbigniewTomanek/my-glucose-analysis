import os
from pathlib import Path

from loguru import logger
from telegram import Update
from telegram.ext import Application

from telegram_bot.handlers.commands.list_drug_command import get_list_drugs_command
from telegram_bot.handlers.commands.list_food_command import get_list_food_command
from telegram_bot.handlers.conversations.log_drug_conversation import get_drug_log_handler
from telegram_bot.handlers.conversations.log_food_conversation import get_food_log_handler
from telegram_bot.handlers.messages.default_message_handler import get_default_message_handler
from telegram_bot.service.db_service import DBService

OUT_DIR = Path(__file__).parent.parent / "out"


def setup_logger() -> None:
    log_dir_path = OUT_DIR / "log"
    log_dir_path.mkdir(parents=True, exist_ok=True)

    logger.add(log_dir_path / "debug.log", rotation="100MB", retention="7 days", level="DEBUG")
    logger.add(log_dir_path / "error.log", rotation="100MB", retention="7 days", level="ERROR")
    logger.info("logger initialized")


def build_app() -> Application:
    bot_token = os.getenv("TELEGRAM_BOT_API_KEY")
    if bot_token is None:
        raise ValueError("TELEGRAM_BOT_API_KEY env var was not set")

    read_timeout = int(os.getenv("READ_TIMEOUT_S"), 30)
    write_timeout = int(os.getenv("WRITE_TIMEOUT_S"), 30)
    app = (
        Application.builder()
        .token(bot_token)
        .concurrent_updates(True)
        .read_timeout(read_timeout=read_timeout)
        .write_timeout(write_timeout=write_timeout)
        .build()
    )
    return app


def main() -> None:
    setup_logger()

    app = build_app()
    db_service = DBService(out_dir=OUT_DIR)

    app.add_handler(get_food_log_handler(db_service))
    app.add_handler(get_drug_log_handler(db_service))
    app.add_handler(get_list_food_command(db_service))
    app.add_handler(get_list_drugs_command(db_service))
    app.add_handler(get_default_message_handler())

    logger.info("Starting polling")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
