"""
Static blogs generator. Tests
See https://github.com/st-kurilin/blogator for details.

Builds final blogator.py script that should be distribured
"""

def main():
    """Start endpoint"""
    with open("blogator_src.py", 'r') as srcf, open("blogator.py", 'w') as resf:
        src = srcf.read()
        resf.write("""
\"\"\"
Static blogs generator.\n
This file was generated. Do not edit it directly.
See https://github.com/st-kurilin/blogator for details.\n
\"\"\"

#__ignore comment bellow__
""")
        resf.write(src)
        resf.write("""if __name__ == "__main__":\n    main()\n""")


if __name__ == "__main__":
    main()
