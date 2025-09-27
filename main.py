import os
from dotenv import load_dotenv
from fetch_spacex_images import download_random_launch_images
from fetch_epic_images import fetch_epic_images
from fetch_nasa_images import fetch_nasa_images


def main():
    load_dotenv()
    nasa_token = os.environ['NASA_API_KEY']
    download_random_launch_images()
    fetch_nasa_images(nasa_token)
    fetch_epic_images(nasa_token)


if __name__ == '__main__':
    main()