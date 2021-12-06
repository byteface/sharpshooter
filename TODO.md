# NOTE - non of this works. its all TODO/ideas

Anything working will go over to readme.md once added as a feature. consider all of these tickets.

### - TODO - testmode . should also report if it would have failed/succeeded.
### - TODO - testmode . should also report on colons.

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


TODO - colons for opening muli-line strings?
+hello
    cow.md:
        here you could write blocks of text
        over multiple lines.
        Form this tab point


TODO - << 2 chevrons to append to a file.


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

TODO - print the tree in a tree format (use anytree lib?)
```
Udo
├── Marc
│   └── Lian
└── Dan
    ├── Jet
    ├── Jan
    └── Joe
        └── dan.txt
```


# another optional way is it use f_ and d_ builder functions
# TODO - this aint dont yet
d_('somedir',
    f_('file1', chmod=755),
    d_('things', 'file2.txt', 'file3.txt')
)


# using forward slash or tilde to set root dir? not sure where that note went. might be a ticket.
(tilde already used for home)

```
/start/from/here

```


# over ssh ?
could tie in to the forward slash. or use a pipe?

```
| USERNAME@ADRESS:/var/www
$ zip -r site.zip /app/staging/site/
+backups
    (DATE).txt < taking a snapshot
$ mv site.zip backups/site.zip

```

# labels

some way of labelling trees. so you can have more than 1 in a single .tree file. 
and pass a lable via cmd to only run those lables.

maybe could exist on notation of a comment that gets parsed?

i.e #[somelabel]

then you could do
```
sharpshooter -f myproj.tree -l somelabel
```

# variables for cmd line defaults i.e.
--book="My Great Novel"
--author="My Great Novel"
--chapters=10


# detect jinja and warn
- if using jinja tags it needs to detect and warn if not plug or not running with -j flag


notes...

- various additions added as comments in the __main__.py file.
- ¥ needs to be pasted in terimnal . find an other shortcut symbol 🌳 \U0001F333
https://raw.githubusercontent.com/carpedm20/emoji/master/emoji/unicode_codes/data_dict.py
deciduous_tree

- grep (much later) - maybe do some shorthand searching?