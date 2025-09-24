import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.getenv('TG_BOT_TOKEN')
    tg_channel_id = os.getenv('TG_CHANNEL_ID')

    bot = telegram.Bot(token=bot_token)
    bot.send_document(
        chat_id=tg_channel_id,
        document=open('images/spacex6.jpg', 'rb')
        )


if __name__ == '__main__':
    main()