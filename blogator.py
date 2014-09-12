"""Static blogs generator.
   See https://github.com/st-kurilin/blogator for details.
"""

def read(path):
    """Reads file content from FS"""
    with open(path.as_posix(), 'r') as file:
        return file.read()

def write(path, content):
    """Writes file content to FS"""
    with open(path.as_posix(), 'w') as file:
        file.write(content)

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

def pystached(template, data):
    """Applies data to pystache template"""
    import pystache
    pys_template = pystache.parse(template)
    pys_renderer = pystache.Renderer()
    return pys_renderer.render(pys_template, data)

def parse_blog_meta(blog_meta_content):
    """Reads general blog info from file."""
    from functools import partial
    meta = md_read(blog_meta_content)['meta']
    get = partial(md_meta_get, meta)
    favicon_file = get('favicon-file')
    favicon_url = get('favicon-url', "favicon.cc/favicon/169/1/favicon.png")
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

def prepare_favicon(blog, blog_home_dir, target):
    """Puts favicon file in right place with right name."""
    import shutil
    if blog['favicon-file'] is not None:
        orig_path = blog_home_dir / blog['favicon-file']
        destination_path = target / 'favicon.ico'
        shutil.copyfile(orig_path.as_posix(), destination_path.as_posix())

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
        """file name without suffix. TODO: handle complex paths"""
        return file_name.split(".")[0]

    blog = parse_blog_meta(read(blog_path))

    prepare_favicon(blog, blog_path.parent, target)
    posts = [parse_post(read(blog_path.parent / _), fname(_))
             for _ in blog['posts']]
    for active_index, post in enumerate(posts):
        posts_view = marked_active_post(posts, active_index)
        write_templated(templates / "post.template.html",
                        target / post['link_base'],
                        {'blog': blog, 'posts': posts_view, 'post': post})

    write_templated(templates / "index.template.html",
                    target / "index.html",
                    {'blog' : blog, 'posts': posts})

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
                        default='templates')
    return parser

if __name__ == "__main__":
    ARGS = create_parser().parse_args()
    clean_target(ARGS.target)
    generate(ARGS.blog, ARGS.templates, ARGS.target)
