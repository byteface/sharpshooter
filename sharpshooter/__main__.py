"""
    ¥ tree (sharpshooter) CLI entry point.
    ====================================

"""

import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(add_help=False,
                                     prog="sharpshooter",
                                     usage="%(prog)s [options]",
                                     description="Generate filesystems with Python 3")
    
    # parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-v', '--version', action='store_true')
    # parser.add_argument('-d', '--debug', action='store_true')
    # parser.add_argument('-q', '--quiet', action='store_true')
    # parser.add_argument('-c', '--config', action='store')    
    # parser.add_argument('-i', '--input', action='store_true') # create trees from terminal input


    args = parser.parse_args()
    return args


def do_things(arguments):
    if arguments.version is True:
        from sharpshooter import __version__
        print(__version__)
        return __version__


if __name__ == "__main__":
    args = parse_args()
    do_things(args)
