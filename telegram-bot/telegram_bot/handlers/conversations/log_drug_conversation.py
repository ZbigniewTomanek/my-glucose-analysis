from loguru import logger
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from telegram_bot.handlers.base.private_handler import PrivateHandler
from telegram_bot.service.db_service import DBService, DrugLogEntry

DRUG, DOSAGE = range(2)
drug_types = [
    ["ALA 300mg", "1 coffee", "bepis 500ml"],
    [
        "ibuprofen 400mg",
        "medikinet CR 10mg",
        "concerta 18mg",
    ],
    [
        "1 beer",
        "weed 3 pufs",
        "0,5 edible",
        "10mg amphetamine",
    ],
]


class StartHandler(PrivateHandler):
    async def _handle(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text(
            "What drug did you take? 💊",
            reply_markup=ReplyKeyboardMarkup(
                drug_types,
                one_time_keyboard=True,
                input_field_placeholder="Drug type",
            ),
        )
        return DRUG


class DrugHandler(PrivateHandler):
    async def _handle(self, update: Update, context: CallbackContext) -> int:
        name = update.message.text
        if not name:
            await update.message.reply_text("Drug name cannot be null!")
            return DRUG
        context.user_data["drug_name"] = name
        await update.message.reply_text(
            "What is the dosage multiplier?",
        )
        return DOSAGE


class DosageHandler(PrivateHandler):
    def __init__(self, db_service: DBService) -> None:
        super().__init__()
        self.db_service = db_service

    async def _handle(self, update: Update, context: CallbackContext) -> int:
        dosage = update.message.text

        try:
            dosage = int(dosage)
        except ValueError:
            await update.message.reply_text("Dosage should be int!")
            return DOSAGE

        if dosage <= 0:
            await update.message.reply_text("Dosage should be greater than 0!")
            return DOSAGE

        context.user_data["dosage"] = dosage

        self.db_service.add_drug_log_entry(DrugLogEntry(**context.user_data))
        context.user_data.clear()
        await update.message.reply_text("Entry was logged! Use /list_drugs to see your logs")
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def get_drug_log_handler(db_service: DBService) -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("log_drug", StartHandler().handle)],
        states={
            DRUG: [MessageHandler(filters.TEXT & ~filters.COMMAND, DrugHandler().handle)],
            DOSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, DosageHandler(db_service).handle)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
