from datetime import datetime
import os
from pathlib import Path

from dotenv import load_dotenv
import requests

import constants
from fetch_image import fetch_image


def fetch_epic_nasa_images(epic_img_dir: str, nasa_api_key: str,
                           epic_nasa_count: int):
    """
    Получает Earth Polychromatic Imaging Camera (EPIC) с сайта NASA
    и помещает их в указанную папку.
    """

    epic_nasa_api_url = 'https://api.nasa.gov/EPIC/'
    params = {'api_key': nasa_api_key}

    response = requests.get(f'{epic_nasa_api_url}api/natural', params=params)
    response.raise_for_status()

    img_descriptions = response.json()
    imgs_count = min(len(img_descriptions), epic_nasa_count)
    epic_nasa_archive_url = f'{epic_nasa_api_url}archive/natural/'
    file_ext = '.png'

    for number, description in enumerate(img_descriptions[:imgs_count], 1):
        date_time = datetime.fromisoformat(description['date'])
        img_date = f'{date_time:%Y}/{date_time:%m}/{date_time:%d}'
        img_filename = f'{description["image"]}{file_ext}'
        img_url = f'{epic_nasa_archive_url}{img_date}/png/{img_filename}'
        img_name = f'epic_nasa_{number}'
        fetch_image(img_url, epic_img_dir, img_name, params)


def main():
    load_dotenv()
    img_dir = os.getenv('IMAGES_DIRECTORY',
                        default=constants.DEFAULT_IMAGES_DIRECTORY)

    try:
        nasa_api_key = os.environ['NASA_API_KEY']
    except KeyError:
        print('Не задана переменная окружения NASA_API_KEY в файле .env.')
        return

    epic_nasa_count = int(os.getenv('EPIC_NASA_COUNT',
                                    default=constants.DEFAULT_EPIC_NASA_COUNT))

    epic_img_dir = (Path.cwd() / img_dir / constants.EPIC_IMAGES_SUBDIR)

    fetch_epic_nasa_images(epic_img_dir, nasa_api_key, epic_nasa_count)


if __name__ == '__main__':
    main()
