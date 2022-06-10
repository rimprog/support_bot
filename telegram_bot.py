import os
import json
import html
import logging
import traceback

from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters
from dotenv import load_dotenv

from utils.dialogflow_helper import get_fullfilment_text


load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__file__)

DEVELOPER_CHAT_ID = os.getenv('TELEGRAM_DEVELOPER_USER_ID')


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    logger_bot = Bot(token=os.getenv('TELEGRAM_LOGGER_BOT_TOKEN'))
    logger_bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


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
