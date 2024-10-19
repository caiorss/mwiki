from setuptools import setup, find_packages

setup(
      name        = "mdwiki"
    , version     = "0.1"
    , description = ( "mdwiki - Markdown Wiki Server for publishing and accessing" 
                     " Github Markdown-Flavor Documents, MyST (from Jupyter Books) documents"
                     " and  Obsidian Markdown vaults."
                     )
    , packages    = find_packages(include=["mdwiki", "mdwiki.plugins"])
    , author      = "Caio Rodrigues"
    ##, url          = "to complete"
    ##, download_url = "<ADD download URL>"
    , license = "AGPL - GNU Affero"
    , keywords = [ "wiki", "markdown", "MyST", "sphynx", "flask", "server", "web" ]
    , entrypoints = {
        "console_scripts": [
            "run-mdwiki = mdwiki.__main__:main"
        ]
    }
    , include_package_data = True
    , package_data = {
        '': [ "*.html", "templates/*.html" ]
    }
    , scripts = [ "./run-mdwiki"]
    , install_requires = [
        # 'flask'
          'flask==3.0.3'
        , 'flask-session'
        , 'frontmatter'
        # , 'frontmatter==3.0.8'
        ## , 'linkfy-it-py'
        , 'markdown-it-py==3.0.0'
        , 'markdown-it-py[linkify, plugins]'
        ##, 'mdit-py-plugin'
        , 'pygments'
        , 'click==8.1.7'
        , 'cryptography'
        , 'tomli'
    ]
)