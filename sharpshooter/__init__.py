"""
    tree (sharpshooter)
    ====================================

    A shorthand syntax for creating files and folders.

    /dir
        file.txt < hello world

"""

__version__ = "0.2.2"
__license__ = "MIT"
__author__ = "@byteface"

VERSION = __version__

import os
import shutil
import ply.lex as lex
import warnings

try:
    TREE_ICN = "\U0001F333"
    FOLDER_ICN = "\U0001F4C1"
    FILE_ICN = "\U0001F4DD"
    ERR_ICN = "\U0000274C"
    WARN_ICN = "\U000026A0"
    OK_ICN = "\U00002714"
    # TODO - this breaks 'quiet mode'
    print(VERSION, TREE_ICN, FOLDER_ICN, FILE_ICN, ERR_ICN, WARN_ICN, OK_ICN)
except UnicodeEncodeError:
    warnings.warn("Warning: Icons not supported.")
    TREE_ICN = ""
    FOLDER_ICN = ""
    FILE_ICN = ""
    ERR_ICN = ""
    WARN_ICN = ""
    OK_ICN = ""


def term(cmd: str) -> str:
    """run

    runs any command on the terminal

    Args:
        cmd (str): The command you want to run on the terminal

    Returns:
        str: the response as a string
    """
    sslog("    - command: " + cmd)
    if tree.TEST_MODE:
        sslog(
            'TEST_MODE',
            'command not run:',
            cmd,
            lvl='w'
        )
        return  # cmd
    import subprocess
    returned_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    try:
        returned_output = returned_output.decode('utf-8')
    except:
        returned_output = returned_output.decode('cp1252')  # latin-1
    return returned_output

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


def sslog(msg: str, *args, lvl: str = None, **kwargs):
    """logging for sharpshooter"""
    if tree.QUIET_MODE:
        return

    # if tree.VERBOSE_MODE:
    #     import sys
    #     old_log = sys.stdout
    #     log_file = open("tree.log","w") # will need to fix tree.root
    #     sys.stdout = log_file
    #     print(msg)
    #     sys.stdout = old_log

    if lvl is None:
        print(msg, args, kwargs)
    elif 'e' in lvl:  # error
        print(f"{ERR_ICN} \033[1;41m{msg}\033[1;0m", *args, kwargs)
    elif 'w' in lvl:  # warning
        print(f"{WARN_ICN} \033[1;31m{msg}\033[1;0m", *args, kwargs)
    elif 'g' in lvl:  # green for good
        print(f"{OK_ICN} \033[1;32m{msg}\033[1;0m", *args, kwargs)


def octal_to_text(octal) -> str:
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


