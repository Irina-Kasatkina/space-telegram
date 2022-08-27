import os
import pathlib
import time

from dotenv import load_dotenv

import constants
from publish_image_in_telegram import publish_image_in_telegram
from get_files import get_good_random_file


def publish_all_images_in_telegram(
        telegram_bot_token: str, telegram_channel_id: str,
        img_dirs: list, delay_in_seconds: int):
    """
    Публикует все фотографии из заданной директории
    в указанном telegram-канале с помощью указанного telegram-бота.
    """

    published_filepaths = set()

    while True:
        img_filepath = get_good_random_file(img_dirs, published_filepaths)
        if not img_filepath:
            return True

        if not publish_image_in_telegram(telegram_bot_token,
                                         telegram_channel_id,
                                         img_filepath):
            return False

        published_filepaths.add(img_filepath)
        time.sleep(delay_in_seconds)


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY',
                                 default=constants.DEFAULT_IMAGES_DIRECTORY)

    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    telegram_channel_id = os.environ['TELEGRAM_CHANNEL_ID']

    delay_in_seconds = int(os.getenv('DELAY_IN_SECONDS',
                                     default=constants.DEFAULT_DELAY_IN_SECONDS))

    images_directories = [
            pathlib.Path.cwd() / images_directory / constants.SPACEX_IMAGES_SUBDIR,
            pathlib.Path.cwd() / images_directory / constants.APOD_IMAGES_SUBDIR,
            pathlib.Path.cwd() / images_directory / constants.EPIC_IMAGES_SUBDIR,
    ]

    while True:
        if not publish_all_images_in_telegram(telegram_bot_token,
                                              telegram_channel_id,
                                              images_directories,
                                              delay_in_seconds):
            return


if __name__ == '__main__':
    main()
