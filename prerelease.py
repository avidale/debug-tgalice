import logging
import os
import urllib.request

logging.basicConfig(level=logging.DEBUG)

navec_url = 'https://github.com/natasha/navec/releases/download/v0.0.0/navec_hudlit_v1_12B_500K_300d_100q.tar'
navec_file = 'navec_hudlit_v1_12B_500K_300d_100q.tar'


def download_if_not_exists(url, file):
    if os.path.exists(file):
        logging.info('File {} already exists'.format(file))
        return
    logging.info('Downloading from {} to {}'.format(url, file))
    urllib.request.urlretrieve(url, file)


if __name__ == '__main__':
    download_if_not_exists(navec_url, navec_file)
    print(os.listdir('.'))
