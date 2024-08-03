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
        reply = ["List of food 🍣\n"]
        for food_log_entry in self.db_service.list_food_logs(limit):
            reply.append(
                f"[{food_log_entry.datetime}] {food_log_entry.name}\n- {food_log_entry.protein} protein"
                f"\n- {food_log_entry.carbs} carbs\n- {food_log_entry.fats} fats"
                f"\n- Comment: {food_log_entry.comment}\n"
            )

        await update.message.reply_text("\n".join(reply))


def get_list_food_command(db_service: DBService) -> CommandHandler:
    return CommandHandler("list_food", ListFoodHandler(db_service).handle)
