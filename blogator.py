
import sys


def writeTemplated(template_path, out_path, data):
	import pystache
	outs = out_path.open('w')
	template = pystache.parse(template_path.open('r').read())
	renderer = pystache.Renderer()
	outs.write(renderer.render(template, data))


def generate(templates_dir, posts_dir, out_dir):
	import markdown
	import pystache
	from pathlib import Path
	posts = []
	for post_file in Path(posts_dir).iterdir():
		with post_file.open() as fin:
			post = {'title' : post_file.with_suffix("._").name,
				'link' 	: "./" + post_file.with_suffix(".html").name,
				'content': markdown.markdown(fin.read())}
			posts.append(post)
			writeTemplated(Path(templates_dir) / "post.template.html", Path(out_dir) / post_file.with_suffix(".html").name, post)			
	writeTemplated(Path(templates_dir) / "index.template.html", Path(out_dir) / "index.html", {'posts':posts})
		
def clean_dir(dir):
	print ("cleaning")

templatesDir = sys.argv[3]
fromDir = sys.argv[1]
toDir = sys.argv[2]


generate(templatesDir, fromDir, toDir)







