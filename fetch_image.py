import os
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def fetch_image(img_url: str, img_dir: str,
                img_name: str, request_params=None):
    """
    Получает картинку по указанному url и помещает её в указанную папку.
    """

    response = requests.get(img_url, params=request_params)
    response.raise_for_status()

    Path(img_dir).mkdir(parents=True, exist_ok=True)

    filename = f'{img_name}{get_file_extension(img_url)}'
    filepath = Path(img_dir) / filename

    with open(filepath, "wb") as file:
        file.write(response.content)


def get_file_extension(url: str) -> str:
    """ Выделяет расширение файла из заданной строки url. """

    filepath_from_url = urlsplit(url).path
    file_ext = os.path.splitext(filepath_from_url)[1]
    decoded_file_ext = unquote(file_ext)
    return decoded_file_ext
