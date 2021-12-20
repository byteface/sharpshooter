# 🌳 tree (sharpshooter)

[![PyPI version](https://badge.fury.io/py/sharpshooter.svg)](https://badge.fury.io/py/sharpshooter.svg) 
[![Downloads](https://pepy.tech/badge/sharpshooter)](https://pepy.tech/project/sharpshooter)
[![Python version](https://img.shields.io/pypi/pyversions/sharpshooter.svg?style=flat)](https://img.shields.io/pypi/pyversions/sharpshooter.svg?style=flat)
[![Python package](https://github.com/byteface/sharpshooter/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/byteface/sharpshooter/actions/workflows/python-package.yml)

Shorthand templates for creating (or destroying) file-systems.

tree could be written for any language.

<p align="center"><img src="https://github.com/byteface/sharpshooter/raw/master/tty.gif?raw=true"/></p>

## install

```bash
python3 -m pip install sharpshooter --upgrade  # for just sharpshooter
python3 -m pip install sharpshooter[jinja2]  # sharpshooter with jinja2 cli extension
```

## CLI quick start

```bash
cd /path/to/some/folder
sharpshooter -c hello
# now open and edit the created hello.tree file in any text editor of your choice
# i.e sudo vim hello.tree
sharpshooter -t hello.tree  # run -t to test
sharpshooter -f hello.tree  # or -f to create folders/files specified hello.tree
sharpshooter --mock  # creates a sharpshooter.tree file of the current working directory
```

## intro

To create a plain empty file just type a word i.e.

```
file
```

to create or access a dir use a slash /

```
/dir
```

To create a file inside a dir use a 4 spaces (or tab)

```
/dir
    file
```

putting it all together…

```
/dir
    file
    /plugins
    /mail
        /vendor
        index.html
            /something # this one will fail
        file.py
        file.py
```

### / (slash) Creating a tree

```python
from sharpshooter import tree

tree('''
/dir
    file
    /plugins
        /mail
            /vendor
            index.html
            file.py
        file2.py
''')
```

tree doesn't wait to be told. Your files are now there.

### - (minus) deleting a tree

tree can also remove dirs and files. You guessed it. With the the - minus symbol

```python
tree = '''
/dir
    /plugins
         -mail
'''
```

tree will not ask twice. Your files are gone.

But be mindful this example would also 'create' the dir and plugins folders if they didn't exist. Because tree by nature creates by default.

To read info about a file or folder without creation use colon ':' to indicate read-only.

```python
tree = '''
:/dir
    :/plugins
        -mail
'''
```

More on colons : later.

###### WARNING - be careful using minus. tree could destroy your entire filesytem if used incorrectly

### \# (hash) comments

Use # to comment out a line or instruction.

```python
s = '''
/:dir
    file# some ignored text here
    /plugins
        /mail
'''
```

###### WARNING - the # symbol is ignored if it comes after the <, $ or > symbols. (see why further down)

### : (colon) read only

To read info about a file or folder, without creating any, use a colon ':'

You can then format the tree with an f-string to get the result which produces similir output as 'ls -al' on nix systems i.e.

```python
test = tree('''
:README.md
''')
print(f"{test}")
# -rw-r--r-- byteface staff 2100 21 Sep 07:58 README.md
```

or for a directory...

```python
test = tree('''
:venv
''')
print(f"{test}")
# drwxr-xr-x byteface staff 192 Mon Sep 20 10:18:44 2021 venv
```

Notice the little 'd' at the front lets you know it's a directory. Just like in a terminal.

you can safely change change order of colon and plus i.e. will still work.

```python
tree('''
:/dont
    :/make
        :this
''')
```

but i prefer to use the colon right before the file or folder name .i.e.

```python
tree('''
/:dont
    /:make
        :this
''')
```

up to you.

### test mode

If you are feeling unsure. Try tree in test mode.

It will log what it would do to the console but won't actually create any files or folders.

You just have to past test=True to the tree function. i.e

```python
mytree = '''
/somedir
    /anotherdir
        someotherfile.png
    file.txt
    file2.gif
'''

tree(mytree, test=True)  # notice how we set test=True

```

Now check the console and if you feel confident set test=False and run the code again.

### ~ (tilde) users home direcory

users home path is supported.

```python
s1 = """
:/~
    test.png
    /somedir
        somescript.py
"""
tree(s1, test=True)
tree(s1, test=False)
```

### < (lt) write to a file

< This symbol can be used to write a string to a file.

```python
mystring = """
/somedir
    somescript.py < print('hello world!')
    some.txt < hello world!
    script.sh < echo 'hello world'
"""
tree(mystring)
```

you can use \n to add more than one line to a file.

```python
mystring = """
/somedir
    somepage.md < # heading \n## another heading \n### and another heading
"""
tree(mystring)
```

###### WARNING - the comment # symbols are ignored after the < so they can be succesfully written to files. (i.e. .md files)

### $ (dollar) pass to the shell

Anything after the $ symbol is passed to the shell and the result is written to the file.

```python
mystring = """
/somedir
    test.txt $ cowsay moo
"""
tree(mystring)
```

###### WARNING - comments # symbol is ignored after the $ so don't use comments on these lines or they could be sent to the terminal

### > (gt) pass to windows cmd

bash commands won't work on windows. Instead use the > symbol for windows commands

Anything after the > symbol is passed to cmd with the result written to the file.

```python
mystring = """
/somedir
    test.txt $ ls -al
    test.txt > dir
"""
tree(mystring)
```

###### WARNING - comments # symbol is ignored after the > so don't use comments on these lines or they could be sent to cmd


### ? (question)

A question will take user input. It can be used in place of a filename.

```python
mystring = """
/somedir
    somefile.txt
    ?
    anotherfile.txt ?
    /?
        info.txt
"""
tree(mystring)
```

In this example a prompt would ask for a filename inbetween creating somefile.txt and anotherfile.txt.

Then a multi-line prompt would ask for content to be input for anotherfile.txt.

Lastly a prompt would ask for the folder name to be created before putting info.txt in it.

###### WARNING - comments # symbol is ignored after the > so don't use comments on these lines or they could be sent to cmd


### \#[name] labels

A label is a way to store multiple trees in a single file.

By using square brackets after a # symbol you can label a tree. i.e.

```
#[mylabel]
/dir
    file
```

You can now pass the label to the tree function.

```bash
sharpshooter --test myconfig.tree -l mylabel  # use --label to only parse part of a .tree file
```

## Anything else?

- you can now have spaces in filenames.

- tips: use with a proxy server and range requests to write partials to files.

To see planned features/goals see TODO.md

## CLI

There's several commands you can pass to sharpshooter on the command line.

```bash
python3 -m sharpshooter --help  # shows available commands. also uses -h
```

```bash
sharpshooter --version  # shows the current version. also uses -v
```

```bash
sharpshooter --create someconfigname  # creates a helloworld.tree file. also uses -c
```

```bash
sharpshooter --file myconfig.tree  # parses a .tree file and executes it. also uses -f
```

```bash
sharpshooter --test anotherconfig.tree  # parses a .tree file in test mode. also uses -t
```

```bash
sharpshooter --mock  # makes a sharpshooter.tree file based on the current working directory. also uses -m
# sharpshooter --mock 1  # pass optional depth as int
```

```bash
sharpshooter --dir  # set the current working directory. use with other commands. also uses -d
#i.e. python -m sharpshooter -d tests -f test.tree
```

```bash
sharpshooter --pretty 0 # prints a pretty tree of the cwd. also uses -p

# i.e
# ├── refs
# │   ├── heads
# │   │   ├── question
# │   │   ├── master
# │   │   └── anytree
# │   ├── tags
# │   └── remotes
# │       └── origin
# │           └── master

# takes optional parameter for depth : int

```

There's an optional feature that requires jinja2:

```bash
python -m pip install jinja2  # make sure you have jinja2 installed
sharpshooter --jinja myconfig.tree arg1=test # parses a .tree but runs through jinja first. also uses -j
```

- (note. jinja2 is not part of sharpshooter so you need to install it yourself. its an optional CLI dependency)
- (note. jinja2 has no test mode yet so be careful)


## NOTES

I came up with the idea while mucking around with a lexer.

https://www.dabeaz.com/ply/

https://github.com/dabeaz/ply

remember it executes from where your python thinks is the current dir.
If you're unsure set it first. i.e.

```bash
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
```

For your information, tree is the language and sharpshooter is an implementation.

pretty is available on the tree class as a static method.

```
from sharpshooter import tree
tree.pretty(tree_string)
```

## Contributing

If you think you can write a sharpshooter parser in another language then please do and i'll link to your repo.

To dev on this one locally just pull the repo and do...

```bash
cd /sharpshooter
python3 -m venv venv
. venv/bin/activate  # lnux, # windows: venv\Scripts\activate 
pip install -r requirements.txt 
python -m sharpshooter -d tests -f test.tree  # to use code version without installing
make test  # to run tests
```

Or run and write some tests, there's a few to get started in the Makefile.

You can install your own version using...

```bash
python3 -m pip install -e .
```

There's several test.tree files in the /tests you can tweak and run through the CLI.

It creates a tmp folder you can delete and rerun to experiment. i.e.

```
/tmp
    /hello
        world.txt < y tho!
        page.html < <html>y tho!</html>
    /this # some comment
        /is
            cool.txt $ cowsay cool
            cool.txt > dir
            test.md < # heading \n## another heading \n### and another heading
    page.html $ curl -s https://www.google.com
    page2.htm $ curl -s https://www.fileformat.info/info/charset/UTF-32/list.htm
    /partial
        star.html $ curl -s -r 32-35 https://raw.githubusercontent.com/byteface/domonic/master/docs/_templates/sidebarintro.html
    files.txt $ find .
```

## DISCLAIMER / known bugs

Use 4 spaces not tabs.

This is a work in progress. It creates and destroys files on your hard drive. So be careful.

DON'T leave trailing negative space on lines. I use space to change dirs.

comments won't work on lines with bash/windows commands or when writing to file. this is so you can write # symbols to the file.

filenames with special chars #?><$ at start or end may cause issues until escaping them is sorted.
