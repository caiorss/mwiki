import os
import re
import pathlib
import secrets
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
from flask import Flask, request, session
import flask_session
from typing import Any, Tuple, List, Optional
import datetime
import mwiki 
from . import utils
from . import mparser
from . import render

## Http Method GET 
M_GET = "GET" 
# Http Method Post
M_POST = "POST"
# Http Delete Method
M_DELETE = "DELETE"

def run_app_server(   host:        str
                    , port:        int
                    , debug:       bool
                    , login:       Optional[Tuple[str, str]]
                    , wikipath:    str
                    , random_ssl:  bool = False
                    , secret_key:  Optional[str] = None 
                   ):

    APPNAME = "mwiki"
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
        # Get all pages in directories and subdirectories in a recursively way
        files_ = pathlib.Path(BASE_PATH).rglob("*.md")
        files = []
        if query == "":
            files = [f for f in files_ ]
        else:
            files = [f for f in files_ 
                        if utils.file_contains(str(f), query) ]
                     ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
        sorted_files = sorted(files, key = lambda x: x.name)
        page_to_file = lambda f:  str(f) ##os.path.join(BASE_PATH, f) # + ".md"
        MAX_LEN = 200
        pages = [  {    "name": f.name.split(".")[0] 
                     # , "src":  f 
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

    @app.get("/about")
    def route_about():
        resp = flask.render_template("about.html")
        return resp

    @app.get("/wiki/img/<path:filepath>")
    @check_login
    def route_wiki_image(filepath):
        root = IMAGE_PATH ## utils.get_wiki_path("images")
        resp = flask.send_from_directory(root, filepath)
        return resp

    @app.route("/wiki/math/<file>")
    def route_wiki_math(file):
        resp = flask.send_from_directory(render.svg_cache_folder, file)    
        return resp

    rpat = re.compile(r"!\[(.*?)\]\(data:image/(.+?);base64,(.*?)\)")

    def replacement_(m: re.Match) -> str:
        img = m.group(3)[:200] + "..."
        out = f"![{m.group(1)}](data:image/{m.group(2)};base64,{img})"
        return out

    @app.route("/source/<path>")
    @check_login
    def route_wiki_source(path):
        mdfile_ = path + ".md"
        match = next(base_path.rglob(mdfile_), None)
        if request.method == M_GET:
            if not match:
                flask.abort(404) 
        ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
        if not match.exists(): 
            flask.abort() 
        src = match.read_text()
        src = re.sub(rpat, replacement_, src)
        ## src = utils.escape_html(src)
        content = utils.highlight_code(src, "markdown")
        ## content = f"<pre>\n{src}\n</pre>" 
        ## html = mparser.fill_template(f"Source of '{page}.md'", content, toc = "", query = "")
        html = flask.render_template("source.html"
                                     , page = path 
                                     , title = f"Source: {path}"
                                     , content = content)
        return html

    ## Latex Macros to be Injected in Page Template
    latex_macros = utils.read_resource(mwiki, "macros.sty")

    base_path = pathlib.Path(BASE_PATH)

    @app.route("/wiki/<path>")
    @check_login
    def route_wiki_page(path: str):
        # path does not have exntension, it is just the name
        # of the mdfile without any extension
        if "." not in path:
            mdfile_ = path + ".md"
            ##print(f" [TRACE] mdfile_ = {mdfile_} ; base_path = {base_path}")
            matches = list(base_path.rglob(mdfile_))
            ## print(" [TRACE] matches = ", matches)
            # ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
            if len(matches) == 0:
                ## flask.abort(404) 
                out = flask.redirect(f"/create/{path}")
                return out
            mdfile = str(matches[0])
            headings = []
            with open(mdfile) as fd:
                inp = fd.read()
                headings = mparser.get_headings(inp)
            root = mparser.make_headings_hierarchy(headings)
            # ## breakpoint()
            toc      = mparser.headings_to_html(root)
            content  = render.pagefile_to_html(mdfile, base_path = BASE_PATH)
            ## print(" [TRACE] Macros = \n", latex_macros)
            response = flask.render_template(  "content.html"
                                             , title   = path
                                             , page    = path
                                             , content = content
                                             , toc     = toc
                                             , latex_macros = latex_macros
                                             )
            return response
        ## breakpoint()
        # Dont' show source code of markdown file
        if path.endswith(".md"):
            flask.abort(404)
        # Seach file in any directory in basepath recursively 
        # In the future this code can be optimized using some sort 
        # of caching or search index for speeding up 
        # the response.
        match: Optional[pathlib.Path] = next(base_path.rglob(path), None)
        if not match:
            flask.abort(404)
        relpath = match.relative_to(base_path)
        resp = flask.send_from_directory(BASE_PATH, relpath)
        return resp 
        # Attempt to server static file 

    @app.route("/api/wiki/<path>", methods = [M_GET, M_POST, M_DELETE])
    @check_login
    def api_wiki(path: str):
        mdfile_ = path + ".md"
        p: Optional[pathlib.Path] = next(base_path.rglob(mdfile_), None)
        if request.method == M_GET:
            if not p: flask.abort(404)
            content = p.read_text()
            out = flask.jsonify({ "status": "ok", "error": "", "content": content })
            return out
        elif request.method == M_POST:
            out = ""
            ## breakpoint()
            if p: 
                out = flask.jsonify({ "status": "error", "error": "Note already exists"})
            else: 
                p_ = base_path.joinpath(mdfile_)
                p_.touch()    
                out = flask.jsonify({ "status": "ok", "error": ""})
            return out
        elif request.method == M_DELETE:
            if not p: flask.abort(404)
            ## Remove file 
            p.unlink()
            out = flask.jsonify({ "status": "ok", "error": ""})
            return out
        else:
            flask.abort(405)

    @app.route("/create/<path>", methods = [M_GET, M_POST])
    def route_create(path: str):
        """Flask http route for creating new wiki pages/notes."""
        mdfile_ = path + ".md"
        p: Optional[pathlib.Path] = next(base_path.rglob(mdfile_), None)
        out = None 
        if p:
            out = flask.redirect(f"/wiki/{path}")
            return out
        if request.method == M_GET:
            out = flask.render_template("create.html", title = f"Creating page '{path}'", pagename = path)
        elif request.method == M_POST:
            ## _page        = flask.request.form.get("page", "") 
            label       = flask.request.form.get("label", "") 
            description = flask.request.form.get("description", "") 
            keywords    = flask.request.form.get("keywords", "") 
            submit_yes  = flask.request.form.get("submit-yes", "") 
            ##submit_no   = flask.request.form.get("submit-no", "") 
            ## breakpoint()
            if submit_yes == "YES":
                content = (   "---"
                             f"\ntitle:       {path}"
                             f"\nlable:       {label}"
                             f"\ndescription: {description}"
                             f"\nkeywords:    {keywords}"
                             "\n---\n\n"
                          )
                page_path = base_path.joinpath(path + ".md")
                page_path.write_text(content)
                out = flask.redirect(f"/wiki/{path}")
            else:
                out = flask.redirect(f"/")
        else:
            flask.abort(405)
        return out

    @app.route("/edit/<path>", methods = [M_GET, M_POST])
    @check_login
    def route_edit_page(path: str):
        mdfile_ = path + ".md"
        line_start = utils.parse_int(request.args.get("start"))
        line_end   = utils.parse_int(request.args.get("end"))
        match = next(base_path.rglob(mdfile_), None)
        if request.method == M_GET:
            if not match:
                flask.abort(404) 
            content = match.read_text() 
            ## breakpoint()
            if line_start is not None:
                lines = content.splitlines()
                content = "\n".join(lines[line_start:line_end]) 
            ## print(" [TRACE] content = ", content)
            resp = flask.render_template(  "edit.html"
                                         , title = f"Edit page: {path}", 
                                         page = path, content = content)
            return resp
        assert request.method == M_POST
        data: dict[str, Any] = request.get_json()
        content = data.get("content", "") 
        out = {}
        if not match:
            out = { "status": "error", "error": "Page not found." }
        elif not isinstance(content, str):
            out = { "status": "error", "error": "Invalid input. Expected text. " }
        else:
            ## lines = content.splitlines()
            if line_start is None:
                match.write_text(content)
            else:
                ## breakpoint()
                text = ""
                content_ = match.read_text() 
                lines_   = content_.splitlines()
                if line_end is not None:
                    lines    = lines_[0:line_start]
                    lines   = lines + content.splitlines()
                    lines   = lines + lines_[line_end:]
                    text = "\n".join(lines)
                else:
                    lines    = lines_[0:line_start]
                    lines   = lines + content.splitlines()
                    text = "\n".join(lines)
                match.write_text(text)                    
            out = { "status": "ok", "error": "" }
        resp = flask.jsonify(out)
        return resp

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

