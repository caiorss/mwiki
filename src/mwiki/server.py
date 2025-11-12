"""Http Routes"""
import io
import os
import json
import re
import pathlib
import secrets
import time
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
import base64
from flask import request, session
from werkzeug.security import generate_password_hash
from PIL import Image
import flask_session

from typing import Any, Tuple, List, Optional
import datetime
import mimetypes
from dateutil.parser import parse as parsedate
import mwiki 
from . import utils
from . import mparser
from . import render
from . import search 
import mwiki.models as models
from . models import db, User, Settings, BookmarkedPage, WikiPage, WikiRepository, MwikiConfig
from . login import add_login
from . forms import UserAddForm, UserSettingsForm, SettingsForm
from . constants import ( M_GET, M_POST, M_DELETE
                        , STATUS_CODE_400_BAD_REQUEST, STATUS_CODE_401_UNAUTHORIZED
                        , STATUS_CODE_403_FORBIDDEN,   STATUS_CODE_404_NOT_FOUND
                        , STATUS_CODE_405_METHOD_NOT_ALLOWED
                        )
from .app import app, current_user

# This variable is set to true if gunicorn WSGI server is being used.
server_software =  os.environ.get("SERVER_SOFTWARE", "")
is_wsgi = "gunicorn" in server_software or "waitress" in server_software


 
def make_app_server(  host:        str
                    , port:        int
                    , debug:       bool
                    , login:       Optional[Tuple[str, str]]
                    , wikipath:    str
                    , random_ssl:  bool = False
                    , secret_key:  Optional[str] = None 
                   ):
    secret_key = models.get_secret_key()
    app.config["SECRET_KEY"] = secret_key
    ##secret_key = get_secret_key(APPNAME) if secret_key is None else secret_key
    # Specify a custom directory for storing session files
    ### app.config['SECRET_KEY'] = secret_key
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
    repository = WikiRepository(wikipath, debug = MwikiConfig.debug)


    @app.route("/user", methods = [M_GET, M_POST])
    @check_login( required = True )
    def route_user_settings():
        """Panel for updating user account settings.""" 
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
        """Form for creating new user accounts."""
        user = current_user()
        if not user.is_admin():
            flask.abort(STATUS_CODE_403_FORBIDDEN)
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
            flask.flash("User created successfully. Ok.")
            app.logger.info("User created ok.")
            return flask.redirect("/account/new")
        resp  = flask.render_template("add_user.html", form = form, title = "Add User")
        return resp

    @app.route("/settings", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_settings():
        """Form for changing wiki settings."""
        user = current_user()
        if not user.is_admin():
            flask.abort(403)
        form = SettingsForm()
        resp = None
        conf = Settings.get_instance()
        if request.method == M_GET:
            form.sitename.data = conf.sitename
            form.public.data = conf.public
            form.show_source.data = conf.show_source
            form.display_edit_button.data  = conf.display_edit_button   
            form.vim_emulation.data  = conf.vim_emulation
            form.description.data = conf.description   
            form.main_font.data = conf.main_font
            form.title_font.data = conf.title_font
            form.code_font.data = conf.code_font
            form.show_licenses.data = conf.show_licenses
            form.default_locale.data = conf.default_locale
            form.use_default_locale.data = conf.use_default_locale
            form.use_cdn.data = conf.use_cdn
            form.latex_renderer.data = conf.latex_renderer
        if request.method == M_POST:
            form.validate()
            app.logger.info(f"Form data = {form.data}")    
            conf.sitename = form.sitename.data
            conf.description = form.description.data
            conf.public = form.public.data 
            conf.show_source = form.show_source.data
            conf.main_font = form.main_font.data
            conf.title_font = form.title_font.data
            conf.code_font = form.code_font.data 
            conf.display_edit_button = form.display_edit_button.data
            conf.vim_emulation = form.vim_emulation.data
            conf.show_licenses = form.show_licenses.data 
            conf.default_locale = form.default_locale.data
            conf.use_default_locale = form.use_default_locale.data
            conf.use_cdn = form.use_cdn.data
            conf.latex_renderer = form.latex_renderer.data 
            conf.save()
            flask.flash('<span data-i18n="settings-page-successful-update-message">Wiki settings updated successfully.</span>')
            app.logger.info("Wiki setting updated.")
            flask.redirect("/settings")
        page_title_i18n_tag = "settings-page-title"
        resp  = flask.render_template(	  "settings.html"
										, form = form
										, title = "Wiki Settings"
										, page_title_i18n_tag = page_title_i18n_tag
										)
        return resp

    ##@auth_basic(is_authhenticated)
    @app.route("/pages", methods = [M_GET])
    @check_login()
    def route_pages():
        """Allows searching or browsing all wiki pages.

        This page provides a form search where users can look 
        for keywords in all wiki page files (markdown files).
        """
        query = (request.args.get("search") or "").strip()
        # Possibliity: ?sort=modified, ?sort=name, ?sort=created
        sort  = request.args.get("sort", "")
        # Get all pages in directories and subdirectories in a recursively way
        files_ = pathlib.Path(BASE_PATH).rglob("*.md")
        files = []
        if query == "":
            files = [(f, 1) for f in files_ ]
        else:
            DUMMY_VALUE = 10
            files = [(f, DUMMY_VALUE) for f in search.search_text(pathlib.Path(BASE_PATH), query)]
                     ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
        sorted_files = []
        if sort == "" or sort == "score":
            sorted_files = files  # sorted(files, key = lambda x: x[1], reverse = True)
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
                      , "link": f.name.split(".")[0].replace(" ", "_")

                      , "matches": [ lin[:MAX_LEN] + " ..." 
                                    if len(lin) > MAX_LEN else lin  
                                        for (n, lin) in  search.grep_file(page_to_file(f), query)  ] \
                                    if query != "" else [ ]

                      , "metadata": mparser.get_pagefile_metadata( page_to_file(f))
                   } 
                 for f in sorted_files ]
        ##title = f"Search results for \"{query}\"" if query != "" else "All pages"
        
        # [i18n] in English: 'Search results for"
        title = f"[i18n] \"{query}\"" if query != "" else "All pages"
        page_title_i18n_tag = "title-search-results-page" \
			if query != "" else "title-listing-all-pages"
        response = flask.render_template( "listing.html"
                                         , title = title
										 , page_title_i18n_tag = page_title_i18n_tag
                                         , pages = pages
                                         , size  = len(pages)
                                         , query = query
                                         )
        return response

   ## print(" [TRACE] running gunicorn = ", is_gunicorn)
    ## print(" [TRACE] server sofware   = ", server_software)


    @app.get("/about")
    def route_about():
        """Show about page."""
        resp = flask.render_template( "about.html"
									 , page_title_i18n_tag = "about-page-title"
                                     , title = "[i18n] " + Settings.get_instance().sitename )
        return resp

    @app.get("/licenses")
    def route_licenses():
        """Serve page showing open source licenses of dependencies used in this project."""
        conf = Settings.get_instance()
        if not conf.show_licenses:
            flask.abort(STATUS_CODE_404_NOT_FOUND)
        resp = flask.render_template("licenses.html", title="Open Source Licenses")
        return resp

    @app.get("/wiki/img/<path:filepath>")
    @check_login()
    def route_wiki_image(filepath):
        print(" [TRACE] path = ", filepath)
        root = IMAGE_PATH ## utils.get_wiki_path("images")
        ## print(" [TRACE] root = ", root)
        resp = flask.send_from_directory(root, filepath)
        return resp

    @app.route("/wiki/math/<file>")
    def route_wiki_math(file):
        """Server cached SVG image of compiled LaTeX equation."""
        resp = flask.send_from_directory(render.svg_cache_folder, file)    
        return resp

    rpat = re.compile(r"!\[(.*?)\]\(data:image/(.+?);base64,(.*?)\)")

    def replacement_(m: re.Match) -> str:
        img = m.group(3)[:200] + "..."
        out = f"![{m.group(1)}](data:image/{m.group(2)};base64,{img})"
        return out

    @app.route("/source/<path>")
    @check_login( required = False)
    def route_wiki_source(path):
        """Serve source code of wiki page."""
        conf = Settings.get_instance()
        # Only show source code of Wiki page if it is enabled
        # in the URL endpoint /settings forms.
        if not conf.show_source:
            flask.abort(STATUS_CODE_401_UNAUTHORIZED)
        page = repository.get_wiki_page(path)
        if not page: flask.abort(STATUS_CODE_404_NOT_FOUND)
        src = page.read()
        src = re.sub(rpat, replacement_, src)
        ## src = utils.escape_html(src)
        content = utils.highlight_code(src, "markdown")
        ## content = f"<pre>\n{src}\n</pre>" 
        ## html = mparser.fill_template(f"Source of '{page}.md'", content, toc = "", query = "")
        html = flask.render_template("source.html"
                                     , page = path 
                                     , title = f"[i18n]: {path}"
                                     , page_title_i18n_tag = "source-page-title"
                                     , content = content)
        return html

    ## Latex Macros to be Injected in Page Template
    latex_macros = utils.read_resource(mwiki, "macros.sty")

    base_path = pathlib.Path(BASE_PATH)
    tags_cache_file = base_path.joinpath(".data/tags_cache.json")


    @app.route("/wiki/<path>")
    @check_login()
    def route_wiki_page(path: str):
        """Return rendered wiki pages as html or server files upload by user"""
        # path does not have exntension, it is just the name
        # of the mdfile without any extension
        if "." not in path:
            path_ = path
            path = path.replace("_", " ")
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
            # The files  'Cloud Computing.md' abd 'Cloud_Computing.md'
            # are regarded as the same file, consequentely the wiki pages 'Cloud Computing'
            # and 'Cloud_Computing' are also regarded as the wiki page (note). This approach
            # improves compatibility with Wikis or note taking applications  that use underline
            # in file name and Wikis that use space in the file name.
            conf: Settings = Settings.get_instance()
            page = repository.get_wiki_page(title = path, latex_renderer = conf.latex_renderer) \
                    or repository.get_wiki_page(title = path_, latex_renderer = conf.latex_renderer)
            ## print(" [TRACE] matches = ", matches)
            # ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
            if not page:
                ## flask.abort(404) 
                out = flask.redirect(f"/create/{path}")
                return out
            html = page.render_html()
            return html
            # print(" [TRACE] path_ = ", path_)
            ##out = serve_static_file(base_path, path_)
            return out 
        # Dont' show source code of markdown file
        if path.endswith(".md"):
            flask.abort(STATUS_CODE_404_NOT_FOUND)
        out = serve_static_file(base_path, path)
        return out 
            
    @app.get("/api/wiki") 
    @check_login()
    def api_wiki_pages():
        """API endpoint that shows list of all wiki pages."""
        pages  = sorted([x.name.split(".md")[0] for  x in base_path.rglob("*.md")])
        resp  = flask.jsonify(pages)
        return resp 
        

    @app.route("/api/wiki/<path>", methods = [M_GET, M_POST, M_DELETE])
    @check_login()
    def api_wiki(path: str):
        """API endpoint for editing, saving or deleting wiki pages."""
        mdfile_ = path + ".md"
        p: Optional[pathlib.Path] = next(base_path.rglob(mdfile_), None)
        user = current_user()
        if request.method == M_GET:
            if not p:
                flask.abort(STATUS_CODE_404_NOT_FOUND)
                return 
            content = p.read_text() 
            out = flask.jsonify({ "status": "ok", "error": "", "content": content })
            return out
        elif request.method == M_POST:
            if not user.user_can_edit(): flask.abort(STATUS_CODE_403_FORBIDDEN)
            out = ""
            ## breakpoint()
            if p: 
                out = flask.jsonify({ "status": "error", "error": "File already exists"})
            else: 
                p_ = base_path.joinpath(mdfile_)
                p_.touch()    
                out = flask.jsonify({ "status": "ok", "error": ""})
            return out
        elif request.method == M_DELETE:
            if not p:
                flask.abort(STATUS_CODE_404_NOT_FOUND)
                return out 
            if not user.user_can_edit():
                flask.abort(STATUS_CODE_403_FORBIDDEN)
                return out 
            ## Remove file 
            p.unlink()
            search.index_delete_page(base_path, p)
            out = flask.jsonify({ "status": "ok", "error": ""})
            return out
        else:
            flask.abort(STATUS_CODE_405_METHOD_NOT_ALLOWED) 

    @app.route("/api/auth", methods = [M_GET])
    def api_auth():
        user = current_user()
        conf = Settings.get_instance()
        data = {    "is_admin": user.is_admin()
                  , "is_authenticated": user.is_authenticated()
                  , "is_anonymous": user.is_anonymous()
                  , "type": user.type
                  , "active": user.active or False
                  , "username": user.username
                  , "show_buttons": conf.display_edit_button or user.is_admin()
                  }
        out = flask.jsonify(data)
        return out

    @app.route("/create/<path>", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_create(path: str):
        """Http endpoint for creating new wiki pages/notes."""
        user = current_user()
        # Enforce authorization  
        if not user.user_can_edit():
            flask.abort(STATUS_CODE_403_FORBIDDEN)
        mdfile_ = path + ".md"
        p: Optional[pathlib.Path] = next(base_path.rglob(mdfile_), None)
        out = None 
        if p:
            out = flask.redirect(f"/wiki/{path}")
            return out
        if request.method == M_GET:
            out = flask.render_template("create.html"
                                        , page_title_i18n_tag = "creating-page-title"
                                        ,  title = f"[i18n] '{path}'", pagename = path)
        elif request.method == M_POST:
            ## _page        = flask.request.form.get("page", "") 
            label       = flask.request.form.get("label", "") 
            description = flask.request.form.get("description", "") 
            keywords    = flask.request.form.get("keywords", "") 
            submit_yes  = flask.request.form.get("submit-yes")
            ##submit_no   = flask.request.form.get("submit-no", "") 
            ## breakpoint()
            if submit_yes is not None:
                content = (   "---"
                             f"\ntitle:       {path}"
                             f"\nlabel:       {label}"
                             f"\ndescription: {description}"
                             f"\nkeywords:    {keywords}"
                             "\n---\n\n"
                          )
                page_path = base_path.joinpath(path + ".md")
                page_path.write_text(content)
                search.add_index_page(base_path, page_path)
                out = flask.redirect(f"/wiki/{path}")
            else:
                out = flask.redirect("/")
        else:
            flask.abort(405)
        return out

    @app.route("/edit/<path>", methods = [M_GET, M_POST])
    @check_login( required = True)
    def route_edit_page(path: str):
        """Servers Wiki code editor (Ace 9) JavaScript editor."""
        path = path.replace("_", " ")
        user = current_user()
        # Enforce authorization  - Guest (Read-Only Users) and anonymous
        # users cannot edit the Wiki.
        if not user.user_can_edit():
            flask.abort(STATUS_CODE_401_UNAUTHORIZED)
        if path == "special:macros":
            # Enforece - authorization - only admin can edit macros.
            if not user.is_admin():
                flask.abort(STATUS_CODE_401_UNAUTHORIZED)
            macro_file = (base_path / "macros.sty").resolve()
            content = ""
            if request.method == M_GET:
                if not macro_file.is_file():
                    default_content = utils.read_resource(mwiki, "macros.sty")
                    macro_file.write_text( default_content )
                content = macro_file.read_text()
                resp = flask.render_template(  "edit.html"
                                             , title = f"[i18n]: {path}"
                                             # Eglish title: "Editing: <WikiPageName>"
                                             , page_title_i18n_tag = "edit-page-title"
                                             , page = path
                                             , page_link = path.replace(" ", "_")
                                             , content = content)
                return resp 
            elif request.method == M_POST:
                data: dict[str, Any] = request.get_json()
                content = data.get("content", "") 
                macro_file.write_text(content)
                resp = flask.jsonify({ "status": "ok", "error": "" })
                return resp
            else:
                raise RuntimeError("Impossible branch")
        line_start = utils.parse_int(request.args.get("start"))
        line_end   = utils.parse_int(request.args.get("end"))
        timestamp  = utils.parse_int(request.args.get("timestamp"))
        page = repository.get_wiki_page(title = path)
        if not page:
            flask.abort(STATUS_CODE_404_NOT_FOUND)
        ## match = next(base_path.rglob(mdfile_), None)
        if request.method == M_GET:
            if timestamp is None or timestamp < page.timestamp:
                return flask.redirect("/wiki/" + path.replace(" ", "_"))
            ## content = match.read_text() 
            content = page.read()
            ## breakpoint()
            if line_start is not None:
                lines = content.splitlines()
                content = "\n".join(lines[line_start:line_end]) 
            ## print(" [TRACE] content = ", content)
            resp = flask.render_template(  "edit.html"
                                         , title = f"[i18n]: {path}"
                                         # Eglish title: "Editing: <WikiPageName>"
                                         , page_title_i18n_tag = "edit-page-title"
                                         , page = path
                                         , page_link = path.replace(" ", "_")
                                         , content = content)
            return resp
        assert request.method == M_POST
        # Simulate a delay of 5 seconds
        data: dict[str, Any] = request.get_json()
        content = data.get("content", "") 
        out = {}
        if not page:
            out = { "status": "error", "error": "Page not found." }
        elif not isinstance(content, str):
            out = { "status": "error", "error": "Invalid input. Expected text. " }
        else:
            ## lines = content.splitlines()
            if line_start is None:
                ## match.write_text(content)
                page.write(content)
            else:
                ## breakpoint()
                text = ""
                ## content_ = match.read_text() 
                content_ = page.read()
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
                ## match.write_text(text)                    
                page.write(text)
            # Update search index
            # NOTE: The search index is updated by the module mwiki.watcher outside the
            # request-response cycle. The module watcher detects files changed in the data repository
            # and updates the search index.
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
            flask.abort(STATUS_CODE_404_NOT_FOUND) 
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
                                       , title = f"[i18n] {path}"
                                       , page_title_i18n_tag = "links-page-title"
                                       , page = path
                                       , links = links
                                       , internal_links = internal_links
                                       )
        return resp

    @app.route("/tags")
    @check_login()
    def route_tags():
        """URL endpoint /tags for browsing all wiki tags.
        """
        tags = []
        ## print(" [TRACE] tags_cache_file = ", tags_cache_file)
        if tags_cache_file.exists():
            with open(tags_cache_file) as fd:
                data = json.load(fd)
                tags = data.get("tags") or []
        resp = flask.render_template("tags.html", title = "Tags", tags = tags)
        return resp 

    @app.route("/api/preview", methods = [M_POST])
    @check_login(required = True)
    def route_preview():   
        """Provide document preview"""
        data: dict[str, Any] = request.get_json()
        content = data.get("code", "") 
        ### content = utils.read_resource(mwiki, "refcard.md")
        ast = mparser.parse_source(content)
        builder = render.HtmlRenderer(base_path=BASE_PATH, preview = True)
        html_ = builder.render(ast)
        html = flask.render_template(  
                                          "standalone.html"
                                        , title   = "Preview"
                                        , page    = data.get("page")
                                        , content = html_
                                        , latex_macros = latex_macros
                                        , document_type = "preview"
                                        )
        html = utils.escape_html(html)
        # print(" [TRACE] html = ", html)
        resp = flask.jsonify({ "status": "ok", "error": "", "html": html })
        return resp 

    @app.route("/paste", methods = [M_GET, M_POST])
    @check_login(required = True)
    def route_paste():
        """URL endpoint API /paste 
        for uploading images to the wiki by pasting images from the clipboard.
        """
        user = current_user()
        # Enforce authorization  - Guest (Read-Only Users) and anonymous
        # users cannot edit the Wiki.
        if user.is_anonymous():
            flask.abort(STATUS_CODE_401_UNAUTHORIZED)
        if not user.user_can_edit():
            flask.abort(STATUS_CODE_403_FORBIDDEN)
            return 
        payload: dict[str, Any] = request.get_json()
        if not "fileName" in payload.keys() or "data" not in payload.keys():
            flask.abort(STATUS_CODE_400_BAD_REQUEST)
            return 
        fileName = payload["fileName"]
        data = payload["data"]
        if fileName is None or data is None:
            flask.abort(STATUS_CODE_400_BAD_REQUEST)
            return 
        b64data_ = data.split(",")
        if len(b64data_) != 2 or fileName == "":
            flask.abort(STATUS_CODE_400_BAD_REQUEST)
        blob: bytes = base64.b64decode(b64data_[1])
        png_image = Image.open(io.BytesIO(blob))
        jpeg_image = png_image.convert('RGB')
        ### breakpoint()
        image_path = pathlib.Path(wikipath).joinpath("pasted")
        utils.mkdir(str(image_path))
        path = image_path.joinpath(fileName)
        if path.exists():
            flask.abort(STATUS_CODE_400_BAD_REQUEST)
        ## path.write_bytes(blob)
        path_ = str(path)
        ### print(" [TRACE] path_ = ", path_)
        jpeg_image.save(path_, "JPEG")
        response = flask.jsonify({"error": False, "status": "ok"})
        return response 

    
    @app.route("/api/upload", methods = [M_POST, M_GET, "OPTIONS"])
    @check_login( required = True)
    def route_upload():
        # Enforce authorization  - Guest (Read-Only Users) 
        # and anonymous users cannot edit the Wiki.
        user = current_user()
        if user.is_anonymous():
            flask.abort(STATUS_CODE_401_UNAUTHORIZED)
        if not user.user_can_edit():
            flask.abort(STATUS_CODE_403_FORBIDDEN)
        afile = request.files.get('file')
        ## breakpoint()
        if afile is None:
            flask.abort(STATUS_CODE_400_BAD_REQUEST)        
        upload_dir = pathlib.Path(wikipath).joinpath("upload")
        utils.mkdir(str(upload_dir))
        file_ = request.form.get("fileLabel") or afile.filename
        _, extension = os.path.splitext(afile.filename)
        filename = utils.slugify(file_) + extension
        path = upload_dir.joinpath(filename)
        if path.exists():
            out = flask.jsonify({ "status": "ok", "error": "", "file": filename})
            return out 
        afile.save(path)
        out = flask.jsonify({ "status": "ok", "error": "", "file": filename})
        return out

    @app.route("/auth", methods = [M_POST, M_GET])
    def route_auth():
        """Passwordless authentication using token in a similar way to Jupyter Lab

        The authentication token, that is valid for 1 minute, can
        be generated with the command:

        $ mwiki auth --user=admin --wikipath=/path/to/markdown-files-repository
        """
        token = ""
        if request.method == M_GET:
            token = request.args.get("token", "")
        elif request.method == M_POST:
            token =  flask.request.form.get("token") or ""
        else:
            # THis line should never be executed.
            raise RuntimeError("Invalid state.")
        path = request.args.get("path", "/")
        data = utils.decode_json_from_base64(token) or {}
        user      = data.get("user", "")
        salt      = data.get("salt", "")
        timestamp = data.get("expiration", 0)
        signature = data.get("signature", "")
        message = user + "/" + str(timestamp) + "/" + str(salt)
        # print(" [TRACE] message = ", message)
        signature_is_valid = utils.hmac_compare(secret_key, message, signature)
        not_expired = not utils.timestamp_has_expired(timestamp)
        user_ = User.get_user_by_username(user)
        if signature_is_valid and not_expired and user_ is not None:
            session["user"] = user_.to_Dict()
            session["loggedin"] = True
        return flask.redirect(path)

    @app.get("/")
    def route_index_page():
        """Server index page '/'"""
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

