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

host = "0.0.0.0"
port = 8000 
debug = False
wikipath = os.getenv("WIKIPATH", "./notes")
app = make_app_server(  host     = host
                      , port     = port
                      , debug    = debug
                      , login    = None #("user", "pass")
                      , wikipath = wikipath 
                      )

if __name__ == "__main__":
    app.run()