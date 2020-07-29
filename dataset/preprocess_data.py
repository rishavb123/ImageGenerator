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
import cv2

from util.program import Program
from util.progress_bar import ProgressBar
from util.timer import Timer

class ProcessImages(Program):

    def run(self):
        super().run()
        query = args['query']

        options = os.listdir('../data/raw/' + query)
        ind = -1
        if len(options) == 1:
            ind = 0
        else:
            for i, option in enumerate(options):
                print('({}) {}'.format(i, option))
            ind = input('Enter your option index: ')
            while not ind.isdigit() or int(ind) < 0 or int(ind) >= len(options):
                ind = input('Please enter a valid option: ')
            ind = int(ind)
        img_dir = '../data/raw/' + query + '/' + options[ind]
        
        img_names = os.listdir(img_dir)
        progress_bar = ProgressBar(len(img_names))

        if not os.path.exists('../data/preprocessed/' + query):
            os.mkdir('../data/preprocessed/' + query)
        if not os.path.exists('../data/preprocessed/' + query + '/' + options[ind]):
            os.mkdir('../data/preprocessed/' + query + '/' + options[ind])

        while True:
            img = cv2.imread(img_dir + '/' + img_names[progress_bar.i])
            dim = min(img.shape[:2])
            if img.shape[0] == dim:
                lrg_dim = img.shape[1]
                img = img[:, int((lrg_dim - dim) / 2): int((lrg_dim + dim) / 2)]
            else:
                lrg_dim = img.shape[0]
                img = img[int((lrg_dim - dim) / 2): int((lrg_dim + dim) / 2), :]
            img = cv2.resize(img, (200, 200))
            cv2.imwrite('../data/preprocessed/' + query + '/' + options[ind] + '/' + img_names[progress_bar.i], img)
            if progress_bar.increment(): break

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--query', type=str, default='sunset')

    args = vars(parser.parse_args())

    ProcessImages(args).run()