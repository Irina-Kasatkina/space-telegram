# Загрузка в Telegram фотографий космоса

Этот проект представляет собой набор скриптов для скачивания с сервисов SpaceX и NASA фотографий космоса и загрузки их в Telegram:
- fetch_apod_nasa_images - получает <= 30 случайных фотографий Astronomy Pictures of the Day (APOD) с сайта NASA и помещает их в папку `images/nasa_apod`;
- fetch_nasa_epic - получает 5 фотографий Земли Earth Polychromatic Imaging Camera (EPIC) с сайта NASA и помещает их в папку `images/nasa_epic`;
- fetch_spacex_images - получает фотографии запуска ракеты с сайта SpaceX и помещает их в папку `images/spacex`;
- main -

## Установка

### Клонировать проект
Сделайте клонирование проекта:
```
git clone https://github.com/Irina-Kasatkina/web-api-space-telegram.git
```
или просто скопируйте все его файлы на ваш локальный диск.

### Настройка окружения

Для работы с утилитой у вас уже должен быть установлен Python 3.

Для управления зависимостями Python желательно воспользоваться [virtualenv](https://pypi.org/project/virtualenv/).

Установите пакеты с помощью `pip` (или `pip3`, есть конфликт с Python2):
```
pip install -r requirements.txt
```

### Переменные окружения

Персональный ключ – `API KEY` для взаимодействия с API NASA (для скриптов `fetch_apod_nasa_images` и `fetch_epic_nasa_images`) берётся из переменных окружения. Для определения настроек окружения создайте файл `.env` рядом с `main.py` и запишите туда такие данные: 
```
#
NASA_API_KEY={ваш_API_KEY}
```
Вместо `{ваш_API_KEY}` подставьте значение вашего `API KEY` с сервиса API NASA. Чтобы получить его, зарегистрируйтесь на сервисе [сайта NASA](https://api.nasa.gov/) и сгенерируйте там свой личный `API KEY` (там вы получите строку наподобие такой: `hg639e20ad155405123dk5677542fecf00231da7`).

## Запуск

Для запуска нужного вам скрипта наберите в командной строке одну из команд:
```
python -m fetch_apod_nasa_images
python -m fetch_epic_nasa_images
python -m fetch_spacex_images
python -m fetch_spacex_images {id_конкретного_запуска}
python -m main
```
где для скрипта `fetch_spacex_images` можно указать необязательный параметр `{id_конкретного_запуска}` - id конкретного запуска ракеты (например `5eb87d47ffd86e000604b38a`) - если этот параметр указан, то скрипт `fetch_spacex_images` получит фотографии указанного запуска, а если не указан - получит фотографии последнего из запусков, для которого имеются фотографии.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).