import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

import constants
from fetch_image import fetch_image


def create_parser():
    """ Создаёт парсер параметров командной строки. """

    parser = argparse.ArgumentParser(
            description='Получает с сайта SpaceX фотографии конкретного '
                        'запуска ракеты, если на вход дан id этого запуска. '
                        'Получает с сайта SpaceX фотографии последнего '
                        'из запусков, для которого имеются фотографии, '
                        'если id запуска не указан.'
    )
    parser.add_argument(
        'launch_id',
        nargs='?',
        help='id нужного запуска для скачивания фото из него'
    )
    return parser


def fetch_spacex_launch(spacex_img_dirpath: str, launch_id: str):
    """
    Получает с сайта SpaceX фотографии для запуска с заданным ID
    и помещает их в указанную папку.
    """

    response = requests.get('https://api.spacexdata.com/v5/launches/'
                            f'{launch_id}')
    response.raise_for_status()

    if img_urls := response.json()['links']['flickr']['original']:
        for number, url in enumerate(img_urls, 1):
            img_name = f'spacex_{number}'
            fetch_image(url, spacex_img_dirpath, img_name)


def fetch_spacex_last_launch(img_dir: str):
    """
    Получает с сайта SpaceX фотографии последнего из запусков, для которого
    имеются фотографии, и помещает их в указанную папку.
    """

    spacex_api_url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(f'{spacex_api_url}/latest')
    response.raise_for_status()

    if not (img_urls := response.json()['links']['flickr']['original']):
        response = requests.get(spacex_api_url)
        response.raise_for_status()

        launches = response.json()
        for launch in launches[::-1]:
            if img_urls := launch['links']['flickr']['original']:
                break

    if img_urls:
        for img_number, img_url in enumerate(img_urls, 1):
            img_name = f'spacex_{img_number}'
            fetch_image(img_url, img_dir, img_name)


def main():
    load_dotenv()
    img_dir = os.getenv('IMAGES_DIRECTORY',
                        default=constants.DEFAULT_IMAGES_DIRECTORY)

    parser = create_parser()
    args = parser.parse_args()

    spacex_img_dirpath = Path.cwd() / img_dir / constants.SPACEX_IMAGES_SUBDIR
    if args.launch_id:
        fetch_spacex_launch(spacex_img_dirpath, args.launch_id.strip())
        return

    fetch_spacex_last_launch(spacex_img_dirpath)


if __name__ == '__main__':
    main()
