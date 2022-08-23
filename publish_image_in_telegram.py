import argparse
import os
import random

from dotenv import load_dotenv
import telegram


def create_parser():
    """ Создаёт парсер параметров командной строки. """
    parser = argparse.ArgumentParser(
            description='Публикует указанную или случайную (если не указана) '
                        'фотографию в telegram-канале.'
    )
    parser.add_argument(
        'image_filename',
        nargs='?',
        help='имя файла с фото'
    )
    return parser


def publish_image_in_telegram(
        telegram_bot_token: str, telegram_channel_id: str,
        images_directory: str, image_filename: str = ''):
    """
    Публикует указанную или случайную (если не указана) фотографию
    в указанном telegram-канале с помощью указанного telegram-бота.
    """

    if not image_filename:
        image_filename = random.choice(os.listdir(images_directory))
    image_filepath = os.path.join(images_directory, image_filename)

    bot = telegram.Bot(token=telegram_bot_token)
    try:
        bot.send_document(chat_id=telegram_channel_id,
                          document=open(image_filepath, 'rb'))
        return True
    except FileNotFoundError as ex:
        print(ex)
        print(f'Введён неправильный путь или имя файла с фото.')
        return False


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY')
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID')

    parser = create_parser()
    args = parser.parse_args()

    image_filename = ''
    if args.image_filename:
        image_filename = args.image_filename

    publish_image_in_telegram(telegram_bot_token, telegram_channel_id,
                              images_directory, image_filename)

if __name__ == '__main__':
    main()
