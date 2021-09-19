#tree (sharpshooter)

#WARNING - probs don't use this until about 0.0.5... just setting up and adding poc

Shorthand templates for creating (or destroying) file-systems.

tree could be written for any language.

```
pip install sharpshooter
```

##syntax

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

##usage

```
from sharpshooter import tree

tree('''
+dir
    file < some text
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


for future feature goals see TODO.md


NOTES:

came up with the idea while mucking around with a lexer. 

https://www.dabeaz.com/ply/

https://github.com/dabeaz/ply

so am using this to do it.


- remember it executes from where your python thinks is the current dir
- if you're unsure set it first. i.e.

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))