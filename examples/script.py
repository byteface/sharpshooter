from sharpshooter import tree

s1 = """
+tmp
    +hello
        world.txt < y tho!
        page.html < <html>y tho!</html>
    +this # some comment
        +is
            cool.txt $ cowsay cool
            cool.txt > dir
            test.md < # heading \n## another heading \n### and another heading
    page.html $ curl -s https://www.google.com
    page2.htm $ curl -s https://www.fileformat.info/info/charset/UTF-32/list.htm
    +partial
        star.html $ curl -s -r 32-35 https://raw.githubusercontent.com/byteface/domonic/master/docs/_templates/sidebarintro.html
    files.txt $ find .
"""

tree(s1, test=True)