from sharpshooter import tree

s1 = """
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

tree(s1, test=True)