def get_file_info(path: str, filename: str) -> dict:
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
        sslog("WINDOWS:::::", owner, 'w')

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
        sslog("WINDOWS:::::", group, 'w')
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
        # as we parse lines we set flags to instruct the parser what to do.
        # most are reset on each line. (see t_newline)
        self.root = os.getcwd()  # may not need
        self.is_root: bool = True
        self.depth: int = 0
        self.cwd: str = None
        self.is_dir: bool = True
        self.was_dir: bool = True  # hacky to always start true?
        self.skip: bool = False
        self.is_read_only: bool = False
        self.is_comment: bool = False
        self.is_recursive: bool = False
        self.is_test: bool = False
        self.tab_count: int = 0
        self.last_tab_count: int = 0
        self.is_user_home: bool = False  # tilde handler

        self.start_tabs: int = 0  # if a whole block is indented, this is the number of tabs where to start from
        self.first: bool = True  # set to false after the first file or folder is created

        self.delete: bool = False

        self.is_extra: bool = False  # need maybe a better variable name.
        # basically, if we are past the filename or dirname, we are in the extra stuff

        # self.last_thing_created
        # self.last_folder_created = None
        self.last_file_created: str = None   # the last file created. see notes below
        # after is_extra this would be the one on the current line. however before that it would be from a previous line.

        self.is_dead: bool = False  # if a dir fails to create, we can mark it as dead
        self.dead_depth: int = 0  # the depth of the dead dir

        self.labels: list = []  # list of tree labels (branches)
        self.current_label: str = None  # the label of the current tree
        self.empty_line: bool = False  # set true by filename check. if left false the newline checker knows to reset current_label

        # self.chmod_mode = None
        # self.chmod_owner = None
        # self.chmod_group = None
        # self.chmod_perms = None
        # self.write_mode = None

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
        "BACKSLASH",
        "SLASH",
    )

    # Ignored characters
    # t_ignore = " \t"
    t_ignore_COMMENT = r"\#.*"
    # ignore spaces before comments
    # t_ignore_SPACESCOMMENTFIX = r'[ ]+' + r'\#.*' # note - not working ?

    def t_label(self, t):
        r"\#\["
        self.empty_line = False

        content = t.lexer.lexdata[t.lexer.lexpos:]
        if content.find("\n") != -1:
            content = content[:content.find("\n")]
        original_length = len(content)
        content = '\n'.join(content.split('\\n'))
        if content[0] == " ":
            content = content[1:]
        # split at the first space
        content = content.split(" ", 1)[0]
        # if last is a ']' then remove it
        if content[-1] == "]":
            content = content[:-1]

        # sslog('cl:', self.current_label)
        if content not in self.labels:
            # sslog('Adding a label:', self.current_label, lvl='g')
            self.labels.append(self.current_label)
            self.current_label = content
        else:
            pass
            # sslog('Creating a branch:', content, lvl='g')
            # TODO - this is a potential can of worms. (mainly due to catching incorrect use cases)
            # if branch exists already, then make it
            # TODO - may need to save cwd and restore?
            # cwd = os.getcwd()
            # TODO - these cant be constants for this to work. (will need to pass vars)
            # note - the lexer itself allows for custom props
            # tree(self.lexer.lexdata, test=tree.TEST_MODE, quiet=tree.QUIET_MODE, label=tree.LABEL)
            # os.chdir(cwd)

        t.lexer.skip(original_length)

    def t_newline(self, t):
        r"\n+"
        if tree.LABEL is not None:
            if self.current_label != tree.LABEL:
                tree.TEST_MODE = True
                tree.QUIET_MODE = True
            else:
                tree.TEST_MODE = tree._TEST_MODE_BAK
                tree.QUIET_MODE = tree._QUIET_MODE_BAK

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

        if self.empty_line:
            self.current_label = None

        self.empty_line = True

        # This allows us to have multiple root dirs/files
        # NOTE - not sure if this is best way. But it took a while to get to this point. (or to understand why it has to be this way)
        # basically. lines with spaces cause flags to be set, however if there's no space, no flags get checked
        # so for tree to have multiple root paths. we need to know if the oncoming line is a dir or file.
        # so if next char is not a space reset the tab count and depth
        try:
            if t.lexer.lexdata[t.lexer.lexpos] != " ":
                self.tab_count = 0
                self.depth = 0
                # note - we may have to reset more than just that. (keep an eye on this)
        except IndexError:
            # we came to the end of the file
            pass

        # TODO - root safety check
        # really should never allow cwd to be lower than root

    def t_TILDE(self, t):
        r"\~"
        self.is_user_home = True
        # self.depth += 1
        # self.is_root = False

    # def t_PLUS(self, t):
    #     r"\+"
    #     self.is_dir = True

    def t_SLASH(self, t):
        r"\/"
        self.is_dir = True

    def t_MINUS(self, t):
        r"\-"
        self.delete = True  # todo: - test it doesn't remove hyphenated words

    t_TIMES = r"\*"
    t_BACKSLASH = r"\\"
    # def t_BACKSLASH(self, t):
    #     r"\\"
    #     self.lexer.lexpos += 1 # no as this means we don't get the char
    #     return t

    def t_APPEND(self, t):  # literally same as write but uses 'ab' to open the file
        r"\<<"

        content = t.lexer.lexdata[t.lexer.lexpos:]
        if content.find("\n") != -1:
            content = content[:content.find("\n")]
        original_length = len(content)
        content = '\n'.join(content.split('\\n'))
        if content[0] == " ":
            content = content[1:]

        if tree.TEST_MODE:
            sslog(
                'TEST_MODE',
                'skip appending content to this file:',
                self.last_file_created,
                lvl='w'
            )
        else:
            self.last_file_created = self.last_file_created.strip()  # ensure remove trailing spaces
            with open(self.last_file_created, "ab") as f:
                # f.write(content)
                f.write(content.encode())
                sslog(f'    - Appending content to {self.last_file_created}')
                f.close()
        t.lexer.skip(original_length)

    def t_WRITE(self, t):
        r"\<"
        # r"\<\s"
        content = t.lexer.lexdata[t.lexer.lexpos:]
        if content.find("\n") != -1:
            content = content[:content.find("\n")]

        original_length = len(content)

        content = '\n'.join(content.split('\\n'))
        # content = data  # t.lexer.lexdata[t.lexer.lexpos:]
        # if first char is space remove it
        if content[0] == " ":
            content = content[1:]

        if self.is_dir:
            sslog('Syntax Error', 'Cannot write string to a directory on line:', t.lexer.lineno, lvl='e')
            t.lexer.skip(original_length)
            return

        # TODO - use the filestream class to do various things

        # print the path to the file just created
        # sslog('Write content into this file:', self.last_file_created)
        if tree.TEST_MODE:
            sslog('TEST_MODE', 'skip writing content into this file:', self.last_file_created, lvl='w')
        else:
            self.last_file_created = self.last_file_created.strip()  # ensure remove trailing spaces
            with open(self.last_file_created, "w+", encoding="utf-8") as f:
                f.write(content)
                sslog(f'    - Writing into {self.last_file_created}')
                f.close()
            # sslog("wrote content into this file:", self.last_file_created)

        # skip the rest of the line
        t.lexer.skip(original_length)

    def t_sh(self, t):
        r"\$"
        # r"\$\s"  # space after the $ reduce odds of it being a filename
        self.empty_line = False

        data = t.lexer.lexdata[t.lexer.lexpos:]
        if data.find("\n") != -1:
            data = data[:data.find("\n")]
        cmd = data

        original_cmd_len = len(cmd)  # so we can skip the rest of the line
        # if first char is space remove it
        if cmd[0] == " ":
            cmd = cmd[1:]

        # if windows skip the line
        if os.name == 'nt':
            t.lexer.skip(original_cmd_len)
            sslog("skipping bash line on windows", lvl='w')
            return

        # run a shell command with subprocess and return the result
        content = term(cmd)

        # sslog('write content into this file:', self.last_file_created)
        if tree.TEST_MODE:
            sslog('TEST_MODE', 'skip writing content into this file:', self.last_file_created, lvl='w')
        else:
            self.last_file_created = self.last_file_created.strip()  # ensure remove trailing spaces
            with open(self.last_file_created, "w") as f:
                sslog(f'    - Writing to {self.last_file_created}')
                f.write(content)
                f.close()
            # sslog("wrote content into this file:", self.last_file_created)

        # skip the rest of the line
        # t.lexer.skip(len(t.lexer.lexdata) - t.lexer.lexpos)
        t.lexer.skip(original_cmd_len)

    def t_cmd(self, t):
        r"\>"
        # r"\>\s"
        self.empty_line = False

        data = t.lexer.lexdata[t.lexer.lexpos:]
        if data.find("\n") != -1:
            data = data[:data.find("\n")]
        # print('data:::::', data)
        cmd = data
        original_cmd_len = len(cmd)  # so we can skip the rest of the line later
        # if first char is space remove it
        if cmd[0] == " ":
            cmd = cmd[1:]

        # if not windows skip the rest of the line
        if os.name != 'nt':
            t.lexer.skip(original_cmd_len)
            sslog("IGNORE not windows::: skipping rest of line")
            return

        # run a shell command with subprocess and return the result
        content = term(cmd)
        # print('RESULT:', content)

        # print the path to the file just created
        # sslog('write content into this file:', self.last_file_created)
        if tree.TEST_MODE:
            sslog('TEST_MODE', 'skip writing content into this file:', self.last_file_created, lvl='w')
        else:
            self.last_file_created = self.last_file_created.strip()  # ensure remove trailing spaces
            with open(self.last_file_created, "w") as f:
                sslog('    - Writing to', self.last_file_created)
                f.write(content)
                f.close()
            # sslog("wrote content into this file:", self.last_file_created)

        # skip the rest of the line
        # t.lexer.skip(len(t.lexer.lexdata) - t.lexer.lexpos)
        t.lexer.skip(original_cmd_len)

    # t_DIVIDE  = r'/'
    def t_COLON(self, t):
        r"\:"
        self.is_read_only = True

    def t_QUESTION(self, t):
        r"\?"
        self.empty_line = False

        if self.is_extra:
            # gets the question
            question = t.lexer.lexdata[t.lexer.lexpos:]
            if question.find("\n") != -1:
                question = question[:question.find("\n")]
            original_length = len(question)
            question = '\n'.join(question.split('\\n'))
            if question is not None and question != "":
                if question[0] == " ":
                    question = question[1:]
            # print(question)
            # NOTE - not logs, they are questions so should not be supressed
            print("\n")
            sslog("Editing: ", self.last_file_created, lvl='g')
            print("************************************************************")
            print("Multi-line editor: Ctrl-D or (Ctrl-Z then Return on windows) to save.")
            print("TIP: Press Return for an empty newline BEFORE saving.")
            print("************************************************************")
            print(f"{FILE_ICN} Enter/Paste your content.")
            print("************************************************************")

            # TODO - you can't pass existing file content into the input easily
            # i do have a branch that can break into vim and return.
            # but that wont work for windows. so will have a think about it.

            contents = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                contents.append(line)
            content = '\n'.join(contents)

            if tree.TEST_MODE:
                sslog(
                    'TEST_MODE',
                    'Skip writing content into this file:',
                    self.last_file_created,
                    lvl='w')
            else:
                self.last_file_created = self.last_file_created.strip()  # ensure remove trailing spaces
                with open(self.last_file_created, "w+", encoding="utf-8") as f:
                    f.write(content)
                    sslog(f'    - Writing into {self.last_file_created}')
                    f.close()
                # sslog("wrote content into this file:", self.last_file_created)

            t.lexer.skip(original_length)
        else:
            filetype = 'folder' if self.is_dir else 'file'
            # NOTE - not a log. questions should not be supressed
            print('What would you like the ' + filetype + ' to be called?')
            line = input()

            class mock():
                value = line
            t = mock()
            self.t_FILE(t)

    def t_TAB(self, t):
        r"[\t]+"
        self.move_back(len(t.value))

    def t_SPACE(self, t):
        r"[ ]+"
        if self.is_extra:
            return  # TODO - for now ignoring anything after the filename

        spaces = int(len(t.value) / 4)

        if self.first:
            self.start_tabs = spaces
            return

        spaces -= self.start_tabs

        self.move_back(spaces)

    def move_back(self, spaces: int):
        """[counts the spaces and moves back up the directory tree]

        Args:
            spaces ([int]): [how many steps to move back up the directory tree]
        """
        self.is_root = False  # hacky. it wont get called if no space
        self.last_tab_count = self.tab_count
        self.tab_count = self.depth - spaces
        if self.tab_count < 0:
            self.tab_count = self.last_tab_count
            self.skip = True
            sslog("Error.", "You can only put things in folders", lvl='e')
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
            # print(self.depth, self.tab_count, self.cwd)

    t_EQUALS = r"="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    def t_FILE(self, t):
        # r"[a-zA-Z_0-9.\-][a-zA-Z_0-9.\-]*([\w. ]*)"  # TODO - backslash token to allow starting with +-
        # r"[\w.\-][\w.\-]*([\w. ]*)" #? is this just same as above?
        # pasting all special characters into it 3 times...
        # r"[\w.><?@+'`~^%&\*\[\]\{\}.!#|\\\"$';,:;=/\(\),\-][\w.><?@+'`~^%&\*\[\]\{\}.!#|\\\"$';,:;=/\(\),\-]*([\w.><?@+'`~^%&\*\[\]\{\}.!#|\\\"$';,:;=/\(\),\-]*)"
        # seems to pass.
        # but... i assume that's not all the special chars in the universe?. does \w handle umlauts?
        # aw heck...!. no comments chars as first char. added pound sign. and a space. remove special chars in word end.
        r"[\w.><?@+'`~^%&\*\[\]\{\}.!|\\\"$£';,:;=/\(\),\-][\w.><?@+'`~^%&\*\[\]\{\}.!#|\\\"$£';,:;=/\(\),\-]*([\w.@+'`~^%&\*\[\]\{\}.!#|\\\"£';,:;=/\(\),\- ]*)"
        # may need to escape any words that first char is token? (or use '')?

        self.empty_line = False

        if self.cwd is None:
            self.cwd = os.getcwd()

        if self.is_root:
            os.chdir(self.root)
            self.cwd = os.getcwd()

        if self.first:
            self.first = False

        self.is_extra = True  # lets the spacer know we are past the filename or dirname

        if self.is_dead:
            if self.depth <= self.dead_depth:
                sslog("Same depth as previous dead dir. no longer dead:", t.value)
                self.is_dead = False
                self.dead_depth = 0
            else:
                sslog("Skipping dead dir", t.value)
                return

        if not self.was_dir and self.skip:
            sslog(
                "Syntax Error.",
                "You can only create things inside a folder. skipping",
                t,
                lvl='e')
            return

        if self.is_user_home:
            self.cwd = os.path.expanduser("~")
            self.is_user_home = False

        if self.is_dir:
            folder_name = Lex._clean_name(t.value)

            if self.is_read_only:
                # print('nothing can be created in this block')
                # TODO - only if its the last item in the tree
                get_file_info(self.cwd, folder_name)

                try:
                    # if not last line still navigate into it, if exists
                    # also if not then stop nested ones being created also
                    os.chdir(
                        os.path.join(self.cwd, folder_name)
                    )  # this should now error if it doesn't exist
                    self.depth += 1
                    self.cwd = os.getcwd()
                except FileNotFoundError as e:
                    sslog(
                        f"Folder '{folder_name}' not created. read_only."
                        "remove the colon from the line if you want to create the folder",
                        lvl='e'
                    )
                    self.is_dead = True
                    self.dead_depth = self.depth
                    self.depth += 1
                    return

            else:

                if not self.delete:

                    # Note - maybe check the path that exists actually is a folder?
                    # and it was a file created in error. if file then ask to delete it?

                    if not os.path.exists(os.path.join(self.cwd, folder_name)):
                        if tree.TEST_MODE:
                            sslog(
                                "TEST_MODE",
                                f"{FOLDER_ICN} Create folder: {self.cwd}{os.sep}{folder_name}",
                                lvl='w'
                            )
                            self.depth += 1
                            self.cwd += f"{os.sep}{folder_name}"
                            return
                        else:
                            os.mkdir(os.path.join(self.cwd, folder_name))
                            sslog(f"{FOLDER_ICN} Created folder: {self.cwd.replace(self.root, '')}{os.sep}{folder_name}", lvl='g')
                    else:
                        sslog(f"Folder called {folder_name} already exists", lvl='w')

                    os.chdir(os.path.join(self.cwd, folder_name))
                    self.depth += 1
                    self.cwd = os.getcwd()
                else:
                    Lex._remove_file_or_folder(os.path.join(self.cwd, folder_name))
                    # test - these vars below were for read only mode. but may work here too.
                    # issue is a minus dir with children. the children still get created 1 higher.
                    self.is_dead = True
                    self.dead_depth = self.depth
                    self.depth += 1

        else:  # incase you forgot. It's not a folder its a file

            file_name = Lex._clean_name(t.value)
            if self.is_read_only:
                # print('in the file block')
                # TODO - only if its the last item in the tree
                get_file_info(self.cwd, file_name)

            else:
                if not self.delete:

                    if tree.TEST_MODE:
                        sslog(
                            "TEST_MODE",
                            f"{FILE_ICN} Create file: {self.cwd}{os.sep}{file_name}",
                            lvl='w'
                        )
                    else:
                        if not os.path.exists(os.path.join(self.cwd, file_name)):
                            with open(os.path.join(self.cwd, file_name), "w") as f:
                                f.write("")  # t.value
                                f.close()
                            sslog(
                                f"{FILE_ICN} Created file:",
                                f"{self.cwd.replace(self.root, '')}{os.sep}{file_name}",
                                lvl='g'
                            )
                        else:
                            sslog(f"File called {file_name} already exists.", lvl='w')

                    self.last_file_created = os.path.join(self.cwd, file_name)
                    self.last_file_created = self.last_file_created.strip()

                else:
                    try:
                        # os.remove(os.path.join(self.cwd, file_name))
                        Lex._remove_file_or_folder(os.path.join(self.cwd, file_name))
                        return
                    except Exception as e:
                        sslog("Could not delete file", lvl='e')

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
        name = name.replace("\n", "").replace("\t", "")
        return name.strip()

    @staticmethod
    def _remove_file_or_folder(path: str):
        if tree.TEST_MODE:
            sslog(
                "TEST_MODE",
                f"Remove file or folder {path}",
                lvl='w'
            )
            return

        # detect if its a file or folder
        if os.path.isfile(path):
            sslog(f"Removing file: {path}", lvl='g')
            os.remove(path)
        elif os.path.isdir(path):
            sslog(f"Removing folder: {path}", lvl='g')
            shutil.rmtree(path)
            # on windows # ?? still not tested?
            # os.system('rmdir /S /Q "{}"'.format(path))
        else:
            sslog("No file or folder could be found at", path, lvl='w')
            pass

    # @staticmethod
    # def create_symbolic_link(path: str):

    def __str__(self):
        return f"Lexer: {self.cwd}"


