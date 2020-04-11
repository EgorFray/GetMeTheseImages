import hashlib
import os
import unittest

import responses

from image import download_photo

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class ImagesTestCase(unittest.TestCase):

    @responses.activate
    def test_file_download(self):
        img_name = '53e0d54a4f51af14f6da8c7dda79367b1d39dde454596c4870277dd2944cc151b1_1280.jpg'
        url = f'https://pixabay.com/get/{img_name}'
        with open(f'images/{img_name}', 'rb') as img:
            responses.add(responses.GET, url,
                          body=img.read(), status=200,
                          content_type='image/jpg',
                          adding_headers={'Transfer-Encoding': 'chunked'})
            download_photo(url, '.')
        md5_hash_of_original_img = md5(f'images/{img_name}')
        md5_hash_of_downloaded_img = md5(img_name)

        self.assertEqual(md5_hash_of_downloaded_img, md5_hash_of_original_img)

    def test_file_name(self):
        img_name = '53e0d54a4f51af14f6da8c7dda79367b1d39dde454596c4870277dd2944cc151b1_1280.jpg'
        with open(img_name, 'rb') as downloaded_img:
            self.assertEqual(downloaded_img.name, img_name)


if __name__ == '__main__':
    unittest.main()
