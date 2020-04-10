import requests
import json
import argparse
import os
import logging


def createparser():
    version = '1.0.1'
    parser = argparse.ArgumentParser(
        prog='GetMeTheseImages!',
        description='''This program was made for downloading pictures.
                        The main idea of this script is to find images on what category you want.
                        You can choose a category from the list above:
                        {backgrounds, fashion, nature, science, education, feelings, health, people, 
                        religion, places, animals, industry, computer, food, sports, transportation, travel, 
                        buildings, business, music}
                        Also you need to choose a number of photos, by default its value =20, so you will get 20 pictures. 
                        Available values - from 3 to 200'''
    )
    parser.add_argument('-c', '--category', help='One of required categories', metavar='')
    parser.add_argument('-p', '--per_page', help='Determine the number of results per page.', metavar='')
    parser.add_argument('--version', action='version', help='show version', version='%(prog)s {}'.format(version))

    return parser


def write_json(data):
    with open('response_json', 'w') as file:
        json.dump(data, file, indent=2)


def download_photo(url):
    response = requests.get(url, stream=True)

    filename = url.split('/')[-1]

    with open(filename, 'bw') as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level='INFO')
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

    response = requests.get(
        F"https://pixabay.com/api/?key={ULTRA_SECRET_KEY}&category={namespace.category}&per_page={namespace.per_page}")

    write_json(response.json())

    photos = json.load(open('response_json'))['hits']

    count = 1

    for photo in photos:
        url = photo['largeImageURL']
        logger.info(f'Downloading {count} photo from {namespace.per_page}')
        count += 1
        download_photo(url)

    logger.info('Done!')


if __name__ == '__main__':
    ULTRA_SECRET_KEY = os.environ.get('PIXABAY_API_KEY')
    main()
