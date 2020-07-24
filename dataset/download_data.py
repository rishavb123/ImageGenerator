import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(
        os.path.join(os.getcwd(), os.path.expanduser(__file__))
    )
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import argparse
from bs4 import BeautifulSoup
import urllib.request
import re

from util.program import Program

class DownloadImages(Program):

    def run(self):
        super().run()
        
        search_query = args['query']
        num_of_images = args['num_of_images']

        page = urllib.request.urlopen('https://www.flickr.com/search/?text={}&view_all=1'.format(search_query))
        soup = BeautifulSoup(page, 'html.parser')
        img_divs = soup.findAll("div", {"class": "photo-list-photo-view"})
        img_styles = [div['style'] for div in img_divs[:num_of_images]]
        urls = [re.findall('url\((.*?)\)', style) for style in img_styles]
        for i in range(len(urls)):
            urls[i] = 'https:' + urls[i][0]
        print(urls)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--query', type=str, default='sunset')
    parser.add_argument('--num-of-images', type=int, default=10)

    args = vars(parser.parse_args())

    DownloadImages(args).run()