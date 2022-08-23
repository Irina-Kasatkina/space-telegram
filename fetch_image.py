import os
import pathlib
from urllib.parse import urlsplit, unquote

import requests


def fetch_image(image_url: str, images_directory: str,
                image_name: str, request_params=None):
    """
    Получает картинку по указанному url и помещает её в указанную папку.
    """

    if not request_params:
        request_params = {}

    response = requests.get(image_url, request_params)
    response.raise_for_status()

    pathlib.Path(images_directory).mkdir(parents=True, exist_ok=True)

    file_extension = get_file_extension(image_url)
    filepath = f'{images_directory}/{image_name}{file_extension}'

    with open(filepath, "wb") as file:
        file.write(response.content)


def get_file_extension(url: str) -> str:
    """ Выделяет расширение файла из заданной строки url. """

    filepath_from_url = urlsplit(url).path
    file_extension = os.path.splitext(filepath_from_url)[1]
    decoded_file_extension = unquote(file_extension)
    return decoded_file_extension