class tree(object):

    _TEST_MODE_BAK: bool = False  #: private. used to hijack the test mode
    _QUIET_MODE_BAK: bool = False  #: private used to hijack the quiet mode

    TEST_MODE: bool = False  #: wont actually create files
    QUIET_MODE: bool = False  #: suppress all logs
    VERBOSE_MODE: bool = False  #: outputut logs to file

    LABEL: str = None  # 'cat' #: the label of the tree. if set trees without this label will be ignored

    FILE_INFO = None  #: stores read info

    def __str__(self) -> str:
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

    def __init__(
        self,
        tree_string: str,
        test: bool = False,
        quiet: bool = False,
        label: str = None):
        """

        Args:
            tree_string (string): [A string in the format expected by the sharpshooter lexer]
            test (bool, optional): [if true, will not actually create files or folders]. Defaults to False.

        """
        # TODO - put all these as regular vars on the lexer
        tree._QUIET_MODE_BAK = tree.QUIET_MODE = quiet
        tree.LABEL = label

        CWD_b4 = os.getcwd()

        sslog(f"{TREE_ICN} tree")
        tree._TEST_MODE_BAK = tree.TEST_MODE = test
        self.tree_string = tree_string.replace("\t", "    ")  # force tabs to 4 spaces
        if tree.TEST_MODE:
            sslog("TEST_MODE", "testmode is active. Changes will not be applied.", lvl='w')

        self.lexer = Lex()
        self.lexer.lexer.input(self.tree_string)
        while True:
            tok = self.lexer.lexer.token()
            if not tok:
                break

        # return to the original cwd
        os.chdir(CWD_b4)

    @staticmethod
    def mock(depth=0):
        """Create a .tree string from the current working directory

        Returns:
            [str]: [a tree string]
        """
        tree_string = ""
        limit = depth  # depth is used for spacing so can't be none. so use limit

        def walk_dir(dir_path: str, depth: int = 0):
            # print('depth:::', depth)
            nonlocal tree_string
            nonlocal limit
            if depth > limit:
                return
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)
                if os.path.isdir(file_path):
                    tree_string += "    " * depth
                    tree_string += "/"+file_name
                    tree_string += "\n"
                    walk_dir(file_path, depth + 1)
                else:
                    tree_string += "    " * depth
                    tree_string += file_name
                    tree_string += "\n"

        # TODO - this will have to escape any words where the first char is a sharpshooter token

        walk_dir(os.getcwd())
        # print(tree_string)
        return tree_string

    @staticmethod
    def pretty(tree_string: str) -> str:
        """
        ## changes this
        # /brain
        #     /mind
        #         README.md
        #         __init__.py
        #         a.py
        #         b.py
        #         /perspect

        ## to look like this
        # brain
        # ├── README.md
        # └── mind
        #     ├── README.md
        #     ├── __init__.py
        #     ├── a.py
        #     ├── b.py
        #     └── perspect
        """
        # print('lets go!')
        new_tree_string = ""
        lines = tree_string.split("\n")
        for count, line in enumerate(lines):
            if line.strip(' ').lstrip(' ').strip('\n') == "":
                continue
            spaces = (len(line) - len(line.lstrip())) - 4  # the 4 is our pattern
            line = line.lstrip()
            line = line.lstrip("/")  # remove preceding slash if exists

            is_last_child = True
            if count < len(lines) - 1:
                next_line = lines[count + 1]
                next_line_spaces = (len(next_line) - len(next_line.lstrip())) - 4
                if next_line_spaces == spaces:
                    is_last_child = False

                # unless its the last line of the file. the it is the last child
                if count+2 >= len(lines)-1:  # is better to check if 2 empty lines ahead?
                    is_last_child = True

                next_line = next_line.lstrip()
                next_line = next_line.lstrip("/")

            if spaces > -4:
                if is_last_child:
                    new_tree_string += (spaces*' ') + '└── ' + line + "\n"
                else:
                    new_tree_string += (spaces*' ') + '├── ' + line + "\n"
            else:
                new_tree_string += line + "\n"

        # not bad. Let's go through again backwards and patch it up

        reversed_lines = new_tree_string.split("\n")
        new_tree_string_reversed = '\n'.join(reversed_lines[::-1])

        prev_pos = None
        gaps = []
        newlines = ""
        prevline = None
        for count, line in enumerate(new_tree_string_reversed.split("\n")):
            if line.strip(' ').lstrip(' ').strip('\n') == "":
                continue
            if prev_pos is not None:
                # if its a space replace with '│'
                if len(line) >= prev_pos:
                    if line[prev_pos] == ' ':
                        line = line[:prev_pos] + '│' + line[prev_pos+1:]
            for gap in gaps:
                if len(line) > gap:
                    if line[gap] == ' ':
                        if len(prevline) > gap:
                            if prevline[gap] == '│' or prevline[gap] == '└':
                                line = line[:gap] + '│' + line[gap+1:]

            # find any of these '└' record their position. if next line is space replace with '│'
            if '└' in line:
                prev_pos = line.find('└')
                gaps.append(prev_pos)

            # remove artifacts
            if '└' in line:
                pos = line.find('└')
                if prevline is not None:
                    if len(prevline) > pos:
                        if prevline[pos] == '│':
                            line = line[:pos] + '├' + line[pos+1:]

            prevline = line
            # print(line, prev_pos)
            newlines += line + "\n"

        reversed_lines = newlines.split("\n")
        new_tree_string = '\n'.join(reversed_lines[::-1])
        # print(new_tree_string)
        return new_tree_string
