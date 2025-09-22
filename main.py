import requests
import os
from pathlib import Path
from random import choice
from urllib.parse import urlsplit
from os.path import splitext
from dotenv import load_dotenv


def download_image(image_url, image_name):
    try:
        Path('images').mkdir()
    except FileExistsError:
        pass

    filename = rf'images\{image_name}'
    response = requests.get(image_url)
    response.raise_for_status()

    with open (filename, 'wb') as file:
        file.write(response.content)


def download_any_image(url, image_name):
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



def get_spacex_images_links():
    response = requests.get('https://api.spacexdata.com/v5/launches')
    response.raise_for_status()
    response = response.json()

    launches = []
    for dict in response:
        launch_id = dict['id']
        launches.append(launch_id)
    
    while True:
        random_url = f'https://api.spacexdata.com/v5/launches/{choice(launches)}'
        response = requests.get(random_url)
        response.raise_for_status()
        response = response.json()
        if response['links']['flickr']['original']:
            break

    return response['links']['flickr']['original']


def get_nasa_images_links(token):
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


def get_epic_image_link(token):
    url = 'https://api.nasa.gov/EPIC/api/natural/date/2019-05-30'
    payload = {'api_key': token}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    json_response = response.json()
    print(json_response)


def fetch_spacex_random_launch():
    image_links = get_spacex_images_links()

    for index, image_link in enumerate(image_links, start=1):
        filename = f'spacex{index}.jpg'
        download_image(image_link, filename)


def fetch_nasa_images(token):
    images_links = get_nasa_images_links(token)

    for index, image_link in enumerate(images_links, start=1):
        image_name = f'nasa{index}'
        download_any_image(image_link, image_name)



def main():
    load_dotenv()
    nasa_token = os.getenv('NASA_API_KEY')
    fetch_spacex_random_launch()
    fetch_nasa_images(nasa_token)


if __name__ == '__main__':
    main()