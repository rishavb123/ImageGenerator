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
import numpy as np
import cv2

from util.program import Program
from util.progress_bar import ProgressBar
from util.timer import Timer

class Main(Program):

    def run(self):
        super().run()
        query = args['query']

        options = os.listdir('../data/preprocessed/' + query)
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
        img_dir = '../data/preprocessed/' + query + '/' + options[ind]
        
        img_names = os.listdir(img_dir)
        progress_bar = ProgressBar(len(img_names), log=self.log)

        if not os.path.exists('../data/loaded/' + query):
            os.mkdir('../data/loaded/{}'.format(query))

        images = []

        while True:
            img = cv2.imread(img_dir + '/' + img_names[progress_bar.i])
            images.append(img)
            if progress_bar.increment(): break

        timer = Timer(log=self.log)

        images = timer.time(lambda:np.array(images), 'Converting to numpy array')

        timer.time(lambda:np.save('../data/loaded/{}/{}'.format(query, options[ind] + '.npy'), images), 'Saving numpy array to file')


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--query', type=str, default='sunset')

    args = vars(parser.parse_args())

    Main(args).run()