import os
from dotenv import load_dotenv
from fetch_spacex_images import download_random_launch_images
from fetch_epic_images import fetch_epic_images
from fetch_nasa_images import fetch_nasa_images
from download_tools import create_parser


def main():
    load_dotenv()
    nasa_token = os.environ['NASA_API_KEY']

    parser = create_parser()
    args = parser.parse_args()
    path = args.path

    download_random_launch_images(path)
    fetch_nasa_images(nasa_token, path)
    fetch_epic_images(nasa_token, path)


if __name__ == '__main__':
    main()