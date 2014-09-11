import blogator as b
import random
import unittest
from pathlib import Path

class TestBlogator(unittest.TestCase):

    def setUp(self):
        pass

    def test_blog_value_parsing(self):
    	args = b.create_parser().parse_args(['myblog'])
    	self.assertEqual(Path('myblog'), args.blog)

    def test_help_could_be_called(self):
    	with self.assertRaises(SystemExit) as cm:
    		b.create_parser().parse_args(['-h'])
    	self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
