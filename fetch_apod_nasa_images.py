import os

from dotenv import load_dotenv
import requests

from fetch_image import fetch_image, get_file_extension


def fetch_nasa_apod(images_directory: str, nasa_api_key: str):
    """
    Получает Astronomy Pictures of the Day (APOD) с сайта NASA
    и помещает их в указанную папку.
    """

    nasa_apod_api_url = 'https://api.nasa.gov/planetary/apod'
    params = {
            'api_key': nasa_api_key,
            'count': 30
    }

    response = requests.get(nasa_apod_api_url, params=params)
    response.raise_for_status()

    apod_images = response.json()
    apod_number = 0

    for apod_image in apod_images:
        if not (image_url := apod_image.get('url')):
            continue

        if get_file_extension(image_url):
            apod_number += 1
            image_name = f'nasa_apod_{apod_number}'
            fetch_image(image_url, images_directory, image_name)


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY')
    nasa_api_key = os.getenv('NASA_API_KEY')

    fetch_nasa_apod(images_directory, nasa_api_key)


if __name__ == '__main__':
    main()
