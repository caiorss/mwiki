import os
from mwiki.server import run_app_server
import mwiki.utils as utils
import tomli 
from pprint import pprint

import click
## from click.decorators import commmand 

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
def server(host: str, port: int, debug: bool, login: str, wikipath: str, random_ssl: bool, config):
    _login = None  

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
        run_app_server(_host, _port, _debug, _login, _wikipath, _random_ssl)
        exit(0)
        
    if login != "":
        #os.environ["DO_LOGIN"] = "true"
        _login =  login.split(",")
        if len(_login) != 2:
            print("Error expected login in format --login=<USERNAME>;<PASSWORD>")
            exit(1)
    _wikipath = utils.expand_path(wikipath)
    run_app_server(host, port, debug, _login, _wikipath, random_ssl)
    ## app.run(host = host, port = port, debug=True)

def main():
    cli = click.CommandCollection(sources = [ cli1 ])
    cli()

