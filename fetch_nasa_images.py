import requests
from pathlib import Path
from urllib.parse import urlsplit
from os.path import splitext


def download_nasa_image(url, image_name):
    """Скачивание фото из полученных ссылок."""
    try:
        Path('images').mkdir()
    except FileExistsError:
        pass
    parsed_url = urlsplit(url)
    extension = (splitext(parsed_url.path))[1]

    filename = rf'images\{image_name}{extension}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print('Возникла ошибка при скачивании')

    with open (filename, 'wb') as file:
        file.write(response.content)


def get_nasa_images_links(token):
    """Получение ссылок на фото."""
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'count': 30,
        'api_key': token,
        }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_dict = response.json()

    images_links = []
    for object in response_dict:
        if 'hdurl' in object:
            images_links.append(object['hdurl'])

    return images_links


def fetch_nasa_images(token):
    """Получить ссылки на фото и скачать их."""
    images_links = get_nasa_images_links(token)

    for index, image_link in enumerate(images_links, start=1):
        image_name = f'nasa{index}'
        download_nasa_image(image_link, image_name)