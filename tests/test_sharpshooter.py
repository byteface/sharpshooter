# coding: utf8
"""
    test_sharpshooter
    ~~~~~~~~~~~~~~~
    unit tests for sharpshooter

"""

import os
import unittest
from unittest.mock import Mock

import pathlib as pl

# import requests
# from mock import patch
# from inspect import stack

from sharpshooter import tree


class TestCase(unittest.TestCase):

    def setUp(self):
        # change the root to the test directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def tearDown(self) -> None:
        # incase left from previous test or failed runs
        tree("-/dir", test=False)
        return super().tearDown()

    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError(f"File does not exist: {str(path)}")

    def assertIsDir(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError(f"Directory does not exist: {str(path)}")

    def test_tree(self):

#         s1 = """
# /:dir
#     /plugins
#         /mail
#             file3
#             /things
#                 /again
#                     file8
#                     file9.txt
#                 file7
#             /more
#                 file6
#         file4
#             file5# comments are not allowed spaces before them yet. causes wrong directory
#     file1# this is a file
# file2
#         """

# NOTE - should now handle being tabbed in.
        s1 = """
        /dir
            /plugins
                file8
                /:mail
                    file3
                    /things
                        /again
                            :file8
                            file9.txt
                        file7
                    /:more
                        file6
                file4
                    file5# comments are not allowed spaces before them yet. causes wrong directory
            file1# this is a file
        file2
        """
        tree(s1, test=False)

        path = pl.Path("dir")
        self.assertIsDir(path)

        # make sure plugins is inside dir
        path = pl.Path("dir/plugins")
        self.assertIsDir(path)

        # check if files exist
        expected = ['file4', 'file8']
        for f in expected:
            path = pl.Path("dir/plugins/%s" % f)
            self.assertIsFile(path)

        # clean up
        tree("-/dir", test=False)
        tree("-file2", test=False)

    def test_minus(self):
        # NOTE - should now handle being tabbed in.
        s1 = """
        /dir
            /plugins
                file4
                /mail
        """
        tree(s1, test=True)

        # assert we are in test mode
        self.assertFalse(os.path.isdir(os.path.join(os.getcwd(), 'dir')))

        tree(s1)
        assert os.path.isdir(os.path.join(os.getcwd(), 'dir', 'plugins'))
        assert os.path.isfile(os.path.join(os.getcwd(), 'dir', 'plugins', 'file4'))

        # delete a file
        s1 = """
        /dir
            /plugins
                -file4
        """
        tree(s1, test=False)
        # make sure file4 is gone
        self.assertFalse(os.path.isfile(os.path.join(os.getcwd(), 'dir', 'plugins', 'file4')))

        # delete a folder
        s1 = """
        /dir
            /plugins
                -mail  #removing this one
            /addoneaswell   #test comments with space now too
                test.png
        """
        tree(s1, test=True)

        # test hypthon folder
        s1 = """
        /newdir123
            /plug-ins_19
                _test-12-3.png
        """
        tree(s1, test=True)

    def test_colon(self):
        # we want the same info
        # -rw-r--r--@ 1 byteface  staff  2100 21 Sep 07:58 README.md
        # To read info about a file or folder without creation use colon :

        # TODO - cant do for files on same line?
        test = tree("""
:test_sharpshooter.py
""", test=True)
        print(f"{test}")
        assert 'test_sharpshooter.py' in f"{test}"

        test = tree(":venv")
        print(f"{test}")

        # test not creating things by using colon
        tree('''
        /:dont
            /:make
                :this
        ''')
        # self.assertFalse(os.path.isdir(os.path.join(os.getcwd(), 'venv', 'test')))

        # change order of colon and plus
        tree('''
        :/dont
            :/make
                :this
        ''')

    def test_testmode(self):
        # test mode true. things wont get created
        s1 = """
        /DONT
            /MAKE
                me.png
                /or
                    /this
                        /or
                            this.png
                            that.gif
            /WE
                /DONT
                    /make
                        things.png
                        /this
            /test
                /mode
                    /wont
                        /make
                            things.png
        """
        tree(s1, test=True)


    def test_testmode_not_delete(self):
        # same code as test mode. things will get created
        s1 = """
        /DONT
            /MAKE
                me.png
                /or
                    /this
                        /or
                            this.png
                            that.gif
            /WE
                /DONT
                    /make
                        things.png
                        /this
            /test
                /mode
                    /wont
                        /make
                            things.png
        """
        tree(s1, test=False)
        assert os.path.isdir(os.path.join(os.getcwd(), 'DONT', 'MAKE'))
        assert os.path.isdir(os.path.join(os.getcwd(), 'DONT', 'WE', 'DONT', 'make'))
        assert os.path.isdir(os.path.join(os.getcwd(), 'DONT', 'test', 'mode', 'wont', 'make'))

        # print('delete it')
        # aggressively delete the DON'T folder
        s2 = """
        -DONT
        """
        tree(s2, test=False)
        assert os.path.isdir(os.path.join(os.getcwd(), 'DONT')) is False

    def test_folders_with_spaces(self):
        # As much as I hate this. It's pefectly legal.
        s1 = """
        /MAKE THIS FOLDER
            and This file.png
        """
        tree(s1, test=False)
        assert os.path.isdir(os.path.join(os.getcwd(), 'MAKE THIS FOLDER'))
        assert os.path.isfile(os.path.join(os.getcwd(), 'MAKE THIS FOLDER', 'and This file.png'))

    def test_z(self):
        # clean up
        print('clean up')
        s1 = """
        -dir
        -file2
        -MAKE THIS FOLDER
        """
        tree(s1, test=False)

    # def test_chmod(self):
    #     s1 = """
    #     /MAKE THIS FOLDER
    #         and This file.png =644 # this will be tough/impossible? to parse. i.e that could literally be the full filename
    #     """
    #     os.chdir(os.path.dirname(os.path.abspath(__file__)))
    #     tree(s1, test=False)

    # def test_tilde(self):
    #     s1 = """
    #     :/~
    #         test.png
    #         /somedir
    #             somescript.py
    #     """
    #     tree(s1, test=True)
    #     tree(s1, test=False)

    # def test_paths(self):
    #     s1 = """
    #     :/var/www/html/
    #         test.png
    #         somedir/somescript.py
    #     """



if __name__ == '__main__':
    unittest.main()
