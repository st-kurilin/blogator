"""Static blogs generator.
See https://github.com/st-kurilin/blogator for details.

Unit tests.
"""
import blogator as b
import unittest
from pathlib import Path

# pylint: disable=R0904
class TestIO(unittest.TestCase):
    """Test operations related to file system"""
    def setUp(self):
        b.fill_vitual_fs()

    def test_read(self):
        """Test read from file"""
        import tempfile
        with tempfile.NamedTemporaryFile() as temp:
            content = 'Some data'
            temp.write(content.encode('utf-8'))
            temp.flush()
            self.assertEqual(content, b.read(Path(temp.name)))

    def test_write_read(self):
        """Test read from file and write to file"""
        import tempfile
        with tempfile.NamedTemporaryFile() as temp:
            content = 'Some data'
            b.write(Path(temp.name), content)
            self.assertEqual(content, b.read(Path(temp.name)))

    def test_copy(self):
        """Test copy file"""
        import tempfile
        import os.path
        from random import randint
        temp_dir = Path(tempfile.gettempdir())
        rand = str(randint(0, 1000))
        from_dir = temp_dir / ('from_dir' + rand)
        from_file = from_dir / ('from_file' + rand)
        to_dir = temp_dir / ('to_dir' + rand)
        to_file = to_dir / ('to_file' + rand)
        os.mkdir(from_dir.as_posix())
        os.mkdir(to_dir.as_posix())
        content = "Hi " + rand

        b.write(from_file, content)
        b.copy(from_file, to_file)

        self.assertEqual(content, b.read(to_file))



    def test_has_default_post_template(self):
        """Should be in virtual fs"""
        path = Path('blogtor-virtual') / 'templates' / 'post.template.html'
        content = b.read(path)
        self.assertIsNotNone(content)

    def test_has_default_index_template(self):
        """Should be in virtual fs"""
        path = Path('blogtor-virtual') / 'templates' / 'index.template.html'
        content = b.read(path)
        self.assertIsNotNone(content)


def parse_templates(templates_arg):
    """Generic method that can be used to create other tests"""
    parser = b.create_parser()
    args = parser.parse_args(['myblog', '-templates', templates_arg])
    return args.templates

# pylint: disable=R0904
class TestArgumentParser(unittest.TestCase):
    """Test comand line argumens parsing"""

    def test_blog_value_parsing(self):
        """Argument parser should evaluate argument as blog"""
        args = b.create_parser().parse_args(['myblog'])
        self.assertEqual(Path('myblog'), args.blog)

    def test_help_could_be_called(self):
        """Argument parser should print help message and terminate program"""
        with self.assertRaises(SystemExit) as catched:
            b.create_parser().parse_args(['-h'])
        self.assertEqual(catched.exception.code, 0)

    def test_templates_arg_default(self):
        """Templates arg has default value."""
        args = b.create_parser().parse_args(['myblog'])
        self.assertEqual(Path('blogtor-virtual') / 'templates', args.templates)

    def test_templates_arg_simple(self):
        """Templates arg could be other than default value"""
        self.assertEqual(Path('foo'), parse_templates('foo'))

    def test_templates_arg_complex(self):
        """Templates arg could be other than default value"""
        self.assertEqual(Path('foo') / 'bar', parse_templates('foo/bar'))

    # def test_templates_args_can_have_slash_at_the_end(self):
    def test_template_arg_with_slash(self):
        """Templates arg should ignore slash at the end"""
        self.assertEqual(Path('foo') / 'bar', parse_templates('foo/bar/'))




# pylint: disable=R0904
class TestBlogator(unittest.TestCase):
    """Tests with isolated IO"""

    def setUp(self):
        def memory_read(path):
            """read from memory variable instead of file system"""
            if path in memory:
                return memory[path]
            raise IOError("Could not find " + path.as_posix() +
                          " in " + str(memory.keys()))

        def memory_write(path, data):
            """write to memory variable instead of file system"""
            memory[path] = data
        memory = dict()
        self._bread = b.read
        self._bwrite = b.write
        self._read = b.read = memory_read
        self._write = b.write = memory_write

    def tearDown(self):
        b.read = self._bread
        b.write = self._bwrite

    def test_simplest_happy_path(self):
        """Go throw full execution
           except working with IO (arguments parsing, file system)
        """
        templates = Path("mytemplates")
        out = Path("myout")
        blog = Path("myblog")

        self._write(templates / "index.template.html",
                    "{{{blog.title}}}:{{#posts}}{{{title}}}{{/posts}}")
        self._write(templates / "post.template.html",
                    "{{{post.title}}}--{{{post.content}}}")

        self._write(blog,
                    "title:    birds\nposts:    pheasants.md")
        self._write(Path("pheasants.md"),
                    "title: pheasant\nit's all about pheasants")

        b.generate(blog, templates, out)

        self.assertEqual("birds:pheasant",
                         self._read(Path(out / "index.html")))
        self.assertEqual("pheasant--<p>it's all about pheasants</p>",
                         self._read(out / "pheasants.html"))



if __name__ == '__main__':
    unittest.main()
