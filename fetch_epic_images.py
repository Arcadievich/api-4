import requests
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path


def get_epic_images_links(token):
    """Получение ссылок на фото."""
    url = 'https://epic.gsfc.nasa.gov/api/natural/images'
    payload = {'api_key': token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def download_epic_images(token, images_info):
    """Скачивание фото из ссылок."""
    for index, dict in enumerate(images_info, start=1):
        image_name = dict['image']
        aDateTime = datetime.datetime.fromisoformat(dict['date'])
        formatted_date = aDateTime.strftime('%Y/%m/%d')

        url = f'https://epic.gsfc.nasa.gov/archive/natural/{formatted_date}/png/{image_name}.png'
        payload = {'api_key': token}
        response = requests.get(url, params=payload)
        response.raise_for_status()

        try:
            Path('images').mkdir()
        except FileExistsError:
            pass

        filename = rf'images\epic{index}.png'
        with open (filename, 'wb') as file:
            file.write(response.content)


def fetch_epic_images(token):
    """Получение ссылок и скачивание фото."""
    images_info = get_epic_images_links(token)
    download_epic_images(token, images_info)


def main():
    load_dotenv()
    nasa_token = os.getenv('NASA_API_KEY')

    fetch_epic_images(nasa_token)


if __name__=='__main__':
    main()