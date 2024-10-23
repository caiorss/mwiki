import os
import secrets
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
from flask import Flask, request, session
import flask_session
from typing import Tuple, List, Optional
import datetime

import mwiki.utils as utils
import mwiki.mparser as mparser 

## Http Method GET 
M_GET = "GET" 
# Http Method Post
M_POST = "POST"

def get_secret_key(appname: str) -> str:
    KEYFILE = "appkey"
    fkey =  utils.project_data_path(appname, KEYFILE)
    secret_key = ""
    # Generate secret key and store it in file within
    # the application data directory if the file 
    # does not exist yet.
    if not os.path.isfile(fkey):
        secret_key = secrets.token_hex(16)
        with utils.open_project_data_dir(appname, KEYFILE, "w") as fd:
            fd.write(secret_key)
    else:
        with open(fkey, "r") as fd:
            secret_key = fd.read()
            ##print(" [TRACE] secret_key = ", secret_key)
    return secret_key

def run_app_server(   host:        str
                    , port:        int
                    , debug:       bool
                    , login:       Optional[Tuple[str, str]]
                    , wikipath:    str
                    , random_ssl:  bool = False
                    , secret_key:  Optional[str] = None 
                   ):

    APPNAME = "mdwiki"
    session_folder = utils.project_cache_path(APPNAME, "session")
    utils.mkdir(session_folder)
    secret_key = get_secret_key(APPNAME) if secret_key is None else secret_key
    # TODO Separate configuration from code for safer deployment
    # Use some secrets management system
    app = Flask(__name__) ##template_folder="templates")
    # Specify a custom directory for storing session files
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = session_folder ## 'M:/code/flaskLoginTest/sessions'
    # Set the maximum number of stored sessions
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days = 30)
    app.config['SESSION_FILE_THRESHOLD'] = 1000  # Adjust the limit as needed
    # Configure Flask to use FileSystemSessionInterface with the custom options
    app.config["SESSION_PERMANENT"] = True
    app.config['SECRET_KEY'] = secret_key 
    flask_session.Session(app)
    ### WEBSOCKET: sock = Sock(app)
    BASE_PATH = wikipath ## utils.get_wiki_path()
    IMAGE_PATH = os.path.join(BASE_PATH, "images")
    #  For setting a username and password, just 
    # set the environment variable LOGIN, 
    # export LOGIN="<USERNAME>;<PASSWORD>"
    #
    DO_LOGIN = False
    USERNAME = ""
    PASSWORD = ""
    if login is not None:
        DO_LOGIN = True 
        (USERNAME, PASSWORD) = login

    check_login = add_login(app, DO_LOGIN, USERNAME, PASSWORD)

    ##@auth_basic(is_authhenticated)
    @app.route("/pages", methods = [M_GET])
    @check_login
    def route_pages():
        query = (request.args.get("search") or "").strip()
        highlight =  f"#:~:text={ utils.escape_url(query) }" if query != "" else ""
        files = []
        if query == "":
            files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md")]
        else:
            files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md") \
                        and utils.file_contains(os.path.join(BASE_PATH, f), query)]
                     ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
        sorted_files = sorted(files)
        page_to_file = lambda f:  os.path.join(BASE_PATH, f) # + ".md"
        MAX_LEN = 200
        pages = [  {    "name": f.split(".")[0] 
                      , "src":  f 
                      , "matches": [ lin[:MAX_LEN] + " ..." 
                                    if len(lin) > MAX_LEN else lin  
                                        for (n, lin) in  utils.grep_file(page_to_file(f), query)  ] \
                                    if query != "" else [ ]

                      , "metadata": mparser.get_pagefile_metadata( page_to_file(f))
                   } 
                 for f in sorted_files ]
        title = f"Search results for \"{query}\"" if query != "" else "All pages"
        response = flask.render_template( "listing.html"
                                         , title = title
                                         , pages = pages
                                         , query = query
                                         )
        return response


    @app.route("/check")
    def hello():
        return "The server is up and running. OK."

    @app.get("/wiki/img/<path:filepath>")
    @check_login
    def route_wiki_image(filepath):
        root = IMAGE_PATH ## utils.get_wiki_path("images")
        resp = flask.send_from_directory(root, filepath)
        return resp

    @app.route("/wiki/<page>/source")
    @check_login
    def route_wiki_source(page):
        mdfile = os.path.join(BASE_PATH, page + ".md")
        ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
        if not os.path.exists(mdfile):
             return f"<h1>404 SOURCE NOT FOUND: {page}</h1>"
        src = ""
        with open(mdfile) as fd:
            src = fd.read()
        src = utils.escape_html(src)
        content = f"<pre>\n{src}\n</pre>" 
        html = mparser.fill_template(f"Source of '{page}.md'", content, toc = "", query = "")
        return html


    @app.route("/wiki/<page>")
    @check_login
    def route_wiki_page(page):
        mdfile = os.path.join(BASE_PATH, page + ".md")
        # ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
        if not os.path.exists(mdfile):
              return f"<h1>404 PAGE NOT FOUND: {page}</h1>"
        headings = []
        with open(mdfile) as fd:
            inp = fd.read()
            headings = mparser.get_headings(inp)
        root = mparser.make_headings_hierarchy(headings)
        # ## breakpoint()
        toc      = mparser.headings_to_html(root)
        content  = mparser.pagefile_to_html(mdfile)
        response = flask.render_template(  "content.html"
                                         , title   = page
                                         , content = content
                                         , toc     = toc
                                         )
        return response

    @app.get("/")
    def route_index_page():
        index_file = os.path.join(BASE_PATH, "Index.md")
        response = ""
        if os.path.isfile(index_file):
            response = flask.redirect("/wiki/Index")
        else:
            response = flask.redirect("/pages")
        return response

    if random_ssl:
        with utils.TempSSLCert() as c:
            certfile, keyfile = c.certkey()
            assert os.path.exists(certfile)
            assert os.path.exists(keyfile)
            context = (certfile,  keyfile)
            ## context = ("cert.pem",  "key.pem")
            app.run(host = host, port = port, debug = debug, ssl_context = context)
    else:
        app.run(host = host, port = port, debug = debug)


