## tree (sharpshooter)

Shorthand templates for creating (or destroying) file-systems.

tree could be written for any language.

```
pip install sharpshooter
```

## syntax

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

## usage

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
		  file.py
''')
```

tree doesn't wait to be told. Your files are now there.

## deleting a file

tree can also remove dirs and files. You guessed it. With the the - minus symbol

```
tree = ''' \
+dir
    +plugins
         -mail
'''
```

But be mindful that would also create the dir and plugins dir if they didn't exist.

tree will not ask twice. Your files are gone.

## comments

use # to comment out a line or instruction.
(warning. bug. DON'T leave a space before the comment. Lexer may interpret it as directory change)

```
s = '''
+:dir
    file# some ignored text here
    +plugins
        +mail
'''
```

To see planned features/goals see TODO.md

## CLI

You can use the CLI to read the version i.e.

```
$ python3 -m tree --version
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

## DISCLAIMER

This is a work in progress. It creates and destroys files on your hard drive. So be careful.

DON'T leave trailing negative space on lines. I use space to change dirs.

Use 4 spaces not tabs. (I've not tested with tabs as my editor converts them to 4 spaces). will sort later.

if using a comment. Don't leave space before the #
