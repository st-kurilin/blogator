
import sys


def generate(posts, out):
	import markdown
	from pathlib import Path
	for post in Path(posts).iterdir():
		with post.open() as fin:
			fout = Path(out) / post.with_suffix(".html").name
			fout.open('w').write(markdown.markdown(fin.read()))


		
def clean_dir(dir):
	print ("cleaning")

fromDir = sys.argv[1]
toDir = sys.argv[2]

generate(fromDir, toDir)







