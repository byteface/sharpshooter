"""
treez

An instructional shorthand for templates to create (or destroy) file systems.

treez could potentially be written in any language.
(Infact I'm going to try write it with a lexer and parser to make it more portable.)

```
pip install treez
```

To create a plain empty file just type a word i.e.

```
file
```

to create or access a dir use +

```
+dir
```

To create a file inside a dir use a 4 spaces (tab)

```
+dir
    file
```

To write a string to a file use <, >, <<, >>

```
+dir
    file < some text
    other text > file
```


putting it all together…

```
+dir
    file < some text
    +plugins
    +mail
        +vendor
	    index.html
            +something
		file.py
		file.py
```

```
from treez import tree

tree = ''' \
+dir
    file < some text
    +plugins
        +mail
            +vendor
	       index.html
               +something
		  file.py
		  file.py
'''
```

tree doesn't wait to be told. Your file system is now there.


tree can also remove dirs and files. You guessed it. With the the - minus symbol

```
tree = ''' \
+dir
    +plugins
         -mail
'''
```

But be mindful that would also create the dir and plugins dir if they didn't exist.

To read a file or folder without creation use colon :

```
tree = ''' \
+:dir
    +:plugins
        :mail
'''
```

##permissions #TODO - this isn't done yet. planning.

You can set owners/permissions on the folders as you build them with =. For recursion multiply *

```
tree = ''' \
+dir *=740 *=g+w *=bitnami:daemon
    file > some text
    +plugins
        +mail
            +vendor
	       index.html
               +something
		  file.py
		  file.sh =644 =root
'''
```

##comments

use # to comments out a line or instruction.
(warning. bug. DON'T leave a space beore the comment. Lexer will interpret it as directory change)

```
s = '''
+:dir
    file# > some text
    +plugins
        +mail
'''
```

##careful

treez can destroy your file system.

```
s = '''
-:~
'''
```


##CLI
#TODO


## TIPS

Use f strings to Mixin your own functions… ( needs python so won't work from CLI )

```
get_readme = lambda : •.get('https://xyz…')

tree = f''' \
+dir *=740 *=g+w *=bitnami:daemon
    README.md > {get_readme()}
    +plugins
        +mail
            +vendor
	       index.html
               +something
		  file.py
		  file.sh =644 =root
'''
```

"""
import os

# https://www.dabeaz.com/ply/ply.html#ply_nn13

# flags
root = os.getcwd() # may not need
depth = 0
cwd = None
# tab_count = 0
is_dir = True
was_dir = True # hacky to always start true?
skip = False
is_read_only = False
is_comment = False
is_recursive = False
is_test = False

tab_count = 0
last_tab_count = 0


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


def t_newline(t):
    r'\n+'
    print('NEWLINE')
    t.lexer.lineno += t.value.count("\n")
    # print('t_newline', t)
    # reset the flags
    # global tab_count
    global is_dir
    global was_dir
    global is_read_only
    global skip
    # tab_count = 0
    print( "seting:::", is_dir, was_dir)
    was_dir = is_dir
    is_dir = False
    is_read_only = False
    is_comment = False
    is_recursive = False # TODO - will need to be a 2nd pass as creation of all files is not complete
    skip = False

def t_PLUS(t):
    r'\+'
    # print('t_PLUS', t)
    global is_dir
    # global was_dir
    is_dir = True
    # was_dir = is_dir

t_MINUS   = r'-'
t_TIMES   = r'\*'
def t_WRITE(t):
    r'\<'
    print('writing:::')
# t_DIVIDE  = r'/'
# t_COLON  = r':'
def t_COLON(t):
    r'\:'
    # print('t_COLON', t)
    global is_read_only
    is_read_only = True

def t_TAB(t):
    r'[\t]+'
    print("Tab(s)")
    print('t_TAB', t)
    move_back(len(t.value))

def t_SPACE(t):
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
    move_back(int(len(t.value)/4))

