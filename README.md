blogator
========

Static blog generator

Our objectives about blogging are

 - text editor over editing text in browser
 - simple templating engine over [WYSIWYG][wg] editors 
 - dedicated source control system over primitive publishing mechanisms
 - static site hosting over dynamic hosting where it is possible

To serve it we provide simple [Python][py] script that will generates content from [markdown][md] templates.

 To start use it you need to perform just few steps

  1. Download [blogator script][bl-distrib]
  2. Install dependencies with `pip3 install markdown` and `pip3 install pystache` commands
  3. Create file *BLOG_FILE* that will describe your blog. It could be as simple as

        title:           Blogging 
        annotation:      keep calm and blog on
        posts:           intro.md
                         history.md

  4. Create files with posts for `intro.md`, `history.md`. The could be as simple as

        title: About blog
        My blog entry

  5. Generate content: `python3 blogator.py BLOG_FILE -target OUTPUT_DIR`.
  6. Done! Generated content is now in *OUTPUT_DIR*.

  
Blog File Options
-----
You can specify next basic options in your *BLOG_FILE*

  - **title:**        title of your blog that could be shown on blog pages.
  - **annotation:**   short description that could be show on your pages.
  - **favicon-file:** file from your local file system that could be used as a favicon. 
    Could not be used together with `favicon` attribute.
  - **favicon:**      url to the image that could be used as favicon. 
    Could not be used together with `favicon-file` attribute.
  - **posts:**        lists of files where posts stored

See [blog file sample][sample-blog]


Post File Options
-----
You can specify next basic options in your *BLOG_FILE*
 - **title:** title of the post that could be displayed on the page, used to create links, etc.
 - **brief:** brief content that would be displayed on index page. If no brief present whole post will be shown.
 - **short_title:** shorten title that could be used to crete links, etc.
 - **link_base:** link to the post.
 - **published:** date of publishing that could be displayed on pages, used for sorting, etc. Use `%Y-%m-%d` format to specify it, like `2011-10-26`.



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
You can use any workflow to work with blogator. Here is one based on git branches

Prerequirements: 

 - python 3.2.+ installed
 - dependencies (*markdown*, *pystache*) installed
 - git installed
 - github account created 
 
 1. Create new repositiry on github
 2. Create new directory for your blog

            mkdir test-blog

 3. Change your directory to newly created

            cd test-blog

 4. Download blogator script

            curl https://raw.githubusercontent.com/st-kurilin/blogator/master/blogator.py > blogator.py

 5. Create place to store your blog's raw content. *src* directory will be created. *raw* branch will be used.

            git clone -b src --single-branch YOUR_GITHUB_REPO raw

 6. Create place to store your blog's generated content. *site* directory will be created. *master* branch will be used.

            git clone -b master --single-branch YOUR_GITHUB_REPO site

 7. Create all needed files in *src* directory. Including filling you blog meta file and posts. You can make commits and pushes when you need them.

            echo "title: Hello world" > src/blog

 8. Run blogator script to generate content

            python3 src/blog -target site

 9. Commit and push your *site* directory content.


Python Note
-----
We use `Python 3.4.1` for development. We do not test it on other Python versions. I assume that it should work fine for Python >= 3.2. Dependencies could be installed with `pip3 install -r requirements.txt`. 


Contribute
_____
Preretirements are:

 - Installed git and created github account
 - Installed Python 3.4.+, pip3, [pylint][pylint]

 To make you changes please follow next steps

 - Fork https://github.com/st-kurilin/blogator
 - Run `pip3 install -r requirements.txt` to install all dependencies
 - Make your changes. We use `blogator_src` as a main script. To build a distributable script run `build.py`. 
 - Make sure you pass tests from `blogator_test.py`. You can add more there as well.
 - Run pylint and make sure you leave the project better than you found it
 - Create a pull request

 [sample-blog]: https://github.com/st-kurilin/blogator/blob/master/sample/src/blog
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
 [pylint]: http://www.pylint.org
 