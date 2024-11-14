"""WSGI Entry Point for running the application with gunicorn

To start this server, run the following command in 
a terminal:

  $  gunicorn \
      -e WIKIPATH=$HOME/wiki-mdfiles \
     --workers 4  \
     --bind 0.0.0.0:8000 mwiki.wsgi:app

"""
import os
from mwiki.server import make_app_server
from . import utils

host = os.getenv("HOST", "0.0.0.0")
port = utils.parse_int(os.getenv("PORT", "8000")) or 8000
wikipath = os.getenv("WIKIPATH", "./notes")
debug = os.getenv("DEBUG", "false") == "true"
login = os.getenv("LOGIN", "")
_login = login.split(",")
_login =  x if len( x := login.split(","))  == 2 else None
secret_key = os.getenv("SECRET_KEY")


app = make_app_server(  host     = host
                      , port     = port
                      , debug    = debug
                      , login    = _login 
                      , wikipath = wikipath 
                      )

if __name__ == "__main__":
    app.run()