def add_login(app: Flask, do_login: bool, username: str, password: str):
    """Create login form routes for a single user account

    :param do_login: Flag - if set to true, login form is enabled, otherwise login form is disabled.
    :param username: Username required for authentication
    :param password: Corresponding password required for user authentication.
    :returns:        Function decorator for enforcing user authentication.

    Required Python Pakages: flask_session 
    
    This function creates a login form for a single user account by defining 
    the following http routes 

    /login  => Login form, where the user is redirect to in views/routes 
               that requeries authentication if the user is not logged in.

    /loggof => Logs off user and redirects to '/' root page of the site.

    This function returns a decorator function check_login, that can 
    be added to routes/views for requiring authentication. 

    Usage example:
     
    ```python

       app = Flask(__name__)

       LOGIN_ENABLED = True 

       # Creates login form for single user account 
       # requiring "dummy" as username and "pass" as password
       # for authentication.
       check_login = add_login(app, LOGIN_ENABLED, "dummy", "pass")
       
       # Require login for accessing http://<site-url>/check
       @app.route("/check")
       @check_login 
       def hello():
           return "The server is up and running. OK."
    ```

    """
    def is_loggedin():
        return session.get("loggedin") or False

    def do_login():
        session["loggedin"] = True

    def do_logoff():
        session["loggedin"] = False

    @app.route("/api/logged", methods = (M_GET, ))
    def api_is_logged_in():
        res =  session.get("loggedin") or False
        output = flask.jsonify({ "logged": res})
        return output

    @app.route("/login", methods = (M_GET, M_POST))
    def login():
        if not do_login:
            return flask.redirect("/")
        if request.method == M_GET:
            if is_loggedin(): 
                return flask.redirect("/")
            else:
                return flask.render_template('login.html')
        assert request.method == M_POST
        _username = flask.request.form.get("username") or ""
        _password = flask.request.form.get("password") or ""
        if _username == username and _password == password:
            do_login() 
            return flask.redirect("/") 
        else:
            return flask.redirect("/login")

    @app.route("/logoff")
    def loggof():
        do_logoff()
        return flask.redirect("/login")

    def check_login(http_handler):
        """Decorator that redirects to /login page if the user is not loggged in."""
        def wrapper(*args, **kwargs):
            pass
            response = None
            if do_login and not is_loggedin():
                response = flask.redirect("/login")
            else:
                response = http_handler(*args, **kwargs)
            return response 
        wrapper.__name__ = http_handler.__name__
        return wrapper

    return check_login

