"""
    ¥ tree (sharpshooter) CLI entry point.
    ====================================

"""

import argparse
import os
import sys

from sharpshooter import tree


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="sharpshooter",
        usage="%(prog)s [options]",
        description="Generate filesystems with Python 3",
    )

    # parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument("-v", "--version", action="store_true")
    # parser.add_argument('-d', '--debug', action='store_true')
    # parser.add_argument('-q', '--quiet', action='store_true')
    # parser.add_argument('-c', '--config', action='store')
    # parser.add_argument('-i', '--input', action='store_true') # create trees from terminal input
    parser.add_argument("-f", "--file", nargs="?", type=argparse.FileType("r"))
    parser.add_argument("-t", "--test", nargs="?", type=argparse.FileType("r"))
    parser.add_argument(
        "-c",
        "--create",
        help="Create a helloworld.tree file",
        type=str,
        nargs="?",
        default="helloworld",
    )

    args = parser.parse_args()
    return args


def do_things(arguments):
    if arguments.version is True:
        from sharpshooter import __version__

        print(__version__)
        return __version__
    if arguments.test is not None:
        filecontent = ""
        with open(arguments.test.name, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent, test=True)
        return
    if arguments.file is not None:
        filecontent = ""
        with open(arguments.file.name, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent)
        return
    if arguments.create is not None:
        name = "helloworld"
        if arguments.create is not None:
            name = arguments.create
        filename = f"{name}.tree"
        with open(filename, "w") as f:
            f.write(
                """
+hello
    world.txt
"""
            )

        print("done")
        return


def run():
    """[Entry point required by setup.py console_scripts.]"""
    args = parse_args()
    do_things(args)


if __name__ == "__main__":
    run()
