import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv

from dialogflow_helper import get_fullfilment_text


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

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dialogflow_echo_handler = MessageHandler(Filters.text & (~Filters.command), dialogflow_echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialogflow_echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
