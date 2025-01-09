import os
import re
import pathlib
import secrets
import urllib.parse
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy as sa 
import sqlalchemy
from sqlalchemy import ForeignKey
import sqlalchemy.orm as so 
import flask_session
import flask_wtf as fwt 
import wtforms as wt 
import wtforms.validators as wtfv 
from werkzeug.security import generate_password_hash, check_password_hash

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

APPNAME = "mwiki"
session_folder = utils.project_cache_path(APPNAME, "session")
utils.mkdir(session_folder)

app = Flask(__name__) ##template_folder="templates")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = session_folder ## 'M:/code/flaskLoginTest/sessions'
# Set the maximum number of stored sessions
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days = 30)
app.config['SESSION_FILE_THRESHOLD'] = 1000  # Adjust the limit as needed
# Configure Flask to use FileSystemSessionInterface with the custom options
app.config["SESSION_PERMANENT"] = True
dbpath = os.path.join(os.getcwd(), "database.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.filters['encode_url'] = lambda u: urllib.parse.quote_plus(u) 

def current_user():
    """Get user logged in to the server."""
    user: User = session.get("user") or User( username = "anonymous"
                                            , password = "dummy"
                                            , type = USER_ANONYMOUS)
    return user 

app.jinja_env.globals.update(current_user = current_user)

db = SQLAlchemy(app)


USER_MASTER_ADMIN = 100 
USER_ADMIN = 50 
USER_EDITOR = 20
USER_GUEST = 10  
USER_ANONYMOUS = 0 

class User(db.Model):
    __tablename__ = "user"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    username: so.Mapped[str] = so.mapped_column(index=True, nullable=False, unique=True)
    email:    so.Mapped[str] = so.mapped_column(nullable=True, unique=True)
    ## TODO IT should be stored only the password hash, never the password in plain text
    password: so.Mapped[str] = so.mapped_column(sqlalchemy.String(256), nullable= True)
    active:   so.Mapped[bool] = so.mapped_column(default= True)
    type:            so.Mapped[int] = so.mapped_column(default = 0)
    date_created:    so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)
    date_modified:   so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)
    date_lastaccess: so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)
    # date_modified  = so.mapped_column(DateTime, defalt=datetime.datetime.utcnow)

    def is_admin(self):
        result = self.type == USER_ADMIN or self.type == USER_MASTER_ADMIN 
        return result 
    
    def user_can_edit(self):
        result = self.active and (self.is_admin() or self.type == USER_EDITOR)
        return result 

    def is_anonymous(self):
        result = self.type == USER_ANONYMOUS
        return result

    def is_authenticated(self):
        result = self.type != USER_ANONYMOUS
        return result

    def check_password(self, password: str) -> bool:
        out =  check_password_hash(self.password, password)
        ## print(" [TRACE] password = ", password)
        return out


    def __repr__(self):
        return f"User{{ id = {self.id} ; username = {self.username}  ; type = {self.type} }}"

    @classmethod
    def get_user_by_username(self, username: str) -> Optional['User']:
        query = sqlalchemy.select(User).where(User.username.like(username))
        result = db.session.execute(query).scalars().first()
        return result

