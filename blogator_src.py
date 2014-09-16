#
#Static blogs generator.
#See https://github.com/st-kurilin/blogator for details.
#
#Main script. Used to build final script using build.py script.
#

###Files operations
#separated to make testing easier

"""Default values for some files.
   Used to distribute script as a single file.
   Actual values filled by build.py script."""
PREDEFINED = dict()

def read(path):
    """Reads file content from FS"""
    if path in PREDEFINED:
        return PREDEFINED[path]
    with open(path.as_posix()) as file:
        return file.read()

def write(path, content):
    """Writes file content to FS"""
    with open(path.as_posix(), 'w') as file:
        file.write(content)

def copy(from_p, to_p):
    """Copies file content"""
    import shutil
    shutil.copyfile(from_p.as_posix(), to_p.as_posix())

def file_exist(path):
    """Check if file exist for specified path"""
    return path.is_file()


###Markdown template engine operations
def md_read(inp):
    """Reads markdown formatted message."""
    import markdown
    md_converter = markdown.Markdown(extensions=['meta'])
    content = md_converter.convert(inp)
    meta = getattr(md_converter, 'Meta', [])
    return {
        'meta' : meta,
        'content' : content
    }

def md_meta_get(meta, key, alt=None, single_value=True):
    """Reads value from markdown read message meta."""
    if key in meta:
        if single_value:
            if meta[key]:
                return meta[key][0]
        else:
            return meta[key]
    return alt


###Pystache template engine operations
def pystached(template, data):
    """Applies data to pystache template"""
    import pystache
    pys_template = pystache.parse(template)
    pys_renderer = pystache.Renderer()
    return pys_renderer.render(pys_template, data)


###Meta files readers operations
def parse_blog_meta(blog_meta_content):
    """Reads general blog info from file."""
    from functools import partial
    meta = md_read(blog_meta_content)['meta']
    get = partial(md_meta_get, meta)
    favicon_file = get('favicon-file')
    favicon_url = get('favicon-url', 'favicon.cc/favicon/169/1/favicon.png')
    return {
        'meta'         : meta,
        'title'        : get('title', 'Blog'),
        'annotation'   : get('annotation', 'Blogging for living'),
        'favicon-file' : favicon_file,
        'favicon'      : 'favicon.ico' if favicon_file else favicon_url,
        'posts'        : get('posts', [], False),
        'disqus'       : get('disqus'),
        'ganalitics'   : get('ganalitics'),
    }

def parse_post(post_blob, post_blob_orig_name):
    """Reads post info from file."""
    import datetime
    from functools import partial

    def reformat_date(inpf, outf, date):
        """Reformats dates from one specified format to other one."""
        if date is None:
            return None
        return datetime.datetime.strptime(date, inpf).strftime(outf)

    row_post = md_read(post_blob)
    post = {}
    post['meta'] = meta = row_post['meta']
    get = partial(md_meta_get, meta)
    post['content'] = row_post['content']
    post['title'] = get('title', post_blob_orig_name)
    post['brief'] = get('brief')
    post['short_title'] = get('short_title', post['title'])
    post['link_base'] = get('link', post_blob_orig_name + ".html")
    post['link'] = './' + post['link_base']
    post['published'] = reformat_date('%Y-%m-%d', '%d %b %Y',
                                      get('published'))
    return post


###Flow operations
def clean_target(target):
    """Cleans target directory. Hidden files will not be deleted."""
    import os
    import glob
    tpath = target.as_posix()
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    for file in glob.glob(tpath + '/*'):
        os.remove(file)

def generate(blog_path, templates, target):
    """Generates blog content. Target directory expected to be empty."""

    def prepare_favicon(blog, blog_home_dir, target):
        """Puts favicon file in right place with right name."""
        if blog['favicon-file'] is not None:
            orig_path = blog_home_dir / blog['favicon-file']
            destination_path = target / 'favicon.ico'
            copy(orig_path, destination_path)

    def marked_active_post(orig_posts, active_index):
        """Returns copy of original posts
        with specified post marked as active"""
        active_post = orig_posts[active_index]
        posts_view = orig_posts.copy()
        active_post = orig_posts[active_index].copy()
        active_post['active?'] = True
        posts_view[active_index] = active_post
        return posts_view

    def write_templated(template_path, out_path, data):
        """Generate templated content to file."""
        write(out_path, pystached(read(template_path), data))

    def fname(file_name):
        """file name without extension"""
        from pathlib import Path
        as_path = Path(file_name)
        name = as_path.name
        suffix = as_path.suffix
        return name.rsplit(suffix, 1)[0]

    def read_post(declared_path, work_dir):
        """Find location of post and read it"""
        from pathlib import Path
        candidates = [work_dir / declared_path, Path(declared_path)]
        for candidate in candidates:
            if file_exist(candidate):
                return read(candidate)
        raise NameError("Tried find post file by [{}] but didn't find anything"
                        .format(', '.join([_.as_posix() for _ in candidates])))

    blog = parse_blog_meta(read(blog_path))
    work_dir = blog_path.parent
    prepare_favicon(blog, work_dir, target)
    posts = [parse_post(read_post(_, work_dir), fname(_))
             for _ in blog['posts']]
    for active_index, post in enumerate(posts):
        posts_view = marked_active_post(posts, active_index)
        write_templated(templates / "post.template.html",
                        target / post['link_base'],
                        {'blog': blog, 'posts': posts_view, 'post': post})

    write_templated(templates / "index.template.html",
                    target / "index.html",
                    {'blog' : blog, 'posts': posts})


###Utils
def create_parser():
    """Parser factory method."""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='''Generates static blog
                                                  content from markdown posts.
                                                 ''')
    parser.add_argument('blog',
                        type=Path,
                        help='File with general information about blog',
                        default='blog')
    parser.add_argument('-target',
                        type=Path,
                        help='generated content destination',
                        default='target')
    parser.add_argument('-templates',
                        type=Path,
                        help='directory with templates',
                        default='blogtor-virtual/templates')
    return parser


def main():
    """Start endpoint"""
    args = create_parser().parse_args()
    clean_target(args.target)
    generate(args.blog, args.templates, args.target)

