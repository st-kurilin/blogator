
import sys

def md_read(inp):
	import markdown
	md = markdown.Markdown(extensions = ['meta'])
	content = md.convert(inp)
	return {
		'meta' : md.Meta.copy(),
		'content' : md.convert(inp)
	}

def md_meta_get(meta, key, alt = None, single_value = True):
	if key in meta:
		if single_value:
			if len(meta[key]) > 0:
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
	import markdown
	md = markdown.Markdown(extensions = ['meta'])
	with blog_file_path.open() as fin:
		content = md.convert(fin.read())
		meta = md.Meta.copy()
		favicon_file = md_meta_get(meta, 'favicon-file')
		return {
			'title' : md_meta_get(meta, 'title', 'Blog'),
			'annotation' : md_meta_get(meta, 'annotation', 'Blogging for living'),
			'favicon-file' : favicon_file ,
			'favicon': 'favicon.ico' if favicon_file is not None else md_meta_get(meta, 'favicon-url', "http://www.favicon.cc/favicon/169/1/favicon.png"),
			'posts' : map((lambda rel : blog_file_path.parent / rel), md_meta_get(meta, 'posts', [], False)),
			'meta' : meta
		}

def read_post(post_file_path):
	with post_file_path.open() as fin:
		row_post = md_read(fin.read())
		post = {}
		post['meta'] = row_post['meta']
		post['content'] = row_post['content']
		post['title'] = md_meta_get(row_post['meta'], 'title', post_file_path.with_suffix("._").name)
		post['short_title'] = md_meta_get(row_post['meta'], 'short_title', post['title'])
		post['link_base'] = md_meta_get(row_post['meta'], 'link', post_file_path.with_suffix(".html").name)
		post['link'] = './' + post['link_base']
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
	t = target.as_posix()
	if not os.path.exists(t): os.makedirs(t)
	files = glob.glob(t + '/*')
	for f in files:
		os.remove(f)

def generate(blog, args):
	prepare_favicon(blog, args.target)
	posts = map(read_post, blog['posts'])
	for post in posts:
		write_templated(args.templates / "post.template.html", args.target / post['link_base'], {'blog' : blog, 'posts': posts, 'post': post})			
	write_templated(args.templates / "index.template.html", args.target / "index.html", {'blog' : blog, 
		'posts':posts})
		
if __name__ == "__main__":
	import argparse
	from pathlib import Path

	parser = argparse.ArgumentParser(description='Generates static blog content from markdown posts.')
	parser.add_argument('blog', type=Path, help='File with general information about blog', default='blog')
	parser.add_argument('-target', type=Path, help='generated content destination', default='target')
	parser.add_argument('-templates', type=Path, help='directory with templates', default='templates')

	args = parser.parse_args()
	blog = read_blog_meta(args.blog)
	clean_target(args.target)
	generate(blog, args)







