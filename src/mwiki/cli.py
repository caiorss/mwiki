import os
import sys
from mwiki.server import make_app_server
import mwiki.utils as utils
from . import render
import tomli 
from pprint import pprint
from typing import Optional, Tuple, List 
import click
## from click.decorators import commmand 


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
@click.option("-w", "--wikipath", default = ".", help = "Path to wiki directory, default '.' current directory.")
@click.option("-c", "--config", default = None, 
                help = ( "Path to TOML configuration file for" 
                        "running the server and loading its settings from the file."))
@click.option("-s", "--secret-key", default = None, 
                help = ( "Secret key of flask application." ))
@click.option("--pdb", is_flag = True, 
                help = ( "Enable post-mortem debugger." ))
def server(  host: str
           , port: int
           , debug: bool
           , login: str
           , wikipath: str
           , random_ssl: bool
           , config
           , secret_key: Optional[str]
           , pdb: bool
           ):
    """Run the mwiki server."""
    _login = None  

    if pdb:
        print("[INFO] Enabled Post-mortem debugger.")
        sys.excepthook = debughook

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
        make_app_server(_host, _port, _debug, _login, _wikipath, _random_ssl, _secret_key)
        exit(0)
        
    if login != "":
        #os.environ["DO_LOGIN"] = "true"
        _login =  login.split(",")
        if len(_login) != 2:
            print("Error expected login in format --login=<USERNAME>;<PASSWORD>")
            exit(1)
    _wikipath = utils.expand_path(wikipath)
    app = make_app_server(host, port, debug, _login, _wikipath, random_ssl)
    app.run(host = host, port = port, debug = debug)
    ## app.run(host = host, port = port, debug=True)


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
    import glob 
    import os.path 
    import multiprocessing
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


def main():
    cli = click.CommandCollection(sources = [ cli1 ])
    cli()

