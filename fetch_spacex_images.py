import requests
import argparse
from pathlib import Path
from random import choice


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

    launches = []
    for item in response:
        launch_id = item['id']
        launches.append(launch_id)
    
    for launch in range(200):
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
        

def download_image(image_url, image_name):
    """Скачать фото из ссылок."""
    Path('images').mkdir(exist_ok=True)

    filename = rf'images\{image_name}'
    response = requests.get(image_url)
    response.raise_for_status()

    with open (filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_launch_images(image_links):
    """Сохранение фото из полученных ссылок."""
    for index, image_link in enumerate(image_links, start=1):
        filename = f'spacex{index}.jpg'
        download_image(image_link, filename)


def download_random_launch_images():
    """Скачать фото случайного запуска."""
    random_images_links = get_random_launch_spacex_images_links()
    fetch_spacex_launch_images(random_images_links)


def main():
    parser = argparse.ArgumentParser(
        description='Получение изображений с запуска ракеты SpaceX по ID запуска'
    )

    parser.add_argument(
        'launch_id',
        nargs='?',
        default='',
        help='ID запуска космического аппарата'
        )
    
    args = parser.parse_args()
    launch_id = args.launch_id
    
    if launch_id:   # Если ID указан.
        images_links = get_spacex_images_links(launch_id)
        if not images_links:
            random_launch_images_links = get_random_launch_spacex_images_links()
            fetch_spacex_launch_images(random_launch_images_links)
            print('Фото по указанному ID отсутствуют.')
            print('Скачаны фото случайного запуска.')
        else:
            fetch_spacex_launch_images(images_links)
            print('Фото по указанному ID найдены и скачаны.')

    elif not launch_id:    # Если ID не указан.
        latest_launch_images_links = get_latest_spacex_launch_images_links()
        if not latest_launch_images_links:
            random_launch_images_links = get_random_launch_spacex_images_links()
            fetch_spacex_launch_images(random_launch_images_links)
            print('Фото последнего запуска отсутствуют.')
            print('Скачаны фото случайного запуска.')
        else:
            fetch_spacex_launch_images(latest_launch_images_links)
            print('Фото последнего запуска найдены и скачаны.')


if __name__ == '__main__':
    main()