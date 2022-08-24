# Загрузка в Telegram фотографий космоса

Этот проект представляет собой набор скриптов для скачивания с сервисов SpaceX и NASA фотографий космоса и загрузки их в Telegram:
- *fetch_apod_nasa_images* - получает не более 30 случайных фотографий Astronomy Pictures of the Day (APOD) с сайта NASA и сохраняет их на локальном компьютере;
- *fetch_nasa_epic_images* - получает 5 фотографий Земли Earth Polychromatic Imaging Camera (EPIC) с сайта NASA и сохраняет их на локальном компьютере;
- *fetch_spacex_images* - получает фотографии запуска ракеты с сайта SpaceX и сохраняет их на локальном компьютере;
- *publish_image_in_telegram* - публикует одну фотографию в telegram-канале с помощью telegram-бота;
- *publish_all_images_in_telegram* - публикует в telegram-канале все фотографии из папки с фото, делая задержку после публикации каждой фотографии.

## Установка

Для запуска скриптов вам понадобится Python третьей версии.

Скачайте код с GitHub.

Для управления зависимостями Python желательно воспользоваться [virtualenv](https://pypi.org/project/virtualenv/).

Установите зависимости с помощью `pip` (или `pip3`, есть конфликт с Python2):
```
pip install -r requirements.txt
```

### Переменные окружения

Часть настроек утилит берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в той же папке, где и скрипты, и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 5 переменных:

- `IMAGES_DIRECTORY` - абсолютный или относительный (относительно директории, из которой запускаются скрипты) путь к папке с фотографиями. Например: `IMAGES_DIRECTORY=./images`.

- `NASA_API_KEY` - ваш API KEY с сервиса API NASA. Например: `NASA_API_KEY=hg639e20ad155405123dk5677542fecf00231da7`. Чтобы получить API KEY, сгенерируйте его на [сервисе NASA](https://api.nasa.gov/).

- `TELEGRAM_BOT_TOKEN` - API-токен telegram-бота, с помощью которого будет осуществляться публикация фотографий. Например: `TELEGRAM_BOT_TOKEN=958423683:AAEAtJ5Lde5YYfkjergber`. Если такого telegram-бота пока нет, [создайте его](https://way23.ru/регистрация-бота-в-telegram.html).

- `TELEGRAM_CHANNEL_ID` - id telegram-канала, в котором будут публиковаться фотографии. Например: `TELEGRAM_CHANNEL_ID=@flood_channel`. Если такого telegram-канала пока нет, [создайте его и назначьте вашего telegram-бота администратором канала](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/).

- `DELAY_IN_SECONDS` - задержка в секундах между публикациями фотографий для скрипта *publish_all_images_in_telegram*. Например: `DELAY_IN_SECONDS=3600`. 
Если эта переменная не указана, то по умолчанию задержка будет 4 часа.

## Запуск

Для запуска нужного вам скрипта наберите в командной строке одну из команд:
```
python -m fetch_apod_nasa_images
python -m fetch_epic_nasa_images
python -m fetch_spacex_images [{id_конкретного_запуска_ракеты}]
python -m publish_image_in_telegram [{имя_файла_с_фото}]
python -m publish_all_images_in_telegram
```
Здесь для скрипта *fetch_spacex_images* можно указать необязательный параметр командной строки `{id_конкретного_запуска_ракеты}`. Например: `5eb87d47ffd86e000604b38a`.<br>
Если этот параметр указан, то скрипт получит фотографии указанного запуска.<br>
Если этот параметр не указан, то скрипт получит фотографии последнего из запусков, для которого имеются фотографии.

Для скрипта *publish_image_in_telegram* можно указать необязательный параметр командной строки `{имя_файла_с_фото}` - имя конкретного файла, который вы хотите опубликовать. Например: `image1.jpg`. Файл должен лежать в директории, заданной в переменной окружения `IMAGES_DIRECTORY`.<br>
Если этот параметр указан, то скрипт опубликует фото из файла с указанным именем.<br>
Если этот параметр не указан, то скрипт выберет файл для публикации случайным образом.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).