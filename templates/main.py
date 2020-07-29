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

class Main(Program):

    def run(self):
        super().run()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-l', '--log', type=bool, default=True, help='Whether or not the program should log anything to the console')

    args = vars(parser.parse_args())

    Main(args).run()