def serve_static_file(base_path: pathlib.Path, path):
    # Seach file in any directory in basepath recursively 
    # In the future this code can be optimized using some sort 
    # of caching or search index for speeding up 
    # the response.
    ## print(" [TRACE] filePath (528) = ", path)
    # breakpoint()
    match: Optional[pathlib.Path] = None 
    BASE_PATH = str(base_path)
    if isinstance(path, pathlib.Path):
        match = path
    else:
        g = base_path.rglob(path) 
        match: Optional[pathlib.Path] = next(g, None)
        if not match:
            flask.abort(404)
    relpath = match.relative_to(base_path)
    name = relpath.name 
    # DO NOT server the sqlite database or the .data and other hidden directories
    if name == "database.sqlite" or name.startswith(".data") or name.startswith("."):
        flask.abort(STATUS_CODE_404_NOT_FOUND)
    ## print(f" [TRACE] relpath = {path} ; match = {match}")
    resp = None
    ###  Render org-mode file 
    if name.endswith(".org"):
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
    if not is_wsgi:
        resp = flask.send_from_directory(BASE_PATH, relpath)
    else:
        ##print(" [TRACE] Enter line 798 - wsgi static file serving => match.name = ", match.name)
        #if match.name.endswith(".html"):
        #    breakpoint()
        ## Get file mime type
        mtype, _ = mimetypes.guess_type(match.name, strict = False)
        mtype = mtype or "application/octect-stream"
        ## breakpoint()
        if os.getenv("MWIKI_X_ACCEL_REDIRECT"):
            resp = flask.Response(response = None, status = 200)
            resp.headers.add("X-Accel-Redirect", relpath)
            resp.headers.add("Content-Type", mtype)
            return resp 
        ## Get last modified time (formatted as string)
        pattern  = "%a, %d %b %Y %H:%M:%S %Z"
        #last_modfied_timestamp = match.stat().st_mtime
        last_modified_time =  datetime.datetime.fromtimestamp(match.stat().st_mtime, tz = datetime.timezone.utc).timestamp()
        last_modified_str       = time.strftime(pattern, time.gmtime(last_modified_time))
        ifModifiedSince = flask.request.headers.get("If-Modified-Since", None)
        dtime = int(parsedate(ifModifiedSince).timestamp()) if ifModifiedSince is not None else None
        resp = None
        if dtime is not None and dtime >= last_modified_time:
                ## print(" [TRACE] Return (304) status code, NOT modified")
                resp = flask.Response(  response= None
                                      , mimetype=mtype
                                      , content_type=mtype
                                      , status = 304
                                      ) 
        else:
            ## print(" [TRACE] mtype = ", mtype)
            ## print(" [TRACE] sending file response = ", match)
            fd = match.open("rb")
            resp = flask.Response(response = fd, mimetype = mtype, content_type = mtype)
        # Enable cache and Cache never expires
        ## resp.headers.add("Cache-Control", "max-age")  
        # Disable cache 
        ## resp.headers.add("Cache-Control", "no-cache")  
        resp.headers.add("Content-Type", mtype)
        resp.headers.add("Content-Length",       match.stat().st_size)
        resp.headers.add("Last-Modified",        last_modified_str )
        resp.headers.add("vary",                 "Accept-Enconding")
        resp.headers.add("Content-Disposition", f"inline; filename={ match.name }")
    return resp

def get_secret_key_(appname: str) -> str:
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
