
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


def generate(templates_dir, posts_dir, out_dir):
	def get(map_of_lists, key, alt):
		if key in map_of_lists:
			if len(map_of_lists[key]) > 0:
				return map_of_lists[key][0]
		return alt

	posts = []
	for post_file in posts_dir.iterdir():
		with post_file.open() as fin:
			row_post = read_post(fin.read())
			post = {'meta' : row_post['meta'],
					'content': row_post['content']}
			post['title'] = get(row_post['meta'], 'title', post_file.with_suffix("._").name)
			post['short_title'] = get(row_post['meta'], 'short_title', post['title'])
			post['link_base'] = get(row_post['meta'], 'link', post_file.with_suffix(".html").name)
			post['link'] = './' + post['link_base']

			posts.append(post)
			write_templated(templates_dir / "post.template.html", out_dir / post['link_base'], post)			
	write_templated(templates_dir / "index.template.html", out_dir / "index.html", {'posts':posts})
		
def clean_dir(dir):
	print ("cleaning")

if __name__ == "__main__":
	from pathlib import Path
	from_dir = Path(sys.argv[1])
	to_dir = Path(sys.argv[2])
	templates_dir = Path(sys.argv[3])

	generate(templates_dir, from_dir, to_dir)







