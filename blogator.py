"""Static blogs generator.
   See https://github.com/st-kurilin/blogator for details.
"""

def md_read(inp):
    """Reads markdown formatted message."""
    import markdown
    md_converter = markdown.Markdown(extensions=['meta'])
    content = md_converter.convert(inp)
    return {
        'meta' : md_converter.Meta.copy(),
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

def write_templated(template_path, out_path, data):
    """Generate templated content to file."""
    import pystache
    outs = out_path.open('w')
    template = pystache.parse(template_path.open('r').read())
    renderer = pystache.Renderer()
    outs.write(renderer.render(template, data))

def read_blog_meta(blog_file_path):
    """Reads general blog info from file."""
    from functools import partial
    with blog_file_path.open() as fin:
        meta = md_read(fin.read())['meta']
        get = partial(md_meta_get, meta)
        favicon_file = get('favicon-file')
        favicon_url = get('favicon-url', "favicon.cc/favicon/169/1/favicon.png")
        return {
            'meta'         : meta,
            'title'        : get('title', 'Blog'),
            'annotation'   : get('annotation', 'Blogging for living'),
            'favicon-file' : favicon_file,
            'favicon'      : 'favicon.ico' if favicon_file else favicon_url,
            'posts'        : [blog_file_path.parent / ref for ref in
                              get('posts', [], False)],
            'tracking_code': md_meta_get(meta, 'ganalitics'),
            'home-dir'     : blog_file_path.parent
        }

def read_post(post_file_path):
    """Reads post info from file."""
    import datetime
    from functools import partial

    def reformat_date(inpf, outf, date):
        """Reformats dates from one specified format to other one."""
        if date is None:
            return None
        return datetime.datetime.strptime(date, inpf).strftime(outf)

    with post_file_path.open() as fin:
        row_post = md_read(fin.read())
        post = {}
        post['meta'] = meta = row_post['meta']
        get = partial(md_meta_get, meta)
        post['content'] = row_post['content']
        post['title'] = get('title', post_file_path.with_suffix("._").name)
        post['brief'] = get('brief')
        post['short_title'] = get('short_title', post['title'])
        post['link_base'] = get('link',
                                post_file_path.with_suffix(".html").name)
        post['link'] = './' + post['link_base']
        post['published'] = reformat_date('%Y-%m-%d', '%d %b %Y',
                                          get('published'))
        return post

def prepare_favicon(blog, target):
    """Puts favicon file in right place with right name."""
    import shutil
    if blog['favicon-file'] is not None:
        orig_path = blog['home-dir'] / blog['favicon-file']
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

def generate(blog, templates, target):
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

    prepare_favicon(blog, target)

    posts = [read_post(_) for _ in blog['posts']]
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
    generate(read_blog_meta(ARGS.blog), ARGS.templates, ARGS.target)







