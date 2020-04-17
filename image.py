import requests
import argparse
import os
import logging


def create_logger():
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level='INFO')
    logger = logging.getLogger()
    return logger


def createparser():
    version = '1.0.2'
    parser = argparse.ArgumentParser(
        prog='GetMeTheseImages!',
        description='''This program was made for downloading pictures.
                        The main idea of this script is to find images on what category you want.
                        You can choose a category from the list above:
                        {backgrounds, fashion, nature, science, education, feelings, health, people,
                        religion, places, animals, industry, computer, food, sports, transportation, travel,
                        buildings, business, music}
                        Also you need to choose a number of photos.
                        Available values - from 3 to 200'''
    )
    parser.add_argument('-c', '--category',type=str, help='One of required categories', metavar='')
    parser.add_argument('-p', '--per_page',type=int, help='Determine the number of results per page.', metavar='')
    parser.add_argument('--version', action='version', help='show version', version='%(prog)s {}'.format(version))
    return parser


def download_photo(url, id, file_path):
    response = requests.get(url, stream=True)
    filename = str(id) + '.jpg'
    if not os.path.exists(os.path.join(file_path, filename)):
        with open(os.path.join(file_path, filename), 'bw') as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
    else:
        create_logger().warning('This file is already exists')


def create_folder():
    saved_pictures = os.path.join(os.getcwd(), 'pictures')
    if not os.path.isdir(saved_pictures):
        os.mkdir(saved_pictures)
    return saved_pictures


def start_parcing():
    parser = createparser()
    return parser.parse_args()


def get_response():
    parser = start_parcing()
    if 3 <= start_parcing().per_page <= 200:
        response = requests.get(
            f"https://pixabay.com/api/"
            f"?key={ULTRA_SECRET_KEY}"
            f"&category={parser.category}"
            f"&per_page={parser.per_page}")
        return response
    else:
        create_logger().warning('Use python image.py -h for help')


def main():
    answear = create_logger()
    check_folder = create_folder()
    answear.info('Starting program...')
    photos = get_response().json()['hits']
    for index,photo in enumerate(photos):
        url = photo['largeImageURL']
        unick_id = photo['id']
        answear.info(f'Downloading {index + 1} photo from {start_parcing().per_page}')
        index += 1
        test = os.getcwd()
        download_photo(url, unick_id, check_folder)
    answear.info('Done!')


if __name__ == '__main__':
    ULTRA_SECRET_KEY = os.environ.get('PIXABAY_API_KEY')
    main()



