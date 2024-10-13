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

def run_app_server(   host:     str
                    , port:     int
                    , debug:    bool
                    , login:    Tuple[str, str] 
                    , wikipath: str
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
    # 
    def is_loggedin():
        return session.get("loggedin") or False
    def do_login():
        session["loggedin"] = True
    def do_logoff():
        session["loggedin"] = False
    @app.route("/login", methods = (M_GET, M_POST))
    def login():
        if not DO_LOGIN:
            return flask.redirect("/")
        if request.method == M_GET:
            if is_loggedin(): 
                return flask.redirect("/")
            else:
                return flask.render_template('login.html')
        assert request.method == M_POST
        username = flask.request.form.get("username") or ""
        password = flask.request.form.get("password") or ""
        if username == USERNAME and password == PASSWORD:
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
            if DO_LOGIN and not is_loggedin():
                response = flask.redirect("/login")
            else:
                response = http_handler(*args, **kwargs)
            return response 
        wrapper.__name__ = http_handler.__name__
        return wrapper

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
        content =  "\n".join([f"""<li><a href="/wiki/{f}{highlight}" class="link-internal">{f}</a></li>""" for f in pages])
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

    @app.route("/wiki/<page>")
    @check_login
    def route_wiki_page(page):
        mdfile = os.path.join(BASE_PATH, page + ".md")
        ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
        if not os.path.exists(mdfile):
             return f"<h1>404 NOT FOUND PAGE: {page}</h1>"
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

    @app.route("/")
    def route_index_page():
        return flask.redirect("/wiki/Index")

    app.run(host = host, port = port, debug = debug)
    ##return app

##if __name__ == '__main__':
##    print(" [TRACE] Server started Ok.")
##    app.run(host='0.0.0.0', port=8010, debug=True)
##
