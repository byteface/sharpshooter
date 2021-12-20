# NOTE - non of this works. its all TODO/ideas

Anything working will go over to readme.md once added as a feature. consider all of these tickets.

### - TODO - testmode . should also report if it would have failed/succeeded.
### - TODO - testmode . should also report on colons.

## quiet mode

- needs a mode that doesn't throw any warnings. (solvable with a logger)
- maybe also a verbose mode that produces a report in a file.


### read only - (more)

- tree should hold the file object for introspection to access files in a directory for example.

- directory output should probably also show contained files.



### permissions #TODO - this isn't done yet. planning. (may need a 2nd pass for perms)

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


## labels - changes name to 'branches' . also have them includable.

labels are a way of having multiple trees in a single .tree file.

They use comment for notation i.e #[somelabel]

this allows you to run only the trees with the label. i.e

```
sharpshooter -f myproj.tree -l somelabel
```




notes. test use mock to build a tree of a cwd. then use labels with ssh 




# variables for cmd line defaults i.e.
--book="My Great Novel"
--author="My Great Novel"
--chapters=10


# detect jinja and warn
- if using jinja tags it needs to detect and warn if not plug or not running with -j flag


# escaping or quoting for special chars

filenames with special chars #?><$ at start or end may cause issues until escaping them is sorted.
- use 'single quotes' for filenames with special chars?


# - outdir

the dir setting on CLI is good. but means the .tree file gets written to that dir.
may be good to also have an outdir setting.


notes...

- various additions added as comments in the __main__.py file.
- ¥ needs to be pasted in terimnal . find an other shortcut symbol 🌳 \U0001F333
https://raw.githubusercontent.com/carpedm20/emoji/master/emoji/unicode_codes/data_dict.py
deciduous_tree

- grep (much later) - maybe do some shorthand searching?