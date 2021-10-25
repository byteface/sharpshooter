# tree (sharpshooter)

[![PyPI version](https://badge.fury.io/py/sharpshooter.svg)](https://badge.fury.io/py/sharpshooter.svg) 
[![Downloads](https://pepy.tech/badge/sharpshooter)](https://pepy.tech/project/sharpshooter)
[![Python version](https://img.shields.io/pypi/pyversions/sharpshooter.svg?style=flat)](https://img.shields.io/pypi/pyversions/sharpshooter.svg?style=flat)
[![Python package](https://github.com/byteface/sharpshooter/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/byteface/sharpshooter/actions/workflows/python-package.yml)

Shorthand templates for creating (or destroying) file-systems.

tree could be written for any language.

```
pip install sharpshooter
```

## intro

To create a plain empty file just type a word i.e.

```
file
```

to create or access a dir use +

```
+dir
```

To create a file inside a dir use a 4 spaces (or tab)

```
+dir
    file
```

putting it all together…

```
+dir
    file
    +plugins
    +mail
        +vendor
        index.html
            +something
        file.py
        file.py
```

### Creating a tree

```
from sharpshooter import tree

tree('''
+dir
    file
    +plugins
        +mail
            +vendor
            index.html
                +something
            file.py
        file2.py
''')
```

tree doesn't wait to be told. Your files are now there.

### deleting a tree

tree can also remove dirs and files. You guessed it. With the the - minus symbol

```
tree = '''
+dir
    +plugins
         -mail
'''
```

tree will not ask twice. Your files are gone.

But be mindful this example would also 'create' the dir and plugins folders if they didn't exist. Because tree by nature creates by default.

To read info about a file or folder without creation use colon ':' to indicate read-only.

```
tree = '''
+:dir
    +:plugins
         -mail
'''
```

More on colons : later.

## comments

use # to comment out a line or instruction.
(warning. bug. DON'T leave a space before the comment. Lexer may interpret it as directory change. THIS should be fixed. add more tests before removing this warning.)

```
s = '''
+:dir
    file# some ignored text here
    +plugins
        +mail
'''
```

## read only

To read info about a file or folder, without creating any, use a colon ':'

You can then format the tree with an f-string to get the result which produces similir output as 'ls -al' on nix systems i.e.

```
test = tree('''
:README.md
''')
print(f"{test}")
# -rw-r--r-- byteface staff 2100 21 Sep 07:58 README.md
```

or for a directory...

```
test = tree('''
:venv
''')
print(f"{test}")
# drwxr-xr-x byteface staff 192 Mon Sep 20 10:18:44 2021 venv
```

Notice the little 'd' at the front lets you know it's a directory. Just like in a terminal.


you can safely change change order of colon and plus i.e. will still work.

```
tree('''
:+dont
    :+make
        :this
''')
```

but i prefer to use the colon right before the file or folder name .i.e.

```
tree('''
+:dont
    +:make
        :this
''')
```

up to you.


## test mode

If you are feeling unsure. Try tree in test mode.

It will log what it would do to the console but won't actually create any files or folders.

You just have to past test=True to the tree function. i.e

```
mytree = '''
+somedir
    +anotherdir
        someotherfile.png
    file.txt
    file2.gif
'''

tree(mytree, test=True)  # notice how we set test=True

```

Now you can check the console and if you feel confident set test=False and run the code again.

## tilde

users home path is supported. (* TODO - not yet tested on pc)

```
    s1 = """
    :+~
        test.png
        +somedir
            somescript.py
    """
    tree(s1, test=True)
    tree(s1, test=False)
```

## Anything else?

- you can now have spaces in filenames.

To see planned features/goals see TODO.md

## CLI

You can use the CLI to read the version i.e.

```
$ python3 -m sharpshooter --version
```

## NOTES

I came up with the idea while mucking around with a lexer. 

https://www.dabeaz.com/ply/

https://github.com/dabeaz/ply

remember it executes from where your python thinks is the current dir.
If you're unsure set it first. i.e.

```
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
```

## DISCLAIMER / known bugs

This is a work in progress. It creates and destroys files on your hard drive. So be careful.

DON'T leave trailing negative space on lines. I use space to change dirs.

Use 4 spaces not tabs. (I've not tested with tabs as my editor converts them to 4 spaces). will sort later.

When using a comment. Don't leave space before the # < note this one should be fixed.
