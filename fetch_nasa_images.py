import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlsplit
from os.path import splitext
from download_tools import download_image
from download_tools import create_parser


def get_nasa_images_links(token, count):
    """Получение ссылок на фото."""
    url = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'count': count,
        'api_key': token,
        }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_data = response.json()

    images_links = []
    for record in response_data:
        if 'hdurl' in record and record['media_type'] == 'image':
            images_links.append(record['hdurl'])

    return images_links


def fetch_nasa_images(token, path, count):
    """Получить ссылки на фото и скачать их."""
    images_links = get_nasa_images_links(token, count)
    Path(path).mkdir(exist_ok=True)

    for index, image_link in enumerate(images_links, start=1):
        parsed_link = urlsplit(image_link)
        extension = (splitext(parsed_link.path))[1]
        filename = Path(path) / f'nasa{index}{extension}'
        download_image(image_link, filename)


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    count = args.count

    load_dotenv()
    nasa_token = os.environ['NASA_API_KEY']

    fetch_nasa_images(nasa_token, path, count)


if __name__=='__main__':
    main()