#tree (sharpshooter)

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
