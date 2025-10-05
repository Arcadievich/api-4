import requests
from pathlib import Path
from random import choice
from download_tools import download_image
from download_tools import create_parser


def make_request(url):
    """Сделать запрос."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_latest_spacex_launch_images_links():
    """Получение ссылок на фото с последнего запуска."""
    url = 'https://api.spacexdata.com/v5/launches/latest'
    latest_launch_info = make_request(url)
    return latest_launch_info['links']['flickr']['original']


def get_random_launch_spacex_images_links():
    """Получение ссылок на фото случайного запуска."""
    response = make_request('https://api.spacexdata.com/v5/launches')

    launches = [item['id'] for item in response]
    
    for launch in range(len(launches)):
        random_url = f'https://api.spacexdata.com/v5/launches/{choice(launches)}'
        response = make_request(random_url)
        if response['links']['flickr']['original']:
            break

    return response['links']['flickr']['original']


def get_spacex_images_links(launch_id):
    """Получение ссылок на фото указанного запуска."""
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    launch_info = make_request(url)
    return launch_info['links']['flickr']['original']


def fetch_spacex_launch_images(image_links, path):
    """Сохранение фото из полученных ссылок."""
    Path(path).mkdir(exist_ok=True)

    for index, image_link in enumerate(image_links, start=1):
        filename = Path(path) / f'spacex{index}.jpg'
        download_image(image_link, filename)


def download_random_launch_images(path):
    """Скачать фото случайного запуска."""
    random_images_links = get_random_launch_spacex_images_links()
    fetch_spacex_launch_images(random_images_links, path)


def main():
    parser = create_parser()
    args = parser.parse_args()
    launch_id = args.launch_id
    path = args.path
    
    if launch_id:   # Если ID указан.
        images_links = get_spacex_images_links(launch_id)
        if not images_links:
            random_launch_images_links = get_random_launch_spacex_images_links()
            fetch_spacex_launch_images(random_launch_images_links, path)
            print('Фото по указанному ID отсутствуют.')
            print('Скачаны фото случайного запуска.')
        else:
            fetch_spacex_launch_images(images_links)
            print('Фото по указанному ID найдены и скачаны.')

    elif not launch_id:    # Если ID не указан.
        latest_launch_images_links = get_latest_spacex_launch_images_links()
        if not latest_launch_images_links:
            random_launch_images_links = get_random_launch_spacex_images_links()
            fetch_spacex_launch_images(random_launch_images_links, path)
            print('Фото последнего запуска отсутствуют.')
            print('Скачаны фото случайного запуска.')
        else:
            fetch_spacex_launch_images(latest_launch_images_links, path)
            print('Фото последнего запуска найдены и скачаны.')


if __name__ == '__main__':
    main()