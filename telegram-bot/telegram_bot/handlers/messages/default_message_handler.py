from typing import Any

from fortune import fortune
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters

from telegram_bot.handlers.base.private_handler import PrivateHandler


class DefaultMessageHandler(PrivateHandler):
    async def _handle(self, update: Update, context: CallbackContext) -> Any:
        await update.message.reply_text(fortune())


def get_default_message_handler() -> MessageHandler:
    return MessageHandler(filters.TEXT & ~filters.COMMAND, DefaultMessageHandler().handle)
