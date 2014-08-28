
import sys


def generate(posts_dir, out_dir):
	import markdown
	from pathlib import Path
	posts_names = []
	posts_links = []
	for post in Path(posts_dir).iterdir():
		with post.open() as fin:
			posts_links.append(post.with_suffix(".html").name)
			posts_names.append(post.with_suffix(".name").name)
			fout = Path(out_dir) / post.with_suffix(".html").name
			fout.open('w').write(markdown.markdown(fin.read()))
	fout = Path(out_dir) / "index.html"
	fs = fout.open('w')
	for name, link in zip(posts_names, posts_links):
		fs.write("<a href='%s'>%s</a>\n" % (link, name))



		
def clean_dir(dir):
	print ("cleaning")

fromDir = sys.argv[1]
toDir = sys.argv[2]

generate(fromDir, toDir)







