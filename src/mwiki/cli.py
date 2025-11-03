"""Command Line Handler 

Module responsible for processing command line switches and options.
"""
import os
import os.path 
import sys
import random
import pathlib
import subprocess
import tomli 
import shutil
from pprint import pprint
from typing import Optional, Tuple, List 
import click
import flask 
import jinja2
##import waitress
## from click.decorators import commmand 
## from gunicorn.app.wsiapp import run 
import multiprocessing
import mwiki.utils as utils
from mwiki.server import make_app_server
import mwiki.convert
import mwiki.search as search
import mwiki.mparser as mparser
import mwiki.watcher
import mwiki.render as render
import mwiki.models
import mwiki.utils as utils
from mwiki.latex_svg import LatexFormula
from . import render
from .models import User, Settings
from .app import db, app 
import mwiki.export 

def debughook(etype, value, tb):
    import pdb
    import traceback
    traceback.print_exception(etype, value, tb)
    print() # make a new line before launching post-mortem
    pdb.pm() # post-mortem debugger


def generate_login_token_url(wikipath: Optional[str], user: str):
    """Create URL for authentication without password. The token is valid for 20 seconds."""
    MWIKI_URL = os.getenv("MWIKI_URL", "http://localhost:8000")
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error expected --wikipath=./path-to-wiki or MWIKI_PATH environment variable set to this path.")
        exit(1)
    wikipath = utils.expand_path(wikipath)
    mwiki.models.MwikiConfig.set_path(wikipath)
    secret_key = mwiki.models.get_secret_key()
    ## print(" [TRACE] secret_key = ", secret_key)
    timestamp = utils.now_utc_timestamp_add_timedelta(minutes = 0, seconds = 20)
    salt = random.randint(1, 1000)
    message = user + "/" + str(timestamp) + "/" + str(salt)
    signature = utils.hmac_signature(secret_key, message)
    data = { "user": user, "salt": salt, "expiration": timestamp, "signature": signature}
    authtoken = utils.encode_json_to_base64(data)
    url = f"{MWIKI_URL}/auth?token={ utils.escape_url(authtoken) }"
    print("Copy and paste the following URL in the web browser to authenticate.")
    print()
    print(" ", url)
    print()
    print(f"Or paste the following token in the log in form {MWIKI_URL} ")
    print(" \n", authtoken)
    print()
    print("NOTE: This URL is only valid for 20 seconds.")
    print("NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL."
           "For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before "
           "running this comamnd again." )
    print()


@click.group()
def cli1():
    pass


@cli1.command()
@click.option("-h", "--host", default = "0.0.0.0", help="Host to be listened, default 0.0.0.0")
@click.option("-p", "--port", default = 8080, help="TCP port to be listend, default 8080.")
@click.option("--login", default = "", help = "Require login to access any page.")
@click.option("--debug", is_flag = True
            , help =( "Run server in debug mode. WARNING: It is unsafe to run" 
                     " the server in debug mode when exposed in the internet since" 
                     " it can display creadentials and tokens passed as environment" 
                     " variables and expose internal details."
                     ))
@click.option("--random-ssl", is_flag  = True
                , help = ( "Run server with random generated SSL certificate. "
                          " It is not necessary to run openssl command line tool"
                          " or create or pass any file in order to use this command line switch."
                          ))
@click.option("--wikipath", default = ".", help = "Path to wiki directory, default '.' current directory.")
@click.option("-c", "--config", default = None, 
                help = ( "Path to TOML configuration file for" 
                        "running the server and loading its settings from the file."))
@click.option("-s", "--secret-key", default = None, 
                help = ( "Secret key of flask application." ))
@click.option("-g", "--wsgi", 
                is_flag = True, 
                help = ( "Run application with gunicorn WSGI server."
                         "NOTE: Gunicorn only works on Unix-like systems, including "
                         "Linux, BSD or Apple's MacOS. This option is recommended for "
                         "deploying the server in production."
                         ))
@click.option("--pdb", is_flag = True, 
                help = ( "Enable post-mortem debugger." ))
