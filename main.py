import os

from dotenv import load_dotenv
import requests

from fetch_apod_nasa_images import fetch_nasa_apod
from fetch_epic_nasa_images import fetch_nasa_epic
from fetch_spacex_images import fetch_spacex_last_launch


def main():
    images_directory = './images'

    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')

    fetch_spacex_last_launch(f'{images_directory}/spacex')
    fetch_nasa_apod(f'{images_directory}/nasa_apod', nasa_api_key)
    fetch_nasa_epic(f'{images_directory}/nasa_epic', nasa_api_key)


if __name__ == '__main__':
    main()