def move_back(spaces):  # counts the spaces and moves back
    global depth
    global cwd
    global tab_count
    global last_tab_count
    global skip
    print('move_back', depth, spaces)
    # tab_count = depth - spaces
    last_tab_count = tab_count
    tab_count = depth - spaces
    print('tab_count', tab_count)
    if tab_count < 0:
        tab_count = last_tab_count
        skip = True
        print('Error. You can only put things in folders')
        return

    while tab_count > 0:
        print('back up you cunt!')
        print(os.getcwd())
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        cwd = os.getcwd()
        print(os.getcwd())
        depth -= 1
        tab_count -= 1

# t_NEWLINE  = r'\n'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_FILE(t):
    # r'[a-zA-Z_][a-zA-Z_0-9.\-]*[\n\s\r]'
    r'[a-zA-Z_][a-zA-Z_0-9.\-]*'
    # print('file', t)
    # print('tab_count', tab_count)
    # print('is_dir', is_dir)
    # print('is_read_only', is_read_only)
    # print('is_comment', is_comment)
    # print('is_recursive', is_recursive)
    global depth
    global cwd
    global was_dir
    global tab_count
    global last_tab_count
    global skip
    if cwd is None:
        cwd = os.getcwd()
        # print('cwd:', cwd)

    print( 'WAS??::', was_dir,tab_count,last_tab_count)
    if not was_dir and skip:#tab_count<0:#(tab_count>last_tab_count):
        print('Syntax Error. You can only create things inside a folder. skipping', t)
        # tab_count = last_tab_count
        # tab_count = depth+1 # reset tab count to depth
        # last_tab_count = depth+1
        return

    if is_dir:
        print(t.value)
        folder_name = _clean_name(t.value)
        # print(folder_name)

        print("CWD>>",cwd)
        if not os.path.exists(os.path.join(cwd, folder_name)):
            os.mkdir(os.path.join(cwd, folder_name))
        else:
            print('folder already exists')

        # print('changing cwd to', os.path.join(cwd, folder_name))
        # os.chdir(folder_name)
        os.chdir(os.path.join(cwd, folder_name))
        depth += 1
        cwd = os.getcwd()
        # prev_cwd = cwd
        # print('cwd:', os.getcwd())
    else:
        print(t.value)
        file_name = _clean_name(t.value)
        # print(file_name)

        print("CWD>>",cwd)

        if not os.path.exists(os.path.join(cwd, file_name)):
            with open(os.path.join(cwd, file_name), 'w') as f:
                f.write(t.value)
        else:
            print('file already exists')


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()

def _clean_name(somestr):
    # removes newlines and tabs
    return somestr.replace('\n','').replace('\t','')


'''
# dictionary of names (for storing variables)
names = { }

# def p_statement_tab(p): # keep incase need the parser back
#     'statement : TAB'
#     print('p_statement_tab', p)

def p_error(p):
    try:
        print(p)
        print(f"Syntax error at {p.value!r}")
    except:
        print('End')

import ply.yacc as yacc
yacc.yacc()
'''

# class treez:

    # @staticmethod
    # def _(self, rules: str):
    #     """[creates files and directories based on the given rules ]

    #     Args:
    #         tree (str): [rules to create files and directories]
    #     """
    #     instructions = self.parse(rules)
    #     for instruction in instructions:

    # def parse(self, rules: str):
    #     """[parses the rules and returns a list of commands to run]

    #     Args:
    #         rules
    #     """

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

# s = """
# +:dir
#     file # < some text
#     +plugins
#         +mail
# """

# s = """ WRONG
# +:dir
# file1
#     file
#     +plugins
#         +mail
# """

# s = """ # TODO - should fail as file1 is not a directory. or should it get prev directory?
# +:dir
# file1
#     +plugins
#         +mail
# """

s = """ # TODO - should fail as file4 is not a directory. or should it get prev directory?
+:dir
    +plugins
        +mail
            file3
            +things
                +again
                    file8
                    file9.txt
                file7

            +more
                file6
        file4
            file5# comments are not allowed spaces before them yet. causes wrong directory
    file1# this is a file
file2
"""

lex.input(s)
while True:
    tok = lex.token()
    if not tok:
        break

# yacc.parse(s)

# another optional way is it use f_ and d_ treez builder to create the treez
# d_('somedir', 
#     f_('file1', chmod=755),
#     d_('things', 'file2.txt', 'file3.txt')
# )
