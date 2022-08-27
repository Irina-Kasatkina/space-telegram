import os
from pathlib import Path

from dotenv import load_dotenv
import requests

import constants
from fetch_image import fetch_image


def fetch_apod_nasa_images(apod_img_dirpath: str, nasa_api_key: str,
                           apod_nasa_count: int):
    """
    Получает Astronomy Pictures of the Day (APOD) с сайта NASA
    и помещает их в указанную папку.
    """

    apod_nasa_api_url = 'https://api.nasa.gov/planetary/apod'
    params = {
            'api_key': nasa_api_key,
            'count': apod_nasa_count * 2
    }

    response = requests.get(apod_nasa_api_url, params=params)
    response.raise_for_status()

    img_descriptions = [x for x in response.json()
                        if x['media_type'] == 'image' and x.get('url')]
    imgs_count = min(len(img_descriptions), apod_nasa_count)

    for number, description in enumerate(img_descriptions[:imgs_count], 1):
        img_url = description.get('url')
        img_name = f'apod_nasa_{number}'
        fetch_image(img_url, apod_img_dirpath, img_name)


def main():
    load_dotenv()
    img_dir = os.getenv('IMAGES_DIRECTORY',
                        default=constants.DEFAULT_IMAGES_DIRECTORY)

    nasa_api_key = os.environ['NASA_API_KEY']

    apod_nasa_count = int(os.getenv('APOD_NASA_COUNT',
                                    default=constants.DEFAULT_APOD_NASA_COUNT))

    apod_img_dirpath = Path.cwd() / img_dir / constants.APOD_IMAGES_SUBDIR

    fetch_apod_nasa_images(apod_img_dirpath, nasa_api_key, apod_nasa_count)


if __name__ == '__main__':
    main()
