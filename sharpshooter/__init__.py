"""
    tree (sharpshooter)
    ====================================

    # instructional language for creating files and folders i.e
    +:dir
        +plugins
            +mail
                file3
                +things
                    +again
                        file8
                        file9.txt
                    file7
        file6.txt
    file5.txt

    # another optional way is it use f_ and d_ builder functions
    # TODO - this aint dont yet
    d_('somedir', 
        f_('file1', chmod=755),
        d_('things', 'file2.txt', 'file3.txt')
    )

"""

__version__ = "0.0.5"
__license__ = "MIT"
__author__ = "@byteface"

VERSION = __version__

import os
import shutil
import ply.lex as lex


# class FileStream():

#     def __init__(self, input: str, output: str):
#         # detect whether it is a file or a url
#         if input.startswith("http"):
#             self.input = input
#             self.is_url = True
#         else:
#             self.input = input
#             self.is_url = False

#         # check if input is a file if not it is just a string
#         self.data = None
#         self.output = output
#         self.read()
#         self.write()
    
#     def read(self):
#         """
#         reads data from the file
#         """
#         if self.is_url:
#             import urllib.request
#             self.data = urllib.request.urlopen(self.input).read()
#         else:
#             with open(self.input, 'r') as f:
#                 self.data = f.read()
#         return self.data
    
#     def write(self, path=None):
#         """[write the data to the path]

#         Args:
#             path ([str], optional): [optional overwites the constructors output]
#         """
#         if path is None:
#             path = self.output
#         with open(path, 'w') as f:
#             f.write(path)

#     def __str__(self):
#         return self.data


def sslog(msg: str, *args, **kwargs):
    ''' logging for sharpshooter '''

    if tree.QUIET_MODE:
        return

    # if tree.VERBOSE_MODE:
    #     import sys
    #     old_log = sys.stdout
    #     log_file = open("tree.log","w") # will need to fix tree.root
    #     sys.stdout = log_file
    #     print(msg)
    #     sys.stdout = old_log

    print(msg, args, kwargs)


def octal_to_text(octal):
    """
    convers an octal string to a text string
    i.e.
    777 -> rwxrwxrwx
    """
    text = ""
    for i in range(len(octal)):
        if octal[i] == "7":
            text += "rwx"
        elif octal[i] == "6":
            text += "rw-"
        elif octal[i] == "5":
            text += "r-x"
        elif octal[i] == "4":
            text += "r--"
        elif octal[i] == "3":
            text += "-wx"
        elif octal[i] == "2":
            text += "-w-"
        elif octal[i] == "1":
            text += "--x"
        elif octal[i] == "0":
            text += "---"
    return text


def get_file_info(path, filename):
    """
    # get the same data as if doing ls -al
    # -rw-r--r--@ 1 byteface  staff  2100 21 Sep 07:58 README.md
    """

    fileinfo = {}
    fileinfo["name"] = filename
    fileinfo["path"] = os.path.join(path, filename)

    fileinfo["is_dir"] = False
    # detect if its a file or a directory
    if os.path.isfile(fileinfo["path"]):
        fileinfo["is_dir"] = False
    elif os.path.isdir(fileinfo["path"]):
        fileinfo["is_dir"] = True
    else:
        # raise Exception('File not found')
        sslog("File not found:", filename)
        return {}

    stat = os.stat(fileinfo["path"])

    # read the file permissions
    perms = stat.st_mode
    perms = oct(perms)
    perms = perms[-3:]
    fileinfo["perms"] = octal_to_text(perms)

    # read the file owner
    owner = stat.st_uid

    try:
        import pwd

        # get the name of the owner
        owner = pwd.getpwuid(owner)
        owner = owner.pw_name
    except ModuleNotFoundError:
        owner = stat.st_uid
        sslog("WINDOWS:::::", owner)

        # from pathlib import Path
        # path = Path(fileinfo['path'])
        # owner = path.owner()
        # group = path.group()
        # print(f"{path.name} is owned by {owner}:{group}")

    except:
        owner = stat.st_uid

    fileinfo["owner"] = owner

    # read the file group
    group = stat.st_gid

    try:
        import grp

        group = grp.getgrgid(group)
        group = group.gr_name
    except ModuleNotFoundError:
        # on windows try something else?
        # import win32api
        # group = win32api.GetUserName()
        # on windows try something else only using builtin functions
        # import getpass
        # group = getpass.getuser()
        group = stat.st_gid
        sslog("WINDOWS:::::", group)
    except:
        group = stat.st_gid

    fileinfo["group"] = group

    # read the file size
    size = stat.st_size
    fileinfo["size"] = size

    # read the file date
    date = stat.st_mtime
    # convert the date to a string in the format: 21 Sep 07:58
    import time

    date = time.ctime(date)
    fileinfo["date"] = date

    # read the file name
    name = os.path.basename(fileinfo["path"])
    fileinfo["name"] = name

    tree.FILE_INFO = fileinfo

    return fileinfo


