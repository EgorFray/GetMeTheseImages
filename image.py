import requests
import json
import argparse
import os
import logging


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


def write_json(data):
    with open('response_json', 'w') as file:
        json.dump(data, file, indent=2)


def download_photo(url, file_path):
    response = requests.get(url, stream=True)

    filename = url.split('/')[-1]

    with open(os.path.join(file_path, filename), 'bw') as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%H:%M:%S', level='INFO')
    logger = logging.getLogger()

    logger.info('Starting program...')

    saved_pictures = os.getcwd() + '/pictures'

    if not os.path.isdir(saved_pictures):
        os.mkdir(saved_pictures)
    else:
        logger.warning('This directory is already exists. Complement...')

    os.chdir(saved_pictures)

    parser = createparser()

    namespace = parser.parse_args()

    print(namespace)

    if 3 <= namespace.per_page <= 200:
        response = requests.get(
            f"https://pixabay.com/api/"
            f"?key={ULTRA_SECRET_KEY}"
            f"&category={namespace.category}"
            f"&per_page={namespace.per_page}")

        write_json(response.json())

        photos = json.load(open('response_json'))['hits']

        count = 1

        for photo in photos:
            url = photo['largeImageURL']
            logger.info(f'Downloading {count} photo from {namespace.per_page}')
            count += 1
            download_photo(url, saved_pictures)

    else:
        parser.print_help()

    logger.info('Done!')


if __name__ == '__main__':
    ULTRA_SECRET_KEY = os.environ.get('PIXABAY_API_KEY')
    main()