class Settings(db.Model):
    """Single-table instance of only one row that contains the Wiki settings.
    """
    __tablename__ = "settings"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    # Public => Indicates whether the wiki can be viewed (not edited) by everybody.
    public:   so.Mapped[bool] = so.mapped_column(default = False)
    # Web Site Name 
    sitename: so.Mapped[str] = so.mapped_column(default= "MWiki")
    default_password: so.Mapped[str] = so.mapped_column(nullable=False)
    # Wiki Site Description 
    description: so.Mapped[str] = so.mapped_column(default="MWiki Website")
    date_created:    so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)
    date_modified:   so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)

    @classmethod
    def get_instance(self):
        """Always use this method for obtaining a single instance of this class"""
        q = db.session.query(Settings).first()
        if q is None:
            # Generate unique default password per deployment
            password = utils.generate_password(10)
            # Create default settings when the database is initialized
            s = Settings( default_password = password )
            db.session.add(s)
            db.session.commit()
            return s 
        else:
            return q

    def save(self):
        """Update database entry"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        out = f"Settings{{  public = {self.public} ; sitename = {self.sitename}  }}" 
        return out

class Page(db.Model):
    __tablename__ = "page"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    file: so.Mapped[str] = so.mapped_column(unique = True, nullable = False)
    deleted: so.Mapped[bool] = so.mapped_column(default = False)
    date_modified:   so.Mapped[datetime.datetime]  = so.mapped_column(default=datetime.datetime.utcnow)

class BookmarkedPage(db.Model):
    __tablename__ = "bookmarkedpage"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey("user.id"))
    page_id: so.Mapped[int] = so.mapped_column(ForeignKey("page.id"))


def is_database_created() -> bool:
    tables = sqlalchemy.inspect(db.engine).get_table_names()
    result = tables != []
    return result 

def check_login_db(username: str, password: str) -> bool:
    ### print(" [TRACE] Enter check_login_db")
    res = User.get_user_by_username(username) 
    if res is None: 
        ##print(" [TRACE] Exit(1) check_login_db() ")
        ## breakpoint()
        return False
    ## breakpoint()
    if username == "admin" and res.password is None:
        dpassword = Settings.get_instance().default_password
        out = password == dpassword
    else:
        check = res.check_password(password) 
        out = res.active and check
    return out 

# --- Database Initialization -----#
# Create all database tables if they don't exist yet.
with app.app_context():
    u = None 
    created = is_database_created()
    if not created: 
        print(" [TRACE] Admin user created OK")
        u = User( username = "admin", type = USER_MASTER_ADMIN )

    db.create_all()
    if not created:
        db.session.add(u)
        db.session.commit()
    admin = User.get_user_by_username("admin")    
    if admin.password is None:
        conf = Settings.get_instance()
        password = conf.default_password
        print(f" [INFO] Enter the username: {admin.username} and password: '{password}' to log in.")


class SettingsForm(fwt.FlaskForm):
    """Form for changing Wiki Settings (Website settings)"""
    public =  wt.BooleanField("Public", 
                               description = "If enabled, everybody including non logged in users" 
                                             " will be able to view the wiki content. Note that "
                                             "only logged in users can edit the wiki."
                                             )
    submit = wt.SubmitField("Submit")
    sitename = wt.StringField("Wiki Name", validators = [ wtfv.DataRequired() ] )
    description = wt.TextAreaField("Wiki Description") 

        
class UserSettingsForm(fwt.FlaskForm):
    """Form that allows users to change their own account settings."""
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    submit   = wt.SubmitField("Update")

USER_TYPE_CHOICES = [(USER_MASTER_ADMIN, "Root Admin"), (USER_ADMIN, "Admin"), (USER_GUEST, "Guest") ]

class UserAddForm(fwt.FlaskForm):
    """Form for adding new user account manually."""
    username = wt.StringField("Username", validators = [ wtfv.DataRequired() ] )
    ## email    = wt.StringField("Email") 
    email    = wt.StringField("Email", validators = [ wtfv.DataRequired() ] )
    password = wt.PasswordField("Password", validators = [ wtfv.DataRequired() ] )
    ## password = wt.StringField("Password", validators = [ wtfv.DataRequired() ] )
    type     = wt.SelectField("Type", choices = USER_TYPE_CHOICES )
    ## active   = wt.BooleanField("Active", default = True) 
    submit   = wt.SubmitField("Update")

    def get_user_type(self):
        choice = dict(USER_TYPE_CHOICES).get(self.type.data)
        return choice



def make_app_server(  host:        str
                    , port:        int
                    , debug:       bool
                    , login:       Optional[Tuple[str, str]]
                    , wikipath:    str
                    , random_ssl:  bool = False
                    , secret_key:  Optional[str] = None 
                   ):

    secret_key = get_secret_key(APPNAME) if secret_key is None else secret_key
    # Specify a custom directory for storing session files
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


    @app.route("/user", methods = [M_GET, M_POST])
    @check_login( required = True )
    def route_user_settings():
        pass 
        user = current_user()
        form = UserSettingsForm()
        if request.method == M_GET:
            pass 
        if request.method == M_POST:
            form.validate()
            password = form.password.data
            ## breakpoint()
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            flask.flash("User account updated successfully. Ok.")
            flask.redirect("/user")
        resp = flask.render_template("user_settings.html", form = form, title = "User account settings")
        return resp

    @app.route("/account/new", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_user_add():
        user = current_user()
        if not user.is_admin():
            flask.abort(403)
        form = UserAddForm()
        ## if request.method == M_GET:
        ##     form.public.data = conf.public
        ##     form.sitename.data = conf.sitename
        ##     form.description.data = conf.description   
        if request.method == M_POST:
            form.validate()
            username = form.username.data
            email = form.email.data 
            type = form.get_user_type()
            _password =  form.password.data
            ### print(" [TRACE] password (new) = ", _password)
            password =  generate_password_hash(_password) 
            if User.get_user_by_username(username) is not None:
                flask.flash(f"Username {username} already exist.", "error")
                return flask.redirect("/account/new")
            new_user = User( username = username, email = email, password = password, type = type)
            db.session.add(new_user)
            db.session.commit()
            flask.flash("Error: User created successfully. Ok.")
            app.logger.info("User created ok.")
            return flask.redirect("/account/new")
        resp  = flask.render_template("add_user.html", form = form, title = "Add User")
        return resp

    @app.route("/settings", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_settings():
        user = current_user()
        if not user.is_admin():
            flask.abort(403)
        form = SettingsForm()
        resp = None
        conf = Settings.get_instance()
        if request.method == M_GET:
            form.public.data = conf.public
            form.sitename.data = conf.sitename
            form.description.data = conf.description   
        if request.method == M_POST:
            form.validate()
            app.logger.info(f"Form data = {form.data}")    
            conf.sitename = form.sitename.data
            conf.description = form.description.data
            conf.public = form.public.data 
            conf.save()
            flask.flash("Wiki settings updated successfully.")
            app.logger.info("Wiki setting updated.")
            flask.redirect("/settings")
        resp  = flask.render_template("settings.html", form = form, title = "Wiki Settings")
        return resp

    ##@auth_basic(is_authhenticated)
    @app.route("/pages", methods = [M_GET])
    @check_login()
    def route_pages():
        query = (request.args.get("search") or "").strip()
        # Possibliity: ?sort=modified, ?sort=name, ?sort=created
        sort  = request.args.get("sort", "")
        # Get all pages in directories and subdirectories in a recursively way
        files_ = pathlib.Path(BASE_PATH).rglob("*.md")
        files = []
        if query == "":
            files = [(f, 1) for f in files_ ]
        else:
            files = [(f, score) for f in files_ 
                        if (score := utils.file_contains(str(f), query)) != 0 ]
                     ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
        sorted_files = []
        if sort == "" or sort == "score":
            sorted_files = sorted(files, key = lambda x: x[1], reverse = True)
        elif  sort == "name":
            sorted_files = sorted(files, key = lambda x: x[0].name)
        elif sort == "modified":
            sorted_files = sorted(files, key = lambda x: x[0].stat().st_mtime, reverse = True )
        elif sort == "created":
            sorted_files = sorted(files, key = lambda x: x[0].stat().st_ctime, reverse = True)
        sorted_files = [ a for (a, _) in sorted_files ]
        page_to_file = lambda f:  str(f) ##os.path.join(BASE_PATH, f) # + ".md"
        MAX_LEN = 500
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
                                         , size  = len(pages)
                                         , query = query
                                         )
        return response

    # This variable is set to true if gunicorn WSGI server is being used.
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    ## print(" [TRACE] running gunicorn = ", is_gunicorn)

    @app.route("/check")
    def hello():
        return "The server is up and running. OK."

    @app.get("/about")
    def route_about():
        resp = flask.render_template("about.html", title="About MWiki")
        return resp

    @app.get("/licenses")
    def route_licenses():
        resp = flask.render_template("licenses.html", title="Open Source Licenses")
        return resp

    @app.get("/wiki/img/<path:filepath>")
    @check_login()
    def route_wiki_image(filepath):
        print(" [TRACE] path = ", filepath)
        root = IMAGE_PATH ## utils.get_wiki_path("images")
        print(" [TRACE] root = ", root)
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
    @check_login( required = True)
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
    @check_login()
    def route_wiki_page(path: str):
        # path does not have exntension, it is just the name
        # of the mdfile without any extension
        if "." not in path:
            mdfile_ = path + ".md"
            ##print(f" [TRACE] mdfile_ = {mdfile_} ; base_path = {base_path}")
            ## 
            ### breakpoint()
            ## is_special = path.startswith("special:")
            if path == "special:refcard":
                content = utils.read_resource(mwiki, "refcard.md")
                ast = mparser.parse_source(content)
                builder = render.HtmlRenderer(base_path=BASE_PATH)
                content = builder.render(ast)
                response = flask.render_template(  
                                               "standalone.html"
                                             , title   = "MWiki Markup Language Reference Card" # path
                                             , page    = path
                                             , content = content
                                             , latex_macros = latex_macros
                                             )
                return response
            match = next(base_path.rglob(mdfile_), None)
            ## print(" [TRACE] matches = ", matches)
            # ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
            if not match:
                ## flask.abort(404) 
                out = flask.redirect(f"/create/{path}")
                return out
            mdfile = match
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
        ## print(f" [TRACE] relpath = {path} ; match = {match}")
        resp = None
        ###  Render org-mode file 
        if path.endswith(".org"):
            content = match.read_text()
            builder = render.HtmlRenderer(base_path=BASE_PATH)
            ast = mparser.parse_source(content)
            html = builder.render(ast)
            ### ast = mparser.make_headings_hierarchy(headings)
            # ## breakpoint()
            ## toc = mparser.headings_to_html(root)
            response = flask.render_template(  "content.html"
                                             , title   = path
                                             , page    = path
                                             , content = html
                                             ## , toc     = toc
                                             , latex_macros = latex_macros
                                             )
            return response
        if not is_gunicorn:
            resp = flask.send_from_directory(BASE_PATH, relpath)
        else:
            import mimetypes
            import time
            # import datetime
            from dateutil.parser import parse as parsedate
            ## Get file mime type
            mtype, _ = mimetypes.guess_type(match.name, strict = False)
            mtype = mtype or "application/octect-stream"
            ## Get last modified time (formatted as string)
            pattern  = "%a, %d %b %Y %H:%M:%S %Z"
            last_modfied_timestamp = match.stat().st_mtime
            last_modified          = time.strftime(pattern, time.gmtime(last_modfied_timestamp))
            ifModifiedSince = flask.request.headers.get("If-Modified-Since", None)
            dtime = int(parsedate(ifModifiedSince).timestamp()) if ifModifiedSince is not None else None
            resp = None
            if dtime is not None and dtime <= int(last_modfied_timestamp):
                    ## print(" [TRACE] Return (304) status code, NOT modified")
                    resp = flask.Response(response= None, mimetype=mtype, content_type=mtype, status = 304) 
            else:
                ## print(" [TRACE] mtype = ", mtype)
                ## print(" [TRACE] sending file response = ", match)
                fd = match.open("rb")
                resp = flask.Response(response = fd, mimetype = mtype, content_type = mtype)
            # Enable cache and Cache never expires
            ## resp.headers.add("Cache-Control", "max-age")  
            # Disable cache 
            ## resp.headers.add("Cache-Control", "no-cache")  
            resp.headers.add("Content-Length",       match.stat().st_size)
            resp.headers.add("Last-Modified",        last_modified)
            resp.headers.add("vary",                 "Accept-Enconding")
            resp.headers.add("Content-Disposition", f"inline; filename={ match.name }")
        return resp 
        # Attempt to server static file 


    @app.get("/api/wiki") 
    @check_login()
    def api_wiki_pages():
        pages  = sorted([x.name.split(".md")[0] for  x in base_path.rglob("*.md")])
        resp  = flask.jsonify(pages)
        return resp 
        

    @app.route("/api/wiki/<path>", methods = [M_GET, M_POST, M_DELETE])
    @check_login()
    def api_wiki(path: str):
        mdfile_ = path + ".md"
        p: Optional[pathlib.Path] = next(base_path.rglob(mdfile_), None)
        user = current_user()
        if request.method == M_GET:
            if not p: flask.abort(404)
            content = p.read_text()
            out = flask.jsonify({ "status": "ok", "error": "", "content": content })
            return out
        elif request.method == M_POST:
            if not user.user_can_edit(): flask.abort(403)
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
            if not p: flask.abort(403)
            if not user.user_can_edit(): flask.abort(403)
            ## Remove file 
            p.unlink()
            out = flask.jsonify({ "status": "ok", "error": ""})
            return out
        else:
            flask.abort(405) 

    @app.route("/create/<path>", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_create(path: str):
        """Flask http route for creating new wiki pages/notes."""
        user = current_user()
        # Enforce authorization  
        if not user.user_can_edit():
            flask.abort(403)
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
    @check_login( required = True)
    def route_edit_page(path: str):
        user = current_user()
        # Enforce authorization  - Guest (Read-Only Users) and anonymous
        # users cannot edit the Wiki.
        if not user.user_can_edit():
            flask.abort(403)
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

    @app.get("/links/<path>") 
    @check_login()
    def route_link_page(path: str):
        """This endpoint displays all external hyperlinks of wiki page"""
        mdfile_ = path + ".md"
        ## line_start = utils.parse_int(request.args.get("start"))
        ## line_end   = utils.parse_int(request.args.get("end"))
        match = next(base_path.rglob(mdfile_), None)
        if not match:
            flask.abort(404) 
        # Absolute path to file
        abspath =  str(match.absolute())
        links = []
        internal_links = []
        ast = mparser.parse_file(abspath)
        gen = ast.walk()
        r = render.HtmlRenderer()
        while True:
            node = next(gen, None)
            ## breakpoint() 
            if node is None: break  
            elif node.type == "link": 
                label = node.children[0].content 
                url   = node.attrs.get("href")
                entry = {"label": label, "href": url}
                links.append(entry)
            elif node.type == "wikilink_inline":
                href = node.content
                internal_links.append(href)
        resp = flask.render_template("links.html"
                                       , title = f"Links of page: {path}"
                                       , page = path
                                       , links = links
                                       , internal_links = internal_links
                                       )
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

    return app


##def make_app_server(   host:        str
##                    , port:        int
##                    , debug:       bool
##                    , login:       Optional[Tuple[str, str]]
##                    , wikipath:    str
##                    , random_ssl:  bool = False
##                    , secret_key:  Optional[str] = None 
##                   ):
##    ##if random_ssl:
##    ##    with utils.TempSSLCert() as c:
##    ##        certfile, keyfile = c.certkey()
##    ##        assert os.path.exists(certfile)
##    ##        assert os.path.exists(keyfile)
##    ##        context = (certfile,  keyfile)
##    ##        ## context = ("cert.pem",  "key.pem")
##    ##        app.run(host = host, port = port, debug = debug, ssl_context = context)
##    ##else:
##        app.run(host = host, port = port, debug = debug)

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
        ## if not do_login:
        ##     return flask.redirect("/")
        ### breakpoint()
        path = utils.escape_url(request.args.get("path", "/"))
        if request.method == M_GET:
            if is_loggedin(): 
                ## breakpoint()
                return flask.redirect(path)
            else:
                return flask.render_template('login.html', path = path)
        assert request.method == M_POST
        _username = flask.request.form.get("username") or ""
        _password = flask.request.form.get("password") or ""
        print(f" [TRACE] _username = {_username} ; _password = {_password}")
        ##if _username == username and _password == password:
        ## breakpoint()
        if check_login_db(_username, _password): 
            do_login() 
            user = User.get_user_by_username(_username)
            session["user"] = user 
            return flask.redirect(path) 
        else:
            return flask.redirect(f"/login?path={path}")

    @app.route("/logoff")
    def loggof():
        do_logoff()
        session.clear()
        is_public = Settings.get_instance().public
        ## breakpoint()
        if is_public:
            path = request.args.get("path", "/")
            return flask.redirect(path)
        return flask.redirect("/login")

    def check_login(required = False):
        """Decorator that redirects to /login page if the user is not loggged in.
        The user is not asked to log in if the Wiki if the user is already authenticated
        or the wiki public. If the flag required is set to true, the user is asked to 
        log in regardless if the Wiki is public. Setting the flag required to true 
        is useful in pages where the user may modify data.
        """
        def login_checker(http_handler):
            def wrapper(*args, **kwargs):
                pass
                response = None
                is_public = Settings.get_instance().public
                ## breakpoint()
                loggedin = is_loggedin()
                if (is_public or loggedin) and (loggedin or not required):
                    response = http_handler(*args, **kwargs)
                else:
                    # Failed authentication / log in 
                    path = utils.escape_url(request.path)
                    response = flask.redirect(f"/login?path={path}") 
                    ## breakpoint()
                return response 
            wrapper.__name__ = http_handler.__name__
            return wrapper
        return login_checker
    return check_login

