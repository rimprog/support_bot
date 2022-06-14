import os
import logging

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv

from utils.dialogflow_helper import get_fullfilment_text
from utils.telegram_logger import TelegramLogsHandler


logger = logging.getLogger('Telegram logger')


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling telegram update:", exc_info=context.error)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def dialogflow_echo(update: Update, context: CallbackContext):
    text, is_fallback = get_fullfilment_text(
        os.getenv('GOOGLE_PROJECT_ID'),
        update.effective_chat.id,
        update.message.text,
        'ru'
    )

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main():
    load_dotenv()

    telegram_logger_bot_token = os.getenv('TELEGRAM_LOGGER_BOT_TOKEN')
    developer_chat_id = os.getenv('TELEGRAM_DEVELOPER_USER_ID')

    logger_tg_bot = Bot(token=telegram_logger_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logger_tg_bot, developer_chat_id))

    updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dialogflow_echo_handler = MessageHandler(Filters.text & (~Filters.command), dialogflow_echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialogflow_echo_handler)

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
