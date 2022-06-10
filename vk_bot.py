import os
import random

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from utils.dialogflow_helper import get_fullfilment_text
from utils.telegram_logger import create_tg_logger


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

    logger = create_tg_logger()

    vk_session = VkApi(token=os.getenv('VK_TOKEN'))
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                dialogflow_echo(event, vk_api)
            except Exception:
                logger.exception('An exception was raised while handling an event')


if __name__ == '__main__':
    main()
