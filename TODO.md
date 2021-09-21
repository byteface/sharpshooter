NOTE - non of this works. its all TODO. then if i get this working will go over to readme.md


###read only

To read info about a file or folder without creation use colon :

```
tree = ''' \
+:dir
    +:plugins
        :mail
'''
```

#TODO - return info about the file or dir


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

##careful

sharpshooter can destroy your file system.

```
s = '''
-:~
'''
```


TODO - To write a string to a file use <, >, <<, >>

```
+dir
    file < some text
    other text > file
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

