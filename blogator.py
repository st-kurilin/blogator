"""
Static blogs generator.

This file was generated. Do not edit it directly.
See https://github.com/st-kurilin/blogator for details.

"""
#__ignore comment bellow__#
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
PREDEFINED = {}

def read(path):
    """Reads file content from FS"""
    if path in PREDEFINED:
        return PREDEFINED[path]
    with open(str(path)) as file:
        return file.read()

def write(path, content):
    """Writes file content to FS"""
    with open(str(path), 'w') as file:
        file.write(content)

def copy(from_p, to_p):
    """Copies file content"""
    import shutil
    shutil.copyfile(str(from_p), str(to_p))

def is_file_exist(path):
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
        if single_value and meta[key]:
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
        'ganalytics'   : get('ganalytics'),
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
    post['link'] = './' + get('link', post_blob_orig_name + ".html")
    post['published'] = reformat_date('%Y-%m-%d', '%d %b %Y',
                                      get('published'))
    return post


###Flow operations
def clean_target(target):
    """Cleans target directory. Hidden files will not be deleted."""
    import os
    import glob
    tpath = str(target)
    if not os.path.exists(tpath):
        os.makedirs(tpath)
    for file in glob.glob(tpath + '/*'):
        os.remove(file)

def generate(blog_path, templates, target):
    """Generates blog content. Target directory expected to be empty."""

    def prepare_favicon(blog, blog_home_dir, target):
        """Puts favicon file in right place with right name."""
        if blog['favicon-file']:
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

    def read_post(declared_path, work_dir):
        """Find location of post and read it"""
        from pathlib import Path
        candidates = [work_dir / declared_path, Path(declared_path)]
        for candidate in candidates:
            if is_file_exist(candidate):
                return read(candidate)
        raise NameError("Tried find post file by [{}] but didn't find anything"
                        .format(', '.join([str(_) for _ in candidates])))

    from pathlib import Path

    blog = parse_blog_meta(read(blog_path))
    work_dir = blog_path.parent
    prepare_favicon(blog, work_dir, target)
    posts = [parse_post(read_post(Path(_), work_dir), Path(_).stem)
             for _ in blog['posts']]
    for active_index, post in enumerate(posts):
        posts_view = marked_active_post(posts, active_index)
        write_templated(templates / "post.template.html",
                        target / post['link'],
                        {'blog': blog, 'posts': posts_view, 'post': post})

    write_templated(templates / "index.template.html",
                    target / "index.html",
                    {'blog' : blog, 'posts': posts})


###Utils
def parse_args(args):
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
    return parser.parse_args(args)


def main():
    """Start endpoint"""
    import sys
    args = parse_args(sys.argv[1:])
    clean_target(args.target)
    generate(args.blog, args.templates, args.target)

def fill_vitual_fs():
    """Fills virtual fs with default values"""
    from pathlib import Path
    PREDEFINED[Path('blogtor-virtual') / 'templates' / 'index.template.html'] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    {{#blog.favicon}}
    <link rel="icon" href="{{blog.favicon}}">
    {{/blog.favicon}}

    <title>{{blog.title}}</title>

    <!-- Bootstrap core CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="http://getbootstrap.com/ie10-viewport-bug-workaround.js"></script>

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <style type="text/css">
        .post-date {
            display: block;
            margin-top: -.5rem;
            margin-bottom: 1rem;
            color: #9a9a9a;
        }

        .post-brief {
          color: rgb(48, 48, 48);
        }

        .post-title a {
          color: rgb(48, 48, 48);
        }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="page-header">
        <h1>{{blog.title}}</h1>
        <p class="lead">{{blog.annotation}}</p>
      </div>

      <div class="row">
        <div class="col-md-2"> </div>
        <div class="col-md-7">
        	{{#posts}}
            <h3 class="post-title">
              <a href="{{link}}">{{title}}</a>
            </h3>
            {{#published}}
            <span class="post-date">{{published}}</span>
            {{/published}}
            {{#brief}}
              <a href="{{link}}">
                <span class="post-brief">{{{brief}}}</span> 
                <button type="button" class="btn btn-default btn-xs">
                  <span class="glyphicon glyphicon-chevron-right"></span>
                </button>
              </a> 
            {{/brief}}
            {{^brief}}
              {{{content}}}
            {{/brief}}
        	{{/posts}}
        </div>
        <div class="col-md-1">
        </div>
        <div class="col-md-2">
        </div>
      </div>
    </div> <!-- /container -->
    {{#blog.ganalytics}}
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', '{{blog.ganalytics}}', 'auto');
      ga('send', 'pageview');
    </script>
    {{/blog.ganalytics}}
  </body>
</html>
"""
    PREDEFINED[Path('blogtor-virtual') / 'templates' / 'post.template.html'] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    {{#blog.favicon}}
    <link rel="icon" href="{{blog.favicon}}">
    {{/blog.favicon}}

    <title>{{post.title}} - {{blog.title}}</title>

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
        .post-date {
            display: block;
            margin-top: -.5rem;
            margin-bottom: 1rem;
            color: #9a9a9a;
        }

        .blog-title a, .post-title a {
          color: rgb(48, 48, 48);
        }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="page-header">
        <h1 class="blog-title">
          <a href="index.html">{{blog.title}}</a>
        </h1>
        <p class="lead">{{blog.annotation}}</p>
      </div>
      <div class="row">
        <div class="col-md-2"> </div>
        <div class="col-md-7">
            <h3 class="post-title">{{post.title}}</h3>
            {{#post.published}}
            <span class="post-date">{{post.published}}</span>
            {{/post.published}}
            {{{post.content}}}

            {{#blog.disqus}}
            <div id="disqus_thread"></div>
            <script type="text/javascript">
                var disqus_shortname = document.location.hostname === ""  ? window.location.href : "{{blog.disqus}}"; 
                (function() {
                    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; 
                    dsq.async = true;
                    dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
                    dsq.id = 'disqus';
                    (document.getElementsByTagName('body')[0]).appendChild(dsq);
                })();
            </script>
            <noscript>Please enable JavaScript to view the comments.</a></noscript>
            {{/blog.disqus}}
        </div>
        <div class="col-md-3">
          <h3>&nbsp;</h3>
          <ul class="nav nav-pills nav-stacked">
            {{#posts}}
            {{#active?}}
              <li class="active"><a href="#">{{short_title}}</a></li>
            {{/active?}}
            {{^active?}}
              <li><a href="{{link}}">{{short_title}}</a></li>
            {{/active?}}
            {{/posts}}
          </ul>
        </div>
      </div>
    </div> <!-- /container -->
    {{#blog.ganalytics}}
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', '{{blog.ganalytics}}', 'auto');
      ga('send', 'pageview');
    </script>
    {{/blog.ganalytics}}
  </body>
</html>
"""
if __name__ == "__main__":
     fill_vitual_fs()
     main()
