import os

from dotenv import load_dotenv
import requests

from fetch_image import fetch_image


def fetch_nasa_epic(images_directory: str, nasa_api_key: str):
    """
    Получает Earth Polychromatic Imaging Camera (EPIC) с сайта NASA
    и помещает их в указанную папку.
    """

    nasa_epic_api_url = 'https://api.nasa.gov/EPIC/'
    params = {'api_key': nasa_api_key}

    response = requests.get(f'{nasa_epic_api_url}api/natural', params=params)
    response.raise_for_status()

    epic_images = response.json()
    images_count = min(len(epic_images), 5)
    nasa_epic_archive_url = f'{nasa_epic_api_url}archive/natural/'
    file_extension = '.png'

    for epic_number, epic_image in enumerate(epic_images[:images_count], 1):
        image_date = epic_image['date'][:10].replace('-', '/')
        image_filename = f'{epic_image["image"]}{file_extension}'
        image_url = f'{nasa_epic_archive_url}{image_date}/png/{image_filename}'
        image_name = f'nasa_epic_{epic_number}'
        fetch_image(image_url, images_directory, image_name, params)


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY')
    nasa_api_key = os.getenv('NASA_API_KEY')

    fetch_nasa_epic(images_directory, nasa_api_key)


if __name__ == '__main__':
    main()
