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

from util.program import Program
from util.args_util import str2bool

class Test(Program):

    def run(self):
        super().run()
        data = np.load('../data/loaded/fire/50000_1595605654.npy')
        print(data.shape[1:3])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-l', '--log', type=str2bool, default=True, help='Whether or not the program should log anything to the console')

    args = vars(parser.parse_args())

    Test(args).run()