"""WSGI Entry Point for running the application with gunicorn

To start this server, run the following command in 
a terminal:

  $  gunicorn \
      -e WIKIPATH=$HOME/wiki-mdfiles \
     --workers 4  \
     --bind 0.0.0.0:8000 mwiki.wsgi:app

"""
import os
import logging
import flask
import logging
from mwiki.server import make_app_server
from . import utils
from mwiki.models import MwikiConfig
##from .app import app


#host = os.getenv("HOST", "0.0.0.0")
port = utils.parse_int(os.getenv("PORT", "8000")) or 8000
#wikipath = os.getenv("MWIKI_PATH", ".")
wikipath = MwikiConfig.path
host = MwikiConfig.host
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

logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

@app.after_request
def log_request_response(response: flask.wrappers.Response):
  """Request-response logger for waitress WSGI logger.
  NOTE: This custom logger is necessary because waitress
  does not log the network traffic by default.
  """
  ##print(" response = ", type(response))
  request: flask.Request = flask.request
  agent = request.headers.get("User-Agent") 
  realAddr = request.headers.get("X-Forwarded-For") or request.headers.get("X-Real-IP") or ""
  msg =  (  f" Method: {request.method} ; Path: {request.path} ;"
            f"  Addr: {request.remote_addr} ; Real-Addr: {realAddr} ; User-Agent: {agent} ; Resp: {response.status} ")
  logger.log(logging.INFO, msg) 
  return response

if __name__ == "__main__":
    app.run()
