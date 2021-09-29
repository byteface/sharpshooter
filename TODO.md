NOTE - non of this works. its all 'TODO'. 
Anything working will go over to readme.md once added as a feature. consider all of these tickets.

# - TODO - testmode . should also report if it would have failed/succeeded.
# - TODO - testmode . should also report on colons.

## quiet mode

- needs a mode that doesn't throw any warnings. (solvable with a logger)
- maybe also a verbose mode that produces a report in a file.


###read only - (more)

- tree should hold the file object for introspection to access files in a directory for example.

- directory output should probably also show contained files.



##permissions #TODO - this isn't done yet. planning. (may need a 2nd pass for perms)

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

So don't use a minus to 'see what will happen'. Make sure you know what is being removed.


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


## CLI

- various additions added as comments in the __main__.py file.
- ¥ needs to be pasted in terimnal . find an other shortcut symbol




## grep (much later)

- maybe do some shorthand searching?