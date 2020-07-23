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

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('Search Query', type=str)

    args = vars(parser.parse_args())
