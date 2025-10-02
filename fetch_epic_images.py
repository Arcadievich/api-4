import requests
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
from download_tools import download_image
from download_tools import create_parser


def get_epic_images_links(token):
    """Получение ссылок на фото."""
    url = 'https://epic.gsfc.nasa.gov/api/natural/images'
    payload = {'api_key': token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    return response.json()


def fetch_epic_images(token, path):
    images_info = get_epic_images_links(token)
    Path(path).mkdir(exist_ok=True)

    for index, image_info in enumerate(images_info, start=1):
        image_name = image_info['image']
        date_time = datetime.datetime.fromisoformat(image_info['date'])
        formatted_date = date_time.strftime('%Y/%m/%d')

        url = f'https://epic.gsfc.nasa.gov/archive/natural/{formatted_date}/png/{image_name}.png'
        filename = Path(path) / f'epic{index}.png'
        download_image(url, filename)


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path

    load_dotenv()
    nasa_token = os.environ['NASA_API_KEY']

    fetch_epic_images(nasa_token, path)


if __name__=='__main__':
    main()