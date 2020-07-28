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

from util.program import Program

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

        print(img_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--query', type=str, default='sunset')

    args = vars(parser.parse_args())

    ProcessImages(args).run()