from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from telegram_bot.handlers.base.private_handler import PrivateHandler
from telegram_bot.service.db_service import DBService


class ListFoodHandler(PrivateHandler):
    def __init__(self, db_service: DBService) -> None:
        super().__init__()
        self.db_service = db_service

    async def _handle(self, update: Update, context: CallbackContext) -> None:
        limit = context.args[0] if context.args else 10
        reply = ["List of drugs 💊\n"]
        for log_entry in self.db_service.list_drug_logs(limit):
            reply.append(f"[{log_entry.datetime}] {log_entry.drug_name} * {log_entry.dosage}")

        await update.message.reply_text("\n".join(reply))


def get_list_drugs_command(db_service: DBService) -> CommandHandler:
    return CommandHandler("list_drugs", ListFoodHandler(db_service).handle)
