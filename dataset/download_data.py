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
import urllib.request
import re
import time
import cv2
import flickrapi

from util.program import Program
from util.image_utils import download_image_from_url
from util.progress_bar import ProgressBar

from dataset.flickr_auth import *

orig_time = int(time.time())
flickr = flickrapi.FlickrAPI(key, secret, cache=True)

class DownloadImages(Program):

    def run(self):
        super().run()
        
        search_query = self.args['query']
        num_of_images = self.args['num_of_images']

        folder = '{}_{}'.format(num_of_images, orig_time)

        if not os.path.exists('../data/raw/{}'.format(search_query)):
            os.mkdir('../data/raw/{}'.format(search_query))
        if not os.path.exists('../data/raw/{}/{}'.format(search_query, folder)):
            os.mkdir('../data/raw/{}/{}'.format(search_query, folder))

        # page = urllib.request.urlopen('https://www.flickr.com/search/?text={}&view_all=1&media=photos'.format(search_query.replace(' ', '%20')))
        # soup = BeautifulSoup(page, 'html.parser')
        # img_divs = soup.findAll("div", {"class": "photo-list-photo-view"})
        # img_styles = [div['style'] for div in img_divs[:num_of_images]]
        # progress_bar = ProgressBar(len(img_styles))
        # urls = [re.findall('url\((.*?)\)', style) for style in img_styles]
        # for i in range(len(urls)):
        #     url = 'https:' + urls[i][0]
        #     img = download_image_from_url(url)
        #     cv2.imwrite('../data/raw/{}/{}/img_{}_{}.png'.format(search_query, folder, i, int(time.time())), img)
        #     progress_bar.show()
        #     progress_bar.increment()

        photos = flickr.walk(text=search_query, tag_mode='all', tags=search_query, extras='url_c', per_page=num_of_images, sort='relevance')
        progress_bar = ProgressBar(num_of_images)

        err_idx = []

        for i, photo in enumerate(photos):
            try:
                url = photo.get('url_c')
                img = download_image_from_url(url)
                cv2.imwrite('../data/raw/{}/{}/img_{}_{}.png'.format(search_query, folder, i, int(time.time())), img)
            except:
                err_idx.append(i)
            if progress_bar.increment(): break
        
        # print('Error Indexes:', err_idx)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--query', type=str, default='sunset')
    parser.add_argument('--num-of-images', type=int, default=50000)

    args = vars(parser.parse_args())

    for query in args['query'].split(';'):
        a = args.copy()
        a['query'] = query
        DownloadImages(a).start()
