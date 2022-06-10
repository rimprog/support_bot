import os
import logging

from telegram import Bot
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def create_tg_logger():
    logger_tg_bot = Bot(token=os.getenv('TELEGRAM_LOGGER_BOT_TOKEN'))
    developer_chat_id = os.getenv('TELEGRAM_DEVELOPER_USER_ID')

    logger = logging.getLogger('Telegram logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logger_tg_bot, developer_chat_id))

    return logger


def main():
    load_dotenv()

    logger = create_tg_logger()

    try:
        1/0
    except Exception:
        logger.exception('Test exception:')


if __name__ == '__main__':
    main()
