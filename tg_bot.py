import telegram
import os
import time
from pathlib import Path
from random import shuffle
from dotenv import load_dotenv
from download_tools import create_parser


def creating_list_of_files(directory):
    """Создание списка названий файлов в директории."""
    items = []
    for root, dirs, files in os.walk(directory):
        items.extend(files)
    return items


def sending_multiple_images(images, bot, chat_id, delay, path):
    """Отправка фото из списка с задержкой."""
    for image in images:
        with open (Path(path) / image, 'rb') as document:
            bot.send_document(
                chat_id=chat_id,
                document=document,
            )
        time.sleep(delay)


def endless_sending_images(bot, chat_id, delay, path):
    """Бесконечное отправление фотографий."""

    images = creating_list_of_files(path)

    while True:
        try:
            sending_multiple_images(images, bot, chat_id, delay, path)
            shuffle(images)
        except telegram.error.NetworkError:
            time.sleep(60)
        


def main():
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    delay = args.delay

    load_dotenv()
    bot_token = os.environ['TG_BOT_TOKEN']
    tg_channel_id = os.environ['TG_CHANNEL_ID']

    bot = telegram.Bot(token=bot_token)
    endless_sending_images(bot, tg_channel_id, delay, path)


if __name__ == '__main__':
    main()