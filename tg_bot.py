import telegram
import os
import argparse
import time
from random import shuffle
from dotenv import load_dotenv


def setup_delay():
    """Установка задержки через аргумент."""
    parser = argparse.ArgumentParser(
        description='Задержка публикации фотографий'
    )

    parser.add_argument(
        'delay',
        type=int,
        nargs='?',
        default=14400,
        help='ID запуска космического аппарата'
        )
    
    args = parser.parse_args()
    delay = args.delay
    return delay


def creating_list_of_files(directory):
    """Создание списка названий файлов в директории."""
    items = []
    for root, dirs, files in os.walk(directory):
        items.extend(files)
    return items


def sending_multiple_images(images, bot, chat_id, delay):
    """Отправка фото из списка с задержкой."""
    for image in images:
        bot.send_document(
            chat_id=chat_id,
            document=open(f'images/{image}', 'rb'),
        )
        time.sleep(delay)


def endless_sending_images(bot, chat_id):
    """Бесконечное отправление фотографий."""
    delay = setup_delay()

    images = creating_list_of_files('images')

    while True:
        sending_multiple_images(images, bot, chat_id, delay)

        shuffle(images)

        sending_multiple_images(images, bot, chat_id, delay)
        


def main():
    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    tg_channel_id = os.environ['TG_CHANNEL_ID']

    bot = telegram.Bot(token=bot_token)
    endless_sending_images(bot=bot, chat_id=tg_channel_id)


if __name__ == '__main__':
    main()