import argparse
import os

from dotenv import load_dotenv
import requests

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


def fetch_spacex_launch(images_directory: str, launch_id: str):
    """
    Получает с сайта SpaceX фотографии для запуска с заданным ID
    и помещает их в указанную папку.
    """

    response = requests.get('https://api.spacexdata.com/v5/launches/'
                            f'{launch_id}')
    response.raise_for_status()

    if images_urls := response.json()['links']['flickr']['original']:
        for image_number, image_url in enumerate(images_urls, 1):
            image_name = f'spacex_{image_number}'
            fetch_image(image_url, images_directory, image_name)


def fetch_spacex_last_launch(images_directory: str):
    """
    Получает с сайта SpaceX фотографии последнего из запусков, для которого
    имеются фотографии, и помещает их в указанную папку.
    """

    spacex_api_url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(f'{spacex_api_url}/latest')
    response.raise_for_status()

    if not (images_urls := response.json()['links']['flickr']['original']):
        response = requests.get(spacex_api_url)
        response.raise_for_status()

        launches = response.json()
        for launch in launches[::-1]:
            if images_urls := launch['links']['flickr']['original']:
                break

    if images_urls:
        for image_number, image_url in enumerate(images_urls, 1):
            image_name = f'spacex_{image_number}'
            fetch_image(image_url, images_directory, image_name)


def main():
    load_dotenv()
    images_directory = os.getenv('IMAGES_DIRECTORY')

    parser = create_parser()
    args = parser.parse_args()

    if args.launch_id:
        fetch_spacex_launch(images_directory, args.launch_id.strip())
        return

    fetch_spacex_last_launch(images_directory)


if __name__ == '__main__':
    main()
