from pathlib import Path
import random


def get_filepaths(dirpath: str, recursive: bool = False) -> list:
    pathlib_dirpath = Path(dirpath)                                  
    if not pathlib_dirpath.is_dir():
        return []

    filepaths = []
    for path in pathlib_dirpath.iterdir():
        if path.is_file():
            filepaths.append(path)
        elif recursive and path.is_dir():
            filepaths.extend(get_filepaths(str(path), recursive))
    return filepaths


def get_good_random_file(dirpaths: list, bad_filepaths: set) -> str:
    filepaths = []
    for dirpath in dirpaths:
        filepaths.extend(get_filepaths(dirpath))

    good_filepaths = list(set(filepaths) - set(bad_filepaths))
    if not good_filepaths:
        return ''

    return random.choice(good_filepaths)


def get_random_file(dirpath: str, recursive: bool = False) -> str:
    filepaths = get_filepaths(dirpath, recursive)
    if not filepaths:
        return ''

    return random.choice(filepaths)
