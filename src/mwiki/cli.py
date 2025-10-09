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
from pprint import pprint
from typing import Optional, Tuple, List 
import click
##import waitress
## from click.decorators import commmand 
## from gunicorn.app.wsiapp import run 
import multiprocessing
import mwiki.utils as utils
from mwiki.server import make_app_server
import mwiki.convert
import mwiki.search as search
import mwiki.watcher
import mwiki.models
import mwiki.utils as utils
from . import render
from .models import User, Settings
from .app import db, app 


###  # Check whether the OS is a Unix-like operating system
###  if utils.is_os_linux_or_bsd() or utils.is_os_macos():
###      from gunicorn.app.wsgiapp import WSGIApplication
###  else:
###      print("WARNING: Cannot run using gunicorn on Microsoft Windows OS\n" 
###            "Use another WSGI server.")
###  
###  class StandaloneApplication(WSGIApplication):
###      def __init__(self, app_uri, options=None):
###          self.options = options or {}
###          self.app_uri = app_uri
###          super().__init__()
###  
###      def load_config(self):
###          config = {
###              key: value
###              for key, value in self.options.items()
###              if key in self.cfg.settings and value is not None
###          }
###          for key, value in config.items():
###              self.cfg.set(key.lower(), value)
###  
###  
###  def gunicorn_runner(  host:      str
###                      , port:      int
###                      , wikipath:  str
###                      , login:     Optional[str] = None
###                      , secret_key: Optional[str] = None 
###                      ):
###      options = {
###            "bind": f"{host}:{port}"
###          , "workers": (multiprocessing.cpu_count() * 2) + 1
###          ## "worker_class": "uvicorn.workers.UvicornWorker",
###      }
###      environemnt = {
###            "HOST":        host 
###          , "PORT":        str(port)
###          , "LOGIN":       login
###          , "SECRET_KEY":  secret_key
###          , "WIKIPATH":    wikipath
###      }
###      ### print(" [TRACE] wikipath = ", wikipath)
###      for (variable, value) in environemnt.items():
###          ## print(f" [TRACE] variable = {variable} ; value = {value}")
###          if value is not None: os.environ[variable] = value
###      ## See module: mwiki/wsgi, related to file mwiki/wsgi.py 
###      # the inputs of this module are environment variables
###      sapp = StandaloneApplication("mwiki.wsgi:app", options)
###      sapp.run()

def debughook(etype, value, tb):
    import pdb
    import traceback
    traceback.print_exception(etype, value, tb)
    print() # make a new line before launching post-mortem
    pdb.pm() # post-mortem debugger


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
@click.option("-p", "--path", default = None, 
                help = ( "Path to folder containing *.md files." )
                )
@click.option("-f", "--file", default = None, 
                help = ( "Path to *.md file to be compiled." )
                )
def compile(path: Optional[str], file: Optional[str]):
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
    """Create URL for authentication without password. The URL is valid for 1 minute."""
    MWIKI_URL = os.getenv("MWIKI_URL", "http://localhost:8000")
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error expected --wikipath=./path-to-wiki or MWIKI_PATH environment variable set to this path.")
        exit(1)
    wikipath = utils.expand_path(wikipath)
    mwiki.models.MwikiConfig.set_path(wikipath)
    secret_key = mwiki.models.get_secret_key()
    ## print(" [TRACE] secret_key = ", secret_key)
    timestamp = utils.now_utc_timestamp_add_minutes(1)
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
    print("NOTE: This URL is only valid for 1 minute.")
    print("NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL. For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before running this comamnd again.")

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

