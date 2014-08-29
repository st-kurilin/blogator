
import sys

def write_templated(template_path, out_path, data):
	import pystache
	outs = out_path.open('w')
	template = pystache.parse(template_path.open('r').read())
	renderer = pystache.Renderer()
	outs.write(renderer.render(template, data))

def generate_content(inp):
	import markdown
	return markdown.markdown(inp)

def generate(templates_dir, posts_dir, out_dir):
	posts = []
	for post_file in posts_dir.iterdir():
		with post_file.open() as fin:
			post = {'title' : post_file.with_suffix("._").name,
				'link' 	: "./" + post_file.with_suffix(".html").name,
				'content': generate_content(fin.read())}
			posts.append(post)
			write_templated(templates_dir / "post.template.html", out_dir / post_file.with_suffix(".html").name, post)			
	write_templated(templates_dir / "index.template.html", out_dir / "index.html", {'posts':posts})
		
def clean_dir(dir):
	print ("cleaning")

if __name__ == "__main__":
	from pathlib import Path
	from_dir = Path(sys.argv[1])
	to_dir = Path(sys.argv[2])
	templates_dir = Path(sys.argv[3])

	generate(templates_dir, from_dir, to_dir)







