"""
    tree (sharpshooter)

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
    d_('somedir', 
        f_('file1', chmod=755),
        d_('things', 'file2.txt', 'file3.txt')
    )

"""

import os
import ply.lex as lex


class Lex(object):

    def __init__(self):
        
        # flags
        self.root = os.getcwd() # may not need
        self.is_root = True
        self.depth = 0
        self.cwd = None
        self.is_dir = True
        self.was_dir = True # hacky to always start true?
        self.skip = False
        self.is_read_only = False
        self.is_comment = False
        self.is_recursive = False
        self.is_test = False
        self.tab_count = 0
        self.last_tab_count = 0

        self.start_tabs = 0  # if a whole block is indented, this is the number of tabs where to start from
        self.first = True # set to false after the first file or folder is created
        

        self.lexer = lex.lex(module=self)
    
    tokens = (
        'FILE',
        'PLUS','MINUS','TIMES','EQUALS','COLON','TAB','SPACE',
        # 'NEWLINE',
        'LPAREN','RPAREN','COMMENT'
        )

    # Ignored characters
    # t_ignore = " \t"
    t_ignore_COMMENT = r'\#.*'
    # ignore spaces before comments
    # t_ignore_SPACESCOMMENTFIX = r'[ ]+' + r'\#.*' # note - not working ?


    def t_newline(self, t):
        r'\n+'
        print('NEWLINE')
        t.lexer.lineno += t.value.count("\n")
        # print('t_newline', t)
        # reset the flags
        # global tab_count
        # global is_dir
        # global was_dir
        # global is_read_only
        # global skip
        # tab_count = 0
        print( "seting:::", self.is_dir, self.was_dir)
        self.was_dir = self.is_dir
        self.is_dir = False
        self.is_read_only = False
        self.is_comment = False
        self.is_recursive = False # TODO - will need to be a 2nd pass as creation of all files is not complete
        self.skip = False
        self.is_root = True
        print( "SET IS ROOT TRUE!" )

    def t_PLUS(self, t):
        r'\+'
        # print('t_PLUS', t)
        # global is_dir
        # global was_dir
        self.is_dir = True
        # was_dir = is_dir

    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    def t_WRITE(self, t):
        r'\<'
        print('writing:::')
    # t_DIVIDE  = r'/'
    # t_COLON  = r':'
    def t_COLON(self, t):
        r'\:'
        # print('t_COLON', t)
        # global is_read_only
        self.is_read_only = True

    def t_TAB(self, t):
        r'[\t]+'
        print("Tab(s)")
        print('t_TAB', t)
        self.move_back(len(t.value))

    def t_SPACE(self, t):
        r'[ ]+'
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

        spaces = int(len(t.value)/4)

        if self.first:
            self.start_tabs = spaces
            return

        spaces -= self.start_tabs
        # if spaces < self.start_tabs:
            # return

        self.move_back(spaces)

    def move_back(self, spaces):  # counts the spaces and moves back
        # global depth
        # global cwd
        # global tab_count
        # global last_tab_count
        # global skip
        self.is_root = False # hacky. it wont get called if no space
        print( "SET IS ROOT FALSE!" )
        print('move_back', self.depth, spaces)
        # tab_count = depth - spaces
        self.last_tab_count = self.tab_count
        self.tab_count = self.depth - spaces
        print('tab_count', self.tab_count)
        if self.tab_count < 0:
            self.tab_count = self.last_tab_count
            self.skip = True
            print('Error. You can only put things in folders')
            return

        while self.tab_count > 0:
            print('moving back a dir!')
            print(os.getcwd())
            path_parent = os.path.dirname(os.getcwd())
            os.chdir(path_parent)
            self.cwd = os.getcwd()
            print(os.getcwd())
            self.depth -= 1
            self.tab_count -= 1

    # t_NEWLINE  = r'\n'
    t_EQUALS  = r'='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'

    def t_FILE(self, t):
        # r'[a-zA-Z_][a-zA-Z_0-9.\-]*[\n\s\r]'
        r'[a-zA-Z_][a-zA-Z_0-9.\-]*'
        # print('file', t)
        # print('tab_count', tab_count)
        # print('is_dir', is_dir)
        # print('is_read_only', is_read_only)
        # print('is_comment', is_comment)
        # print('is_recursive', is_recursive)
        # global depth
        # global cwd
        # global was_dir
        # global tab_count
        # global last_tab_count
        # global skip
        if self.cwd is None:
            self.cwd = os.getcwd()
            # print('cwd:', cwd)

        print( "ARE WE ROOT?!", self.is_root )
        if self.is_root:
            print('so change it')
            # change dir to root
            os.chdir(self.root)
            self.cwd = os.getcwd()
            print(os.getcwd())

        if self.first:
            self.first = False

        print( 'WAS??::', self.was_dir, self.tab_count, self.last_tab_count)
        if not self.was_dir and self.skip:#tab_count<0:#(tab_count>last_tab_count):
            print('Syntax Error. You can only create things inside a folder. skipping', t)
            # tab_count = last_tab_count
            # tab_count = depth+1 # reset tab count to depth
            # last_tab_count = depth+1
            return

        if self.is_dir:
            print(t.value)
            folder_name = Lex._clean_name(t.value)
            # print(folder_name)

            print("CWD>>",self.cwd)
            if not os.path.exists(os.path.join(self.cwd, folder_name)):
                os.mkdir(os.path.join(self.cwd, folder_name))
            else:
                print('folder already exists')

            # print('changing cwd to', os.path.join(self.cwd, folder_name))
            # os.chdir(folder_name)
            os.chdir(os.path.join(self.cwd, folder_name))
            self.depth += 1
            self.cwd = os.getcwd()
            # prev_cwd = cwd
            # print('cwd:', os.getcwd())
        else:
            print(t.value)
            file_name = Lex._clean_name(t.value)
            # print(file_name)

            print("CWD>>",self.cwd)

            if not os.path.exists(os.path.join(self.cwd, file_name)):
                with open(os.path.join(self.cwd, file_name), 'w') as f:
                    f.write(t.value)
            else:
                print('file already exists')

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    @staticmethod
    def _clean_name(name: str):# -> str:
        """[makes sure the name is valid]

        Args:
            name (str): [a file or folder name]

        Returns:
            [str]: [the name cleaned if necessary]
        """
        return name.replace('\n','').replace('\t','')


class tree(object):

    def __init__(self, tree_string: str, test: bool = False):
        """

        Args:
            tree_string 
                - a string following the format carefully layed out in the treez specifcation (the notes in the readme)

        """
        tree_string = tree_string.replace('\t','    ') # force tabs to 4 spaces

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
    # def _(self, rules: str):
    #     """[creates files and directories based on the given rules ]

    #     Args:
    #         tree (str): [rules to create files and directories]
    #     """
    #     instructions = self.parse(rules)
    #     for instruction in instructions:
    #         self.run(instruction)

'''
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
'''
