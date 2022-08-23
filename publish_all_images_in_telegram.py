import argparse
import os
import random
import time

from dotenv import load_dotenv
import telegram

from publish_image_in_telegram import publish_image_in_telegram


FOUR_HOURS_IN_SECONDS = 14400


def publish_all_images_in_telegram(
        telegram_bot_token: str, telegram_channel_id: str,
        images_directory: str, delay_in_seconds: int):
    """
    Публикует все фотографии из заданной директории
    в указанном telegram-канале с помощью указанного telegram-бота.
    """

    image_filenames = os.listdir(images_directory)
    random.shuffle(image_filenames)
    for image_filename in image_filenames:
        if not publish_image_in_telegram(telegram_bot_token,
                                         telegram_channel_id,
                                         images_directory,
                                         image_filename):
            break
        time.sleep(delay_in_seconds)


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')

    delay_in_seconds = 0
    try:
        delay_in_seconds = int(os.getenv('DELAY_IN_SECONDS'))
    except:
        pass

    if not delay_in_seconds:
        delay_in_seconds = FOUR_HOURS_IN_SECONDS

    while True:
        publish_all_images_in_telegram(telegram_bot_token,
                                       telegram_channel_id,
                                       images_directory,
                                       delay_in_seconds)

if __name__ == '__main__':
    main()
