blogator
========

Static blog generator

Python script that generates static content for blog. It uses sample posts in markdown format as input and produces html that can be uploaded to static content hosting like [github pages][3]. See sample [input][1] and [output][2]. 

Usage: 
 - install dependencies: `pip3 install -r requirements.txt`
 - generate content: `python3 blogator.py  sample/src/blog -target sample/target`

Python3 is required.

 [1]: https://github.com/st-kurilin/blogator/tree/master/sample/src
 [2]: https://github.com/st-kurilin/blogator/tree/master/sample/target
 [3]: https://pages.github.com/