@click.option("--auth", is_flag = True, help = "Create 20 seconds authenticatiion token and URL for passwordless login. (default user 'admin')")
@click.option("--auth-user", default = "admin", help = "Default user for the login token. (default admin)")
def server(  host:       str
           , port:       int
           , debug:      bool
           , login:      str
           , wikipath:   str
           , random_ssl: bool
           , config:     str
           , secret_key: Optional[str]
           , pdb:        bool
           , wsgi:       bool
           , auth:       bool
           , auth_user:  str 
           ):
    """Run the mwiki server."""
    _login = None  
    if pdb:
        print("[INFO] Enabled Post-mortem debugger.")
        sys.excepthook = debughook
    # Default value for configuration variables
    _host = host 
    _port = port 
    _debug = debug
    _do_login = login
    _login = login.split(",")
    _username = _login[0] if len(_login) == 2 else ""
    _password = _login[1] if len(_login) == 2 else ""
    _wikipath = wikipath
    ## print(" [TRACE] (before) wikipath = ", _wikipath)
    _secret_key = secret_key
    _random_ssl = random_ssl
    ##_pdb = pdb 
    _wsgi = wsgi 
    ## ---- Load server settings from a configuration file --- ## 
    if config is not None:
        if not os.path.isfile(config):
            print(f"Error file '{config} does not exist")
            exit(1)
        conf = {}
        with open(config, 'rb') as fd:
            conf = tomli.load(fd)
        if "server" not in conf:
            print(f"Error - missing section [server] in toml config file '{config}'.")
            exit(1)
        server      = conf.get("server", {})
        _host       = server.get("host", "127.0.0.1")
        _port       = server.get("port", 8080)
        _debug      = server.get("debug", False)
        _do_login   = server.get("login", False)
        _username   = server.get("username", "")
        _password   = server.get("password", "")
        _wikipath   = utils.expand_path( server.get("wikipath", ".") )
        _random_ssl = server.get("random-ssl", False)
        _login = (_username, _password) if _do_login else None 
        _secret_key = server.get("secret_key", None)
        #make_app_server(_host, _port, _debug, _login, _wikipath, _random_ssl, _secret_key)
    _wikipath = utils.expand_path(_wikipath)

    if auth:
        generate_login_token_url(_wikipath, auth_user)
    
    if debug:
        mwiki.models.MwikiConfig.enable_debug()
    if not os.path.isdir(_wikipath):
        print("ERROR: Expected an existing wiki directory files (markdown repository).")
        print(f"Directory {_wikipath} not found.")
        exit(1)
    if login != "":
        #os.environ["DO_LOGIN"] = "true"
        if len(_login) != 2:
            ### print("Error expected login in format --login=<USERNAME>;<PASSWORD>")
            exit(1)
    # Add all markdown files (Wiki pages) to the search index database (powered by Whoosh Python library)
    base_path = pathlib.Path(_wikipath)
    mwiki.models.MwikiConfig.set_path(_wikipath)
    if not search.search_index_exists(base_path):
        search.index_markdown_files(base_path)
    if wsgi:
        _loginp = f"{_username},{_password}" if _username != "" else None
        os.environ["SERVER_SOFTWARE"] = "waitress"
        os.environ["WIKIPATH"] = _wikipath
        os.environ["MWIKI_PATH"] = _wikipath
        pyexecutable = sys.executable
        procWatcher =  subprocess.Popen([  pyexecutable
                                      ,"-m" , "mwiki.watcher"
                                      ]) 
        ## print(" [TRACE] procWatcher = ", procWatcher.pid)
        proc = subprocess.Popen([  pyexecutable
                                 , "-m" , "waitress"
                                 , f"--port={port}"
                                 , f"--host={host}"
                                 , "mwiki.wsgi:app"
                                 ]) 
        proc.wait()
        ## print(" [TRACE] Starting flask app using WSGI, wikipath = ", _wikipath)
        ### gunicorn_runner(_host, _port, _wikipath
        ###                 , login = _loginp 
        ###                 , secret_key= _secret_key
        ###                 )
        exit(0)
    _login =  x if len(x := login.split(",")) == 2 else None
    app = make_app_server(  host       = _host
                          , port       = _port
                          , debug      = _debug
                          , login      = _login
                          , wikipath   = _wikipath
                          , secret_key = _secret_key
                          , random_ssl = _random_ssl
                          )
    app.run(host = host, port = port, debug = debug)
    ## app.run(host = host, port = port, debug=True)


@cli1.command()
@click.option("--wikipath", default = "", help = "Path to wiki directory, default '.' current directory.")
def watch(wikipath: str):
    """Start watcher process manually for debugging purposes.
    """
    _wikipath = utils.expand_path( wikipath ) \
                if  wikipath != "" else os.environ.get("MWIKI_PATH", ".")
    mwiki.models.MwikiConfig.set_path(_wikipath)
    #os.environ["SERVER_SOFTWARE"] = "waitress"
    ## os.environ["WIKIPATH"] = _wikipath
    os.environ["MWIKI_PATH"] = _wikipath
    mwiki.watcher.watch()





@cli1.command()
@click.option("--wikipath", default = None, 
                help = ( "Path to folder containing *.md files." )
                )
@click.option("-o", "--output", default = None, 
                help = ( "Directory that will contain the compilation output (default value ./out)." )
                )
@click.option( "--page"
             , default = None
             , help = "Export single page to html, instead of the whole wiki.")
@click.option("--website-name", default = "MWiki", help="Name of the static website (default value 'MWiki').") 
@click.option("--root-url", default = "/", help="Root URL that the static website will be deployed to.  (default value '/').") 
@click.option("--locale", default = "en-US", help="Default locale of the user interface. (Default value 'en-US')") 
@click.option("--icon", default = None, help="Favicon of the static website. (Default value MWiki icon)") 
@click.option("--main-font", default = "literata", help="Main font used in document text.") 
@click.option("--code-font", default = "libertinus-mono", help="Code monospace font used in code blocks.") 
@click.option("--title-font", default = "news-reader", help="Title font used in document section headings.") 
@click.option("--list-fonts", is_flag = True, help="List all available fonts.") 
@click.option("--allow-language-switch", is_flag = True
              , help = ( "Allow end-user to switch the user interface language."
                         
             ))
@click.option("--self-contained", is_flag = True
             , help = ( "Embed all attachment within the current wiki page."
                        " JavaScripts and CSS are inlined and images are embedded in base64 encoding. The generated HTML self-contained file is similar to a PDF file."
                        " This flag is useful for generating self-contained documents for offline view."
            ) )
@click.option("--embed-mathjax", is_flag = True, help = ("Self host Mathjax library for rendering math formulas instead "
                                                        "of loading it from a CDN."))
@click.option("--latex-svg", is_flag = True, help = ("Render all LaTeX formulas and code as SVG images "
                                                     "instead of rendering them with MathJax."
                                                     " Note that this setting requires installing LaTeX dependencies and"
                                                     "compiling LaTeX to SVG consumes more time and resources. However "
                                                     "this enabling this flag is useful for generating self contained documents"
                                                     "or in cases when there is too much formulas and MathJax becomes very slow."
                                                    ))
@click.option("--verbose", is_flag = True, help = ("Display more information about the compilation output."))
@click.option("--author", default = None, help = (
                                            'Override the frontmatter attribute author in all wiki pages. '
                                            'The author field is compiled to <meta name="author" content="AUTHOR NAME"> '
                                            'This setting only makes sense if there is a single author.'
                                            ))

def export(   wikipath:              Optional[str]
            , output:                Optional[str]
            , page:                  Optional[str]
            , website_name:          str
            , root_url:              str 
            , locale:                str
            , icon:                  Optional[str]
            , main_font:             str 
            , code_font:             str 
            , title_font:            str 
            , list_fonts:            bool 
            , allow_language_switch: bool
            , self_contained:        bool 
            , embed_mathjax:         bool
            , latex_svg:             bool 
            , verbose:               bool 
            , author:                str 
    ):
    "Export a MWiki repository or a markdown files repository to a static website."""
    mwiki.export.export(  wikipath, output, page, website_name
                        , root_url, locale, icon, main_font
                        , code_font, title_font
                        , list_fonts, allow_language_switch, self_contained
                        , embed_mathjax, latex_svg  , verbose  , author  )        
 
 
@cli1.command()
@click.option("-p", "--path", default = None, 
                help = ( "Path to folder containing *.md files." )
                )
@click.option("-f", "--file", default = None, 
                help = ( "Path to *.md file to be compiled." )
                )
def compile_latex(path: Optional[str], file: Optional[str]):
    """Compile Latex Formulas of .md file or folder to SVG images.
    The images are stored in the cache folder.
    """
    if file is not None:
        if not os.path.isfile(file):
            print(f" [ERROR] File {file} does not exist.")
            exit(1)
        render.compile_pagefile(file)
        exit(0)
    if path is None:
        print("Error expected path to folder")
        exit(1)
    ##pattern = os.path.join(path, "*.md")
    ## files = glob.glob(pattern)
    render.compile_folder(path)
    ###print(" [INFO] Start compilation of ", path)
    ###with multiprocessing.Pool(4) as p:
    ###    p.map(render.compile_pagefile, files)
    ###print(" [INFO] End compilation of latex formulas in ", path)
    ##with multiprocessing.Pool(5) as p:
    ### # Create process pool 
    ### p = multiprocessing.Pool(5)
    ### p.map(render.compile_pagefile, files)
    ### p.close()
    # Wait for all task termination  
    ## p.join()
    ## input("Type RETURN to exit")
    ## render.compile_folder(path)

@cli1.command()
@click.option("--admin-password", 
                help = ( "Set admin password." )
                )
@click.option("--sitename", 
                help = ( "Change site name" )
                )
def manage(admin_password = None, sitename = None):
    """Manage MWiki settings, including accounts, passwords and etc."""
    if admin_password is not None:
        with app.app_context():
            admin = User.get_user_by_username("admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(" [*] Password changed for admin. Ok.")
    if sitename is not None:
        with app.app_context():
            settings = Settings.get_instance()
            settings.sitename = sitename
            settings.save()
            print(f" [*] Site name changed to: {sitename}")


@cli1.command()
@click.option("--wikipath", default = None, help = "Path to wiki directory, default '.' current directory.")
@click.option("--user", default = "admin", help = "Username to authenticate.")
def auth(wikipath: Optional[str], user: str):
    """Create token and url for authentication without password. The URL is valid for 20 seconds."""
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error extepected --wikipath or enviroment variable $MWIKI_PATH")
        exit(1)
    if not pathlib.Path(wikipath).resolve().is_dir():
        print(f"Error directory not found: {wikipath}")
        exit(1)
    generate_login_token_url(wikipath, user)
    exit(0)



@cli1.command()
@click.option("-f", "--file", default = None, 
                help = ( "Input markdown file to be converted." )
                )
@click.option("-o", "--output", default = None, 
                help = ( "Output file." )
                )
def convert(file: Optional[str], output: Optional[str]):
    """Convert from org-mode markup to markdown"""
    mwiki.convert.convert_file(file, output)


def main():
    cli = click.CommandCollection(sources = [ cli1 ])
    cli()

