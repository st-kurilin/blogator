"""
Static blogs generator. Tests
See https://github.com/st-kurilin/blogator for details.

Builds final blogator.py script that should be distribured
"""

if __name__ == "__main__":
    with open("blogator_src.py", 'r') as srcf, open("blogator.py", 'w') as resf:
        src = srcf.read()
        resf.write(src)
