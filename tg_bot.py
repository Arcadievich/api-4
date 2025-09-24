import telegram
import os
import argparse
import time
from random import shuffle
from dotenv import load_dotenv


def sending_images(bot, chat_id):
    """Бесконечное отправление фотографий."""
    parser = argparse.ArgumentParser(
        description='Задержка публикации фотографий'
    )

    parser.add_argument(
        'delay',
        nargs='?',
        default=14400,
        help='ID запуска космического аппарата'
        )
    
    args = parser.parse_args()
    delay = int(args.delay)

    images_list = []
    for root, dirs, files in os.walk('images'):
        images_list.extend(files)

    while True:
        for image in images_list:
            bot.send_document(
                chat_id=chat_id,
                document=open(f'images/{image}', 'rb')
            )
            time.sleep(delay)

        shuffle(images_list)

        for image in images_list:
            bot.send_document(
                chat_id=chat_id,
                document=open(f'images/{image}', 'rb')
            )
            time.sleep(delay)
        


def main():
    load_dotenv()
    bot_token = os.getenv('TG_BOT_TOKEN')
    tg_channel_id = os.getenv('TG_CHANNEL_ID')

    bot = telegram.Bot(token=bot_token)
    sending_images(bot=bot, chat_id=tg_channel_id)


if __name__ == '__main__':
    main()