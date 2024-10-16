import os
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
from flask import Flask, request, session
import flask_session

import mdwiki.utils as utils
import mdwiki.mparser as mparser 
from typing import Tuple, List

## Method GET 
M_GET = "GET" 
M_POST = "POST"


def run_app_server(   host:        str
                    , port:        int
                    , debug:       bool
                    , login:       Tuple[str, str] 
                    , wikipath:    str
                    , random_ssl:  bool = False
                   ):
    # TODO Separate configuration from code for safer deployment
    # Use some secrets management system
    app = Flask(__name__) ##template_folder="templates")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'd21275220cc324ea002684309195b6741b27ce281dc36294'
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
        query = request.args.get("search") or ""
        highlight =  f"#:~:text={ utils.encode_url(query) }" if query != "" else ""
        files = []
        if query == "":
            files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md")]
        else:
            files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md") \
                        and utils.file_contains(os.path.join(BASE_PATH, f), query)]
                     ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
        sorted_files = sorted(files)
        pages = [f.split(".")[0] for f in sorted_files]
        content = ""
        page_to_file = lambda page:  os.path.join(BASE_PATH, f) + ".md"
        if query == "":
            content =  "\n".join([f"""<li><a href="/wiki/{f}{highlight}" class="link-internal">{f}</a></li>""" 
                              for f in pages])
        else:
            for f in pages:
                inner =  "\n".join( [ utils.replace_ci(f"<li><code>{ utils.escape_html(lin) }</code></li>"
                                        , query, f'<span class="search-highlight">{query}</span>') 
                                       for (n, lin) in  utils.grep_file(page_to_file(f), query)])
                url = utils.encode_url(f"/wiki/{f}") + highlight
                entry = f"""<li><a href="{url}" class="link-internal">{f}</a> <ul>{inner}</ul></li>""" 
                content += entry
            content = f"<ul>\n{content}\n</ul>"
        content = f"""<h1>Markdown Wiki Pages</h1>\n<ul>\n{content}\n</ul>"""
        html = mparser.fill_template("Index Page", content, toc = "", query = query)
        return html

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
        ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
        if not os.path.exists(mdfile):
             return f"<h1>404 PAGE NOT FOUND: {page}</h1>"
        headings = []
        with open(mdfile) as fd:
            inp = fd.read()
            headings = mparser.get_headings(inp)
        root = mparser.make_headings_hierarchy(headings)
        ## breakpoint()
        toc = mparser.headings_to_html(root)
        # TOC - Table of Contents
        ## toc = ""
        ## for (label, id, _) in headings:
        ##      toc += f"""<li ><a href="#{id}" class="link-internal" >{label}</a></li>"""
        ## toc = f"<lu>\n{toc}\n</lu>"
        html = mparser.mdfile_to_html(mdfile, page, toc)
        mparser.make_headings_hierarchy(headings)
        return html

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

