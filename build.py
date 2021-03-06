"""Static blogs generator. Tests
See https://github.com/st-kurilin/blogator for details.

Builds final blogator.py script that should be distribured
"""

def main():
    """Start endpoint"""
    import textwrap
    with open('blogator_src.py') as srcf, open('blogator.py', 'w') as resf:
        src = srcf.read()
        resf.write(textwrap.dedent("""\
                   \"\"\"
                   Static blogs generator.\n
                   This file was generated. Do not edit it directly.
                   See https://github.com/st-kurilin/blogator for details.\n
                   \"\"\"
                   #__ignore comment bellow__"""))
        resf.write(src)
        resf.write('def fill_vitual_fs():\n'
                   '    """Fills virtual fs with default values"""\n'
                   '    from pathlib import Path\n')
        for template in ['index.template.html', 'post.template.html']:
            with open("templates/"  +  template) as templf:
                left = ("PREDEFINED[Path('blogtor-virtual') "
                        "/ 'templates' / '{}']".format(template))
                content = templf.read()
                resf.write('    {0} = """{1}"""\n'.format(left, content))
        resf.write(textwrap.dedent("""\
                   if __name__ == "__main__":
                        fill_vitual_fs()
                        main()\n"""))


if __name__ == "__main__":
    main()
