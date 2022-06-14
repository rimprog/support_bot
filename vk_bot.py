import os
import random
import logging

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Bot
from dotenv import load_dotenv

from utils.dialogflow_helper import get_fullfilment_text
from utils.telegram_logger import TelegramLogsHandler


logger = logging.getLogger('Telegram logger')


def dialogflow_echo(event, vk_api):
    text, is_fallback = get_fullfilment_text(
        os.getenv('GOOGLE_PROJECT_ID'),
        event.user_id,
        event.text,
        'ru'
    )

    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1,1000)
        )


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

    vk_session = VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                dialogflow_echo(event, vk_api)
            except Exception:
                logger.exception('An exception was raised while handling vkontakte event:')


if __name__ == '__main__':
    main()
