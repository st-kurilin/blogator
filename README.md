blogator
========

Static blog generator

Our objectives about blogging are

 - text editor over editing text in browser
 - simple templating engine over [WYSIWYG][wg] editors 
 - dedicated source control system over primitive publishing mechanisms
 - highload resistance free static site hosting over paid complicated failable one

To serve it we provide simple [Python][py] script that will generates content from [markdown][md] templates.

 To start use it you need to perform just few steps

  1. Download [blogator script][bl-distrib]
  2. Install dependencies with `pip3 install markdown` and `pip3 install pystache` commands
  3. Create file *BLOG_FILE* that will describe your blog. It could be as simple as

        title:           Blogging 
        annotation:      keep calm and blog on
        posts:           intro.md
                         history.md
                         popularity.md

  4. Create files with posts for `intro.md`, `history.md`, `popularity.md`. The could be as simple as

        title: About blog
        My blog entry

  5. Generate content: `python3 blogator.py BLOG_FILE -target OUTPUT_DIR`.
  6. Done! Generated content is now in *OUTPUT_DIR*.
  

Website Trafic's Statistic
-----
We support trafic's statistic throw integration with Google Analytics. To add it to your blog

 1. Sign up to the [Google Analytics][ga].
 2. Get your Tracking ID.
 3. Use this id as value for `ganalitics` in blog meta.


Comments
------
We support post comments throw integration with [Disqus][disqus]. To add comments to your blog

 1. Sign up to the [Disqus][disqus]
 2. Go to `Add Disqus to Your Site` page and fill form on that page
 3. Finish form on that page
 4. Choose `Universal code`
 5. Find your discus code at line `var disqus_shortname = 'YOUR_CODE';`
 6. Use this code for setting `disqus` value in blog meta.


Hosting
-----
One of hosting options could be GitHub pages. It's free and supports domains in format `YOUR_ID.github.io` or your custom domain. To host there 
 1. [Create Github account] [github-new]
 2. Create repository YOUR_ACCOUNT_NAME.github.io
 3. Push generated content to master branch of your repo

For details please wisit [GitHub pages][github-pages] 

Workflow
------
**TODO:** describe


System requerements
-----
We use `Python 3.4.1` for development. We do not test it on other Python versions. I assume that it should work fine for Python >= 3.2. Dependencies could be installed with `pip3 install -r requirements.txt` (**TODO:** revisit installiation)


Contribute
_____
Prerequirements are:
 - Installed git and created github account
 - Installed Python 3.4.+, pip3, [pylint][pylint]
 - Fork https://github.com/st-kurilin/blogator
 - Run `pip3 install -r requirements.txt` to install all dependencies
 - Make your changes. We use `blogator_src` as a main script. To build a distributable script run `build.py`. 
 - Make sure you pass tests from `blogator_test.py`. You can add more there as well.
 - Run pylint and make sure you leave the project better than you found it
 - Create a pull request


 [bl-distrib]: https://github.com/st-kurilin/blogator/blob/master/blogator.py
 [disqus]: https://disqus.com
 [github-pages]: https://pages.github.com/
 [github-new]: https://github.com/join
 [sample-input]: https://github.com/st-kurilin/blogator/tree/master/sample/src
 [sample-output]: https://github.com/st-kurilin/blogator/tree/master/sample/target
 [pages]: https://pages.github.com/
 [ga]: http://www.google.com/analytics/
 [wg]: https://en.wikipedia.org/wiki/WYSIWYG
 [md]: https://en.wikipedia.org/wiki/Markdown
 [py]: https://www.python.org
 [pylint]: https://www.pylint.org