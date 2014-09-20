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
        import shutil
        from random import randint
        temp_dir = Path(tempfile.gettempdir())
        try:
            rand = str(randint(0, 1))
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
        finally:
            shutil.rmtree(from_dir.as_posix(), ignore_errors=True)
            shutil.rmtree(to_dir.as_posix(), ignore_errors=True)


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

        def memory_copy(from_p, to_p):
            """Copies virtual files"""
            memory[to_p] = memory[from_p]

        def memory_file_exist(path):
            """Check if content could be retrieved by specified path"""
            return path in memory

        memory = dict()
        self._orig_read = b.read
        self._orig_write = b.write
        self._orig_copy = b.copy
        self._orig_file_exist = b.file_exist

        b.read = memory_read
        b.write = memory_write
        b.copy = memory_copy
        b.file_exist = memory_file_exist

    def tearDown(self):
        b.read = self._orig_read
        b.write = self._orig_write
        b.copy = self._orig_copy
        b.file_exist = self._orig_file_exist

    def add_simple_templates(self, templates):
        """Common method to save simplest templates instead of default"""
        b.write(templates / "index.template.html",
                "{{{blog.title}}}:{{#posts}}{{{title}}}{{/posts}}")
        b.write(templates / "post.template.html",
                "{{{post.title}}}--{{{post.content}}}")

    def add_default_templates(self):
        b.fill_vitual_fs()
        [b.write(path, content) for path, content in b.PREDEFINED.items()]

    def test_simplest_happy_path(self):
        """Go throw full execution
           except working with IO (arguments parsing, file system)
        """
        templates = Path("mytemplates")
        out = Path("myout")
        blog = Path("myblog")

        self.add_simple_templates(templates)

        b.write(blog,
                "title:    birds\nposts:    pheasants.md")
        b.write(Path("pheasants.md"),
                "title: pheasant\nit's all about pheasants")

        b.generate(blog, templates, out)

        self.assertEqual("birds:pheasant",
                         b.read(out / "index.html"))
        self.assertEqual("pheasant--<p>it's all about pheasants</p>",
                         b.read(out / "pheasants.html"))

    def test_post_file_related(self):
        """paths to posts could be specified related to blog file"""
        templates = Path("mytemplates")
        out = Path("myout")
        blog = Path('someparent') / 'myblog'

        self.add_simple_templates(templates)

        b.write(blog,
                "title:    birds\nposts:    posts/pheasants.md")
        b.write(blog.parent / 'posts' / 'pheasants.md',
                "title: pheasant\nit's all about pheasants")
        b.generate(blog, templates, out)

        self.assert_not_empty_file_exist(out / 'pheasants.html')

    def test_post_file_absolute(self):
        """paths to posts could be specified with absolute paths"""
        templates = Path("mytemplates")
        out = Path('myout')
        blog = Path('someparent') / 'myblog'

        self.add_simple_templates(templates)

        b.write(blog,
                "title:    birds\nposts:    /abs/posts/pheasants.md")
        b.write(Path('/abs') / 'posts' / 'pheasants.md',
                "title: pheasant\nit's all about pheasants")
        b.generate(blog, templates, out)

        self.assert_not_empty_file_exist(out / 'pheasants.html')

    def test_favicon_file_copied(self):
        """favicon file should be copied to target"""
        templates = Path("mytemplates")
        out = Path('myout')
        blog = Path('myblog')

        self.add_simple_templates(templates)

        b.write(Path('/d/fav.png'), 'my favicon')
        b.write(blog,
                "title:    birds\nfavicon-file:    /d/fav.png")
        b.generate(blog, templates, out)

        self.assert_not_empty_file_exist(out / 'favicon.ico')

    def test_ganalytics_present(self):
        """Google Analytics should be added in the output html
        since blog file has ganalytics key-value"""
        templates = Path('blogtor-virtual') / 'templates'
        out = Path("myout")
        blog = Path("myblog")
        ganalytics = "UA-77777777-7"

        self.add_default_templates()

        b.write(blog,
                "title: birds\nposts:   pheasants.md\nganalytics:   " +
                ganalytics)
        b.write(Path("pheasants.md"),
                "title: pheasant\nit's all about pheasants")
        b.generate(blog, templates, out)

        self.assertTrue(self.is_google_analytics_presented((out / "index.html"),
                                                           ganalytics))
        self.assertTrue(self.is_google_analytics_presented((out / "pheasants.html"),
                                                           ganalytics))

    def test_ganalytics_absent(self):
        """Gooogle Analytics should not be added in the output html
        since blog file doesn't have ganalytics key-value"""
        templates = Path('blogtor-virtual') / 'templates'
        out = Path("myout")
        blog = Path("myblog")

        self.add_default_templates()

        b.write(blog,
                "title: birds\nposts:   pheasants.md\n")
        b.write(Path("pheasants.md"),
                "title: pheasant\nit's all about pheasants")
        b.generate(blog, templates, out)

        self.assertFalse(self.is_google_analytics_presented((out / "index.html"),
                                                            "UA-"))
        self.assertFalse(self.is_google_analytics_presented((out / "pheasants.html"),
                                                            "UA-"))

    def assert_not_empty_file_exist(self, path):
        self.assertTrue(b.file_exist(path))
        self.assertTrue(len(b.read(path)) > 0)

    def is_google_analytics_presented(self, path, ganalytics):
        content = b.read(path)
        return 'www.google-analytics.com/analytics.js' in content and \
               ganalytics in content


if __name__ == '__main__':
    unittest.main()
