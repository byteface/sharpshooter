"""
    ¥ tree (sharpshooter) CLI entry point.
    ====================================

"""

import argparse
import os
import sys

from sharpshooter import tree, VERSION

HEADER: str = '''# **********************************************************************
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
#   This is a sharpshooter .tree file. (v'''+VERSION+''')
#
#   For more info visit:
#   https://github.com/byteface/sharpshooter/
#
#   sharpshooter (tree) is open sourced under a MIT License
#
# **********************************************************************
# **********************************************************************
'''


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="sharpshooter",
        description="Generate filesystems with Python 3",
    )
    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        '-q',
        '--quiet',
        help="operate in complete silence.",
        action='store_true'
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Create a directory structure from a .tree file.",
        nargs="?",
        type=str
    )
    parser.add_argument(
        "-t",
        "--test",
        help="test mode won't write to the filesystem.",
        nargs="?",
        type=str
    )
    parser.add_argument(
        "-c",
        "--create",
        help="Create a helloworld.tree file.",
        type=str,
        nargs="?",
        const="helloworld"
    )
    parser.add_argument(
        "-j",
        "--jinja",
        help="Create a directory structure from a .tree file. But passes through Jinja first.",
        nargs="*",
        type=str
    )
    parser.add_argument(
        "-m",
        "--mock",
        help="Creates a tree string which mocks the current directory structure.",
        type=str,
        nargs="?",
        const="sharpshooter"
    )
    parser.add_argument(
        "-p",
        "--pretty",
        help="Prints a commonly seen pretty stylistic tree to the terminal.",
        # action='store_true',
        type=str,
        nargs="?",
        const="sharpshooter"
    )
    parser.add_argument(
        "-l",
        "--label",
        help="Only creates trees with a given label.",
        type=str,
        nargs="?",
        default=None
    )
    parser.add_argument(
        '-d',
        '--dir',
        help="Sets the cwd to something else. Put as first argument.",
        type=str,
        nargs="?",
        default=None
    )
    # parser.add_argument('-c', '--config', action='store')
    # parser.add_argument('-i', '--input', action='store_true') # create trees from terminal input
    # parser.add_argument('-r', '--remove', action='store_true') # remove the tree file after creation
    args = parser.parse_args()
    # print(parser.print_usage())
    return args, parser


def do_things(arguments, parser):
    _is_quiet: bool = arguments.quiet
    if arguments.dir is not None:
        # change the cwd to something else
        try:
            os.chdir(arguments.dir)
        except FileNotFoundError:
            print("Directory not found.")
            sys.exit(1)
    if arguments.help is True:
        print(parser.print_help())
        sys.exit()
    if arguments.version is True:
        from sharpshooter import __version__
        print(__version__)
        return __version__
    if arguments.test is not None:
        filecontent = ""
        with open(os.getcwd() + os.sep + arguments.test, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent, test=True, quiet=_is_quiet, label=arguments.label)
        return
    if arguments.file is not None:
        filecontent = ""
        with open(os.getcwd() + os.sep + arguments.file, "r") as f:
            filecontent = f.read()
            f.close()
        tree(filecontent, quiet=_is_quiet, label=arguments.label)
        return
    if arguments.jinja is not None:
        # i.e. sharpshooter -j testjinja.tree replaceme=somefolder andme=another count=20
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
        tree(filecontent, quiet=_is_quiet, label=arguments.label)
        return
    if arguments.create is not None:
        name = "helloworld"
        if arguments.create is not None:
            name = arguments.create
        filename = f"{name}.tree"
        with open(filename, "w") as f:
            f.write(
                f"""{HEADER}

/hello
    world.txt

"""
            )

        print("done")
        return
    if arguments.mock is not None:
        # name = "sharpshooter"
        if arguments.mock == "sharpshooter":
            d = 9999
        else:
            d = 0
            try:
                d = int(arguments.mock)
            except ValueError:
                print('Parameter requires integer for depth. None set')
                return
        # print('>>>',d)
        if arguments.mock is not None:
            name = arguments.mock
        filename = "sharpshooter.tree"
        content = tree.mock(d)
        with open(filename, "w") as f:
            f.write(
                f"""{HEADER}

{content}
"""
            )

        print("done!")
        return

    if arguments.pretty is not None:

        if arguments.pretty == "sharpshooter":
            d = 9999
        else:
            d = 0
            try:
                d = int(arguments.pretty)
            except ValueError:
                print('Parameter requires integer for depth. None set')
                return

        content = tree.mock(d)

        # nest everything into the cwd
        cwd = os.getcwd().split(os.sep)[-1]
        newcontent = "/" + cwd + "\n"
        for line in content.split("\n"):
            newcontent += "    " + line + "\n"
        content = newcontent

        # print(content)
        output = tree.pretty(content)
        print(output)
        # return output
        return


def run():
    """[Entry point required by setup.py console_scripts.]"""
    args, parser = parse_args()
    do_things(args, parser)


if __name__ == "__main__":
    run()
