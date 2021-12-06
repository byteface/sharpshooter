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
    parser.add_argument(
        '-q',
        '--quiet',
        help="operate in complete silence",
        action='store_true'
    )
    # parser.add_argument('-c', '--config', action='store')
    # parser.add_argument('-i', '--input', action='store_true') # create trees from terminal input
    # parser.add_argument('-r', '--remove', action='store_true') # remove the tree file after creation
    # parser.add_argument('-l', '--label', action='store_true') # only run the trees in the file that have a given label
    parser.add_argument(
        "-f",
        "--file",
        help="Create a directory structure from a .tree file",
        nargs="?",
        type=argparse.FileType("r")
    )
    parser.add_argument(
        "-t",
        "--test",
        help="test mode won't write to the filesystem",
        nargs="?",
        type=argparse.FileType("r")
    )
    parser.add_argument(
        "-c",
        "--create",
        help="Create a helloworld.tree file",
        type=str,
        nargs="?",
        default="helloworld",
    )
    parser.add_argument(
        "-j",
        "--jinja",
        help="Create a directory structure from a .tree file. But passes through Jinja first.",
        nargs="*",
        type=str
    )

    args = parser.parse_args()
    return args


def do_things(arguments):

    _is_quiet = arguments.quiet

    if arguments.version is True:
        from sharpshooter import __version__
        print(__version__)
        return __version__
    if arguments.test is not None:
        filecontent = ""
        with open(arguments.test.name, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent, test=True, quiet=_is_quiet)
        return
    if arguments.file is not None:
        # TODO - if no file passed find one called .tree and use it anyway? at least ask for confirmation
        filecontent = ""
        with open(arguments.file.name, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent, quiet=_is_quiet)
        return

    if arguments.jinja is not None:
        try:
            from jinja2 import Environment, FileSystemLoader
        except ImportError:
            raise ImportError("This option requires Jinja2 to be installed")
        filecontent = ""
        kwargs = {}
        args = arguments.jinja
        tmpfile = args.pop(0)
        # print(tmpfile, args)
        for arg in args:
            key, val = arg.split("=")
            kwargs[key] = val
        env = Environment(
            loader=FileSystemLoader(searchpath="./")
        )
        template = env.get_template(tmpfile)
        # print(kwargs)
        filecontent = template.render(**kwargs)
        tree(filecontent, quiet=_is_quiet)
        return
    # sharpshooter -j testjinja.tree replaceme=somefolder andme=another count=20

    if arguments.create is not None:
        name = "helloworld"
        if arguments.create is not None:
            name = arguments.create
        filename = f"{name}.tree"
        with open(filename, "w") as f:
            f.write(
                """# **********************************************************************
# **********************************************************************
#        _                          _                 _            
#       | |                        | |               | |           
#    ___| |__   __ _ _ __ _ __  ___| |__   ___   ___ | |_ ___ _ __ 
#   / __| '_ \ / _` | '__| '_ \/ __| '_ \ / _ \ / _ \| __/ _ \ '__|
#   \__ \ | | | (_| | |  | |_) \__ \ | | | (_) | (_) | ||  __/ |   
#   |___/_| |_|\__,_|_|  | .__/|___/_| |_|\___/ \___/ \__\___|_|   
#                        | |                                       
#                        |_|                                       
#
#   This is a sharpshooter .tree file.
#
#   For more info visit: 
#   https://github.com/byteface/sharpshooter/
#
#   sharpshooter (tree) is open sourced under a MIT License
#
# **********************************************************************
# **********************************************************************

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