class Lex(object):
    def __init__(self):

        # flags
        self.root = os.getcwd()  # may not need
        self.is_root = True
        self.depth = 0
        self.cwd = None
        self.is_dir = True
        self.was_dir = True  # hacky to always start true?
        self.skip = False
        self.is_read_only = False
        self.is_comment = False
        self.is_recursive = False
        self.is_test = False
        self.tab_count = 0
        self.last_tab_count = 0
        self.is_user_home = False # tilde handler

        self.start_tabs = 0  # if a whole block is indented, this is the number of tabs where to start from
        self.first = True  # set to false after the first file or folder is created

        self.delete = False

        self.is_extra = False  # need maybe a better variable name.
        # basically, if we are past the filename or dirname, we are in the extra stuff

        self.is_dead = False  # if a dir fails to create, we can mark it as dead
        self.dead_depth = 0  # the depth of the dead dir

        self.lexer = lex.lex(module=self)


    tokens = (
        "FILE",
        "PLUS",
        "MINUS",
        "TIMES",
        "EQUALS",
        "COLON",
        "TAB",
        "SPACE",
        # 'NEWLINE',
        "LPAREN",
        "RPAREN",
        "COMMENT",
        "TILDE",
    )

    # Ignored characters
    # t_ignore = " \t"
    t_ignore_COMMENT = r"\#.*"
    # ignore spaces before comments
    # t_ignore_SPACESCOMMENTFIX = r'[ ]+' + r'\#.*' # note - not working ?

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")
        self.was_dir = self.is_dir
        self.is_dir = False
        self.is_read_only = False
        self.is_comment = False
        self.is_recursive = False  # TODO - will need to be a 2nd pass as creation of all files is not complete
        self.skip = False
        self.is_root = True
        self.delete = False
        self.is_extra = False
        # self.is_dead = False
        self.chmod_mode = None
        self.chmod_owner = None
        self.chmod_group = None
        self.chmod_perms = None
        self.write_mode = None
        
    def t_TILDE(self, t):
        r"\~"
        self.is_user_home = True
        # self.depth += 1
        # self.is_root = False

    def t_PLUS(self, t):
        r"\+"
        self.is_dir = True

    def t_MINUS(self, t):
        r"\-"
        self.delete = True  # todo: - test it doesn't remove hyphenated words

    t_TIMES = r"\*"

    def t_WRITE(self, t):
        r"\<"
        sslog("writing:::")

    # t_DIVIDE  = r'/'
    # t_COLON  = r':'
    def t_COLON(self, t):
        r"\:"
        # print('t_COLON', t)
        # global is_read_only
        self.is_read_only = True

    def t_TAB(self, t):
        r"[\t]+"
        sslog("Tab(s)")
        sslog("t_TAB", t)
        self.move_back(len(t.value))

    def t_SPACE(self, t):
        r"[ ]+"
        # print('Space(s)')
        # TODO - error if not divisible by 4
        # length = len(t.value)
        # if length % 4 != 0:
        #     print(f"Illegal spacing>>>>>>>>>>>>>>>>>>>>>>>>>>>: {t.value[0]!r}")
        #     print(length)
        # t.lexer.skip(length-1)
        # return

        # print('t_SPACE', t)
        # print(len(t.value))
        if self.is_extra:
            return  # TODO - for now ignoring anything after the filename

        spaces = int(len(t.value) / 4)

        if self.first:
            self.start_tabs = spaces
            return

        spaces -= self.start_tabs
        # if spaces < self.start_tabs:
        # return

        self.move_back(spaces)

    def move_back(self, spaces: int):
        """[counts the spaces and moves back up the directory tree]

        Args:
            spaces ([int]): [how many steps to move back up the directory tree]
        """

        # if spaces == 0:
        #     return

        # if spaces < 0:
        #     print("ERROR: move back negative")
        #     return

        # if self.is_root:
        #     print("ERROR: move back from root")
        #     return

        self.is_root = False  # hacky. it wont get called if no space
        self.last_tab_count = self.tab_count
        self.tab_count = self.depth - spaces
        if self.tab_count < 0:
            self.tab_count = self.last_tab_count
            self.skip = True
            sslog("Error. You can only put things in folders")
            return

        if self.is_dead:
            self.depth = spaces
            return

        while self.tab_count > 0:
            
            if tree.TEST_MODE:
                # note - in test mode we can't change dirs so have to build cwd manually
                path_parent = os.path.dirname(self.cwd)
                self.cwd = path_parent
            else:
                path_parent = os.path.dirname(os.getcwd())
                os.chdir(path_parent)
                self.cwd = os.getcwd()

            self.depth -= 1
            self.tab_count -= 1

    # t_NEWLINE  = r'\n'
    t_EQUALS = r"="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    def t_FILE(self, t):
        # r"[a-zA-Z_][a-zA-Z_0-9.\-]*" # v1- doesn't allows spaces in filenames 
        r"[a-zA-Z_][a-zA-Z_0-9.\-]*([\w. ]*)"
        
        if self.cwd is None:
            self.cwd = os.getcwd()

        if self.is_root:
            os.chdir(self.root)
            self.cwd = os.getcwd()

        if self.first:
            self.first = False

        self.is_extra = True  # lets the spacer know we are past the filename or dirname

        if self.is_dead:
            # print( self.cwd )
            if self.depth <= self.dead_depth:
                sslog(self.depth, self.dead_depth)
                sslog("Same depth as previous dead dir. no longer dead:", t.value)
                self.is_dead = False
                # self.depth = self.dead_depth
                self.dead_depth = 0

                # print( self.cwd )
            else:
                sslog("Skipping dead dir", t.value)
                return

        if not self.was_dir and self.skip:
            sslog(
                "Syntax Error. You can only create things inside a folder. skipping", t
            )
            return

        if self.is_user_home:
            # self.is_user_home = False
            self.cwd = os.path.expanduser("~")
            self.is_user_home = False

        if self.is_dir:
            folder_name = Lex._clean_name(t.value)

            if self.is_read_only:
                # print('nothing can be created in this block')
                # TODO - only if its the last item in the tree
                get_file_info(self.cwd, folder_name)
                # with open(fileinfo['path'], 'r') as f:
                # fileinfo['data'] = f.read()

                try:
                    # if not the last line still need to navigate into it if it exists.
                    # also if not then stop nest ones being created also
                    os.chdir(os.path.join(self.cwd, folder_name))  # this should now error if it doesn't exist
                    self.depth += 1
                    self.cwd = os.getcwd()
                except FileNotFoundError as e:
                    sslog(f"""Folder '{folder_name}' not created. read_only. 

                    remove the colon from the line if you want to create the folder
                    
                    """)
                    # raise e
                    self.is_dead = True
                    self.dead_depth = self.depth
                    # if self.depth == 0:
                        # self.is_dead = False
                        # self.dead_depth = 0 # hacky
                    self.depth += 1
                    # self.cwd = os.getcwd()
                    
                    return

            else:
                if not self.delete:
                    if not os.path.exists(os.path.join(self.cwd, folder_name)):

                        if tree.TEST_MODE:
                            # TODO - doesn't windows have backslash?
                            sslog(f"TEST_MODE: create folder: {self.cwd}{os.sep}{folder_name}")
                            self.depth += 1
                            self.cwd += f"{os.sep}{folder_name}"
                            return
                        else:
                            os.mkdir(os.path.join(self.cwd, folder_name))
                            sslog("created folder", folder_name)
                        # os.mkdir(os.path.join(self.cwd, folder_name))
                    else:
                        sslog("folder already exists")

                    os.chdir(os.path.join(self.cwd, folder_name))
                    self.depth += 1
                    self.cwd = os.getcwd()
                else:
                    Lex._remove_file_or_folder(os.path.join(self.cwd, folder_name))
                    # os.rmdir(os.path.join(self.cwd, folder_name))
                    # self.depth -= 1
                    # self.cwd = os.getcwd()
        
        
        else: # incase you forgot. It's not a folder its a file
            
            # print(t.value)
            file_name = Lex._clean_name(t.value)

            if self.is_read_only:
                # print('in the file block')
                # TODO - only if its the last item in the tree
                get_file_info(self.cwd, file_name)

                # with open(fileinfo['path'], 'r') as f:
                # fileinfo['data'] = f.read()

            else:
                if not self.delete:

                    if tree.TEST_MODE:
                        # TODO - doesn't windows have backslash? test on my other machine later
                        sslog(f"TEST_MODE: create file: {self.cwd}{os.sep}{file_name}")
                    else:
                        if not os.path.exists(os.path.join(self.cwd, file_name)):
                            with open(os.path.join(self.cwd, file_name), "w") as f:
                                f.write(t.value)
                        else:
                            sslog("file already exists")

                else:
                    try:
                        # os.remove(os.path.join(self.cwd, file_name))
                        Lex._remove_file_or_folder(os.path.join(self.cwd, file_name))
                        return
                    except Exception as e:
                        sslog("could not delete file", e)

    def t_error(self, t):
        sslog(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    @staticmethod
    def _clean_name(name: str):  # -> str:
        """[makes sure the name is valid]

        Args:
            name (str): [a file or folder name]

        Returns:
            [str]: [the name cleaned if necessary]
        """
        return name.replace("\n", "").replace("\t", "")

    @staticmethod
    def _remove_file_or_folder(path: str):

        if tree.TEST_MODE:
            sslog(f"TEST_MODE: removing file: {path}")
            return

        # detect if its a file or folder
        if os.path.isfile(path):
            # remove it
            os.remove(path)
        elif os.path.isdir(path):
            # remove it even if it has contents
            shutil.rmtree(path)
            # on windows
            # os.system('rmdir /S /Q "{}"'.format(path))
        else:
            sslog("No file or folder could be found at", path)
            pass

    # @staticmethod
    # def create_symbolic_link(path: str):

    def __str__(self):
        return f"Lexer: {self.cwd}"


class tree(object):

    TEST_MODE = False  # wont actually create files
    QUIET_MODE = False  # TODO suppress all logs
    VERBOSE_MODE = False  # outputut logs to file

    # stores read info
    FILE_INFO = None

    def __str__(self):
        return tree.FILE_INFO

    # def __repr__(self):
    #     return tree.FILE_INFO

    def __format__(self, *args, **kwargs):
        # return tree.FILE_INFO
        # TODO - format the outputut to look like ls -al
        # -rw-r--r--@ 1 byteface  staff  2100 21 Sep 07:58 README.md
        # print('info::', tree.FILE_INFO)
        output = ""
        if tree.FILE_INFO is not None:
            if tree.FILE_INFO["is_dir"]:
                output += "d"
            else:
                output += "-"
            output += tree.FILE_INFO["perms"]
            output += " "
            output += str(tree.FILE_INFO["owner"])
            output += " "
            output += str(tree.FILE_INFO["group"])
            output += " "
            output += str(tree.FILE_INFO["size"])
            output += " "
            output += str(tree.FILE_INFO["date"])
            output += " "
            output += str(tree.FILE_INFO["name"])
            output += "\n"
        return output

    def __init__(self, tree_string: str, test: bool = False):
        """

        Args:
            tree_string
                - a string following the format carefully layed out in the sharpshooter specifcation (the notes in the readme)

        """
        tree.TEST_MODE = test
        tree_string = tree_string.replace("\t", "    ")  # force tabs to 4 spaces

        if tree.TEST_MODE:
            sslog(f"TEST_MODE is active. Changes will not be applied.")

        self.lexer = Lex()
        self.lexer.lexer.input(tree_string)
        while True:
            tok = self.lexer.lexer.token()
            if not tok:
                break

    # def loads(self):
    #     """[summary]
    #     """
    #     with open(self.file_name, 'r') as f:
    #         return f.read()

    # @staticmethod
    # def _(self, tree_string: str, test: bool = False):
    #     """[creates files and directories based on the given rules ]

    #     Args:
    #         tree (str): [rules to create files and directories]
    #     """
    # self.lexer = Lex()
    # self.lexer.lexer.input(tree_string)
    # while True:
    #     tok = self.lexer.lexer.token()
    #     if not tok:
    #         break


"""
class d_():
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        return f'+{self.name}{self.args}, {self.kwargs})' # TODO - colon / read only


class f_():
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
    def __str__(self):
        return f'+{self.name}{self.args}, {self.kwargs})'
"""
