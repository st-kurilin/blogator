def md_read(inp):
    import markdown
    md_converter = markdown.Markdown(extensions=['meta'])
    content = md_converter.convert(inp)
    return {
        'meta' : md_converter.Meta.copy(),
        'content' : content
    }

def md_meta_get(meta, key, alt=None, single_value=True):
    if key in meta:
        if single_value:
            if meta[key]:
                return meta[key][0]
        else:
            return meta[key]
    return alt

def write_templated(template_path, out_path, data):
    import pystache
    outs = out_path.open('w')
    template = pystache.parse(template_path.open('r').read())
    renderer = pystache.Renderer()
    outs.write(renderer.render(template, data))

def read_blog_meta(blog_file_path):
    with blog_file_path.open() as fin:
        meta = md_read(fin.read())['meta']
        favicon_file = md_meta_get(meta, 'favicon-file')
        favicon_url = md_meta_get(meta, 'favicon-url',
                                  "favicon.cc/favicon/169/1/favicon.png")
        return {
            'title'        : md_meta_get(meta, 'title', 'Blog'),
            'annotation'   : md_meta_get(meta, 'annotation',
                                         'Blogging for living'),
            'favicon-file' : favicon_file,
            'favicon'      : 'favicon.ico' if favicon_file else favicon_url,
            'posts'        : [blog_file_path.parent / ref for ref in
                              md_meta_get(meta, 'posts', [], False)],
            'meta'         : meta,
            'tracking_code': md_meta_get(meta, 'ganalitics'),
        }

def read_post(post_file_path):
    import datetime
    with post_file_path.open() as fin:
        row_post = md_read(fin.read())
        post = {}
        post['meta'] = meta = row_post['meta']
        post['content'] = row_post['content']
        post['title'] = md_meta_get(meta, 'title',
                                    post_file_path.with_suffix("._").name)
        post['brief'] = md_meta_get(meta, 'brief')
        post['short_title'] = md_meta_get(meta, 'short_title',
                                          post['title'])
        post['link_base'] = md_meta_get(meta, 'link',
                                        post_file_path.with_suffix(".html").name)
        post['link'] = './' + post['link_base']
        published_str = md_meta_get(row_post['meta'], 'published')
        if published_str:
            published = datetime.datetime.strptime(published_str, '%Y-%m-%d')
            post['published'] = published.strftime('%d %b %Y')
        return post

def prepare_favicon(blog, target_dir):
    import shutil
    if blog['favicon-file'] is not None:
        orig_path = args.blog.parent / blog['favicon-file']
        destination_path = target_dir / 'favicon.ico'
        shutil.copyfile(orig_path.as_posix(), destination_path.as_posix())

def clean_target(target):
    import os
    import glob
    tpath = target.as_posix()
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    for file in glob.glob(tpath + '/*'):
        os.remove(file)

def generate(blog, p_args):
    def marked_active_post(orig_posts, active_index):
        active_post = orig_posts[active_index]
        posts_view = orig_posts.copy()
        active_post = orig_posts[active_index].copy()
        active_post['active?'] = True
        posts_view[active_index] = active_post
        return posts_view

    prepare_favicon(blog, p_args.target)

    posts = [read_post(_) for _ in blog['posts']]
    for active_index, post in enumerate(posts):
        posts_view = marked_active_post(posts, active_index)
        write_templated(p_args.templates / "post.template.html",
                        p_args.target / post['link_base'],
                        {'blog': blog, 'posts': posts_view, 'post': post})

    write_templated(p_args.templates / "index.template.html",
                    p_args.target / "index.html",
                    {'blog' : blog, 'posts': posts})

if __name__ == "__main__":
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

    args = parser.parse_args()
    blog_meta = read_blog_meta(args.blog)
    clean_target(args.target)
    generate(blog_meta, args)







