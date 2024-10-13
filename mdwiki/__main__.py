import os
from mdwiki.server import run_app_server
import mdwiki.utils as utils

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
            , help =( "Run server in debug mode. WARNING: It is unsafe to run " 
                     "the server in debug mode when exposed in the internet since" 
                     "it can display creadentials and tokens passed as environment" 
                     "variables and expose internal details."
                     ))
@click.option("-w", "--wikipath", default = "./pages", help = "Path to wiki directory")
def server(host: str, port: int, debug: bool, login: str, wikipath: str):
    _login = None
    if login != "":
        #os.environ["DO_LOGIN"] = "true"
        _login =  login.split(",")
        if len(_login) != 2:
            print("Error expected login in format --login=<USERNAME>;<PASSWORD>")
            exit(1)
    _wikipath = utils.expand_path(wikipath)
    run_app_server(host, port, debug, _login, _wikipath)
    ## app.run(host = host, port = port, debug=True)

def main():
    cli = click.CommandCollection(sources = [ cli1 ])
    cli()


if __name__ == '__main__':
    main()
    ## print(" [TRACE] Server started Ok.")
    ## app.run(host='0.0.0.0', port=8010, debug=True)
