
import sys

def write_templated(template_path, out_path, data):
	import pystache
	outs = out_path.open('w')
	template = pystache.parse(template_path.open('r').read())
	renderer = pystache.Renderer()
	outs.write(renderer.render(template, data))

def read_post(inp):
	import markdown
	md = markdown.Markdown(extensions = ['meta'])
	content = md.convert(inp)
	return {
		'meta' : md.Meta.copy(),
		'content' : md.convert(inp)
	}


def generate(args):
	def get(map_of_lists, key, alt):
		if key in map_of_lists:
			if len(map_of_lists[key]) > 0:
				return map_of_lists[key][0]
		return alt

	posts = []
	for post_file in args.posts.iterdir():
		with post_file.open() as fin:
			row_post = read_post(fin.read())
			post = {'meta' : row_post['meta'],
					'content': row_post['content']}
			post['title'] = get(row_post['meta'], 'title', post_file.with_suffix("._").name)
			post['short_title'] = get(row_post['meta'], 'short_title', post['title'])
			post['link_base'] = get(row_post['meta'], 'link', post_file.with_suffix(".html").name)
			post['link'] = './' + post['link_base']

			posts.append(post)
			write_templated(args.templates / "post.template.html", args.target / post['link_base'], post)			
	write_templated(args.templates / "index.template.html", args.target / "index.html", {'posts':posts})
		
def prepare_directories(args):
	import os
	import glob
	t = args.target.as_posix()
	if not os.path.exists(t): os.makedirs(t)
	files = glob.glob(t + '/*')
	for f in files:
		os.remove(f)


if __name__ == "__main__":
	import argparse
	from pathlib import Path

	parser = argparse.ArgumentParser(description='Generates static blog content from markdown posts.')
	parser.add_argument('-posts', type=Path, help='directory with posts', default='posts')
	parser.add_argument('-target', type=Path, help='generated content destination', default='target')
	parser.add_argument('-templates', type=Path, help='directory with templates', default='templates')

	args = parser.parse_args()

	prepare_directories(args)
	generate(parser.parse_args())







