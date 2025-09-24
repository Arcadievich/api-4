import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot_token = os.getenv('TG_BOT_TOKEN')

    bot = telegram.Bot(token=bot_token)
    bot.send_message(text='Hi, all!', chat_id='@B_Space_P')


if __name__ == '__main__':
    main()