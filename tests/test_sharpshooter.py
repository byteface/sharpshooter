"""
    test_sharpshooter
    ~~~~~~~~~~~~~~~
    unit tests for sharpshooter

"""

import time
import unittest
from unittest.mock import Mock
# import requests
# from mock import patch
# from inspect import stack

from sharpshooter import tree


class TestCase(unittest.TestCase):


    def test_tree(self):

# TODO - bug. hmmmmm. fuck
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

        import os
        # change to project root
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        tree(s1, test=True)

        # TODO: test that files now exist

        # check if dir exists
        # self.assertTrue(os.path.isdir(os.path.join(os.getcwd(), 'plugins')))
        
        # check if files exist
        # self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), 'plugins', 'mail', 'file3')))


if __name__ == '__main__':
    unittest.main()
