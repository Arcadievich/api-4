import requests
import argparse


def download_image(url, filename):
    """Скачать фото по ссылке."""
    response = requests.get(url)
    response.raise_for_status()
    
    with open (filename, 'wb') as file:
        file.write(response.content)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--launch_id',
        '-id',
        type=str,
        nargs='?',
        default='',
        help='ID запуска космического аппарата'
        )
    parser.add_argument(
        '--path',
        '-p',
        type=str,
        nargs='?',
        default='images',
        help='Папка для сохранения фотографий',
        )
    parser.add_argument(
        '--delay',
        '-d',
        type=int,
        nargs='?',
        default=14400,
        help='Задержка отправки сообщений',
        )
    parser.add_argument(
        '--count',
        '-c',
        type=int,
        nargs='?',
        default=30,
        help='Количество скачиваемых фотографий',
    )
    return parser