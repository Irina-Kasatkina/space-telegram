import os
import pathlib
from urllib.parse import urlsplit, unquote

from dotenv import load_dotenv
import requests


def fetch_image(image_url: str, images_directory: str,
                image_name: str, request_params=None):
    if not request_params:
        request_params = {}

    response = requests.get(image_url, request_params)
    response.raise_for_status()

    pathlib.Path(images_directory).mkdir(parents=True, exist_ok=True)

    file_extension = get_file_extension(image_url)
    filepath = f'{images_directory}/{image_name}{file_extension}'

    with open(filepath, "wb") as file:
        file.write(response.content)


def fetch_nasa_apod(images_directory: str, nasa_api_key: str):
    """
    Fetch NASA Astronomy Pictures of the Day (APOD)
    and save them in image directory.
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
        if not (image_url:=apod_image.get('url')):
            continue

        if get_file_extension(image_url):
            apod_number += 1
            image_name = f'nasa_apod_{apod_number}'
            fetch_image(image_url, images_directory, image_name)


def fetch_nasa_epic(images_directory: str, nasa_api_key: str):
    """
    Fetch NASA Earth Polychromatic Imaging Camera (EPIC) pictures
    and save them in image directory.
    """

    nasa_epic_api_url = 'https://api.nasa.gov/EPIC/'
    params = {'api_key': nasa_api_key}

    response = requests.get(f'{nasa_epic_api_url}api/natural', params=params)
    response.raise_for_status()

    epic_images = response.json()
    images_count = min(len(epic_images), 5)
    nasa_epic_archive_url = f'{nasa_epic_api_url}archive/natural/'
    file_extension = '.png'

    for epic_number, epic_image in enumerate(epic_images[:images_count]):
        image_date = epic_image['date'][:10].replace('-', '/')
        image_filename = f'{epic_image["image"]}{file_extension}'
        image_url = f'{nasa_epic_archive_url}{image_date}/png/{image_filename}'
        image_name = f'nasa_epic_{epic_number}'
        fetch_image(image_url, images_directory, image_name, params)


def fetch_spacex_last_launch(images_directory: str):
    """ Fetch SpaceX last launch images and save them in image directory. """

    spacex_api_url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(f'{spacex_api_url}/latest')
    response.raise_for_status()

    if not (image_urls:=response.json()['links']['flickr']['original']):
        response = requests.get(spacex_api_url)
        response.raise_for_status()

        launches = response.json()
        for launch in launches[::-1]:
            if image_urls:=launch['links']['flickr']['original']:
                break

    if image_urls:
        for image_number, image_url in enumerate(image_urls, 1):
            image_name = f'spacex_{image_number}'
            fetch_image(image_url, images_directory, image_name)


def get_file_extension(url: str) -> str:
    """ Extract file extension from URL string. """

    filepath_from_url = urlsplit(url).path
    file_extension = os.path.splitext(filepath_from_url)[1]
    decoded_file_extension = unquote(file_extension)
    return decoded_file_extension


def main():
    images_directory = './images'

    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')

    fetch_spacex_last_launch(f'{images_directory}/spacex')
    fetch_nasa_apod(f'{images_directory}/nasa_apod', nasa_api_key)
    fetch_nasa_epic(f'{images_directory}/nasa_epic', nasa_api_key)


if __name__ == '__main__':
    main()
