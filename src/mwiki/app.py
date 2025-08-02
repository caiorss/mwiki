"""Flask app and database entry-point."""
import os
import re
import pathlib
import secrets
import urllib.parse
## from bottle import route, run
## from bottle import static_file, route, auth_basic, request
import flask 
import base64
from flask import Flask, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import flask_session
import flask_wtf as fwt 
from flask_wtf.csrf import CSRFProtect
import wtforms as wt 
import wtforms.validators as wtfv 

from typing import Any, Tuple, List, Optional
import datetime
import mwiki 
from . import utils
from . import mparser
from . import render
from . import search 
from . models import db, User, Settings, BookmarkedPage, WikiPage, WikiRepository
from . models import is_database_created
from . login import add_login
from . forms import UserAddForm, UserSettingsForm, SettingsForm
from . constants import *



session_folder = utils.project_cache_path(APPNAME, "session")
utils.mkdir(session_folder)

app = Flask(__name__) ##template_folder="templates")
# App.config['SESSION_TYPE'] = 'filesystem'
# App.config['SESSION_FILE_DIR'] = session_folder ## 'M:/code/flaskLoginTest/sessions'

app.config.update(  SESSION_SERVER_SIDE     = True  
                  , SESSION_TYPE            = "sqlalchemy"
                  , SESSION_COOKIE_NAME     =  os.getenv("MWIKI_SITENAME", "MWiki")
                  , SESSION_COOKIE_PATH     ='/'
                  # Protect against XSS (Script Injection)
                  , SESSION_COOKIE_HTTPONLY = True 
                  # Cookies are only served over HTTPS, not HTTP 
                  ##, SESSION_COOKIE_SECURE   = True 
                  , SESSION_PERMANENT       = True 
                  , SESSION_FILE_THRESHOLD = 1000  
                  , PERMANENT_SESSION_LIFETIME = datetime.timedelta(days = 30)
                 )


MWIKI_REPOSITORY_PATH = utils.expand_path(os.getenv("MWIKI_PATH", os.getcwd()))
dbpath = os.path.join(MWIKI_REPOSITORY_PATH, "database.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_SQLALCHEMY'] = db

## app.json = CustomJSONProvider(app)
## app.json_provider_class = CustomJSONProvider(app)

app.jinja_env.filters['encode_url'] = lambda u: urllib.parse.quote_plus(u) 
app.jinja_env.globals.update(config_sitename = lambda:  Settings.get_instance().sitename)
app.jinja_env.globals.update(config_description = lambda:  Settings.get_instance().description)
app.jinja_env.globals.update(config_show_source = lambda:  Settings.get_instance().show_source)
app.jinja_env.globals.update(config_main_font   = lambda:  Settings.get_instance().main_font)
app.jinja_env.globals.update(config_title_font   = lambda:  Settings.get_instance().title_font)
app.jinja_env.globals.update(config_vim_emulation = lambda:  Settings.get_instance().vim_emulation)

csrf = CSRFProtect(app)
csrf.init_app(app)
db.init_app(app)
## session = flask_session.Session(app)

def current_user() -> User:
    """Get user logged in to the server."""
    obj  = session.get("user") 
    if obj is None or not isinstance(obj, dict) or  obj.get("__class") != "User": 
        user = User(  username = "anonymous"
                    , password = "dummy"
                    , type = USER_ANONYMOUS)
        return user 
    user = User(  id = obj.get("id")
                , username = obj.get("username")
                , email = obj.get("email")
                , type = obj.get("type")
                , active = True 
              )
    return user 

def display_edit_buttons() -> bool:
    user = current_user()
    conf = Settings.get_instance()
    out =  conf.display_edit_button or user.is_admin()
    return out

app.jinja_env.globals.update(current_user = current_user)
app.jinja_env.globals.update(display_edit_buttons = display_edit_buttons)



# --- Database Initialization -----#
# Create all database tables if they don't exist yet.
with app.app_context():
    user = None 
    created = is_database_created()
    ## Evironment variables which allows defining 
    ## container configuration during initialization.
    ADMIN_PASSWORD = os.getenv("MWIKI_ADMIN_PASSWORD")
    SITE_NAME = os.getenv("MWIKI_SITENAME", "MWiki")
    PUBLIC = os.getenv("MWIKI_PUBLIC", False) != False
    if not created: 
        ##print(" [TRACE] Admin user created OK")
        user = User( username = "admin", type = USER_MASTER_ADMIN )
        # Useful for installation with Docker
        user.set_password(ADMIN_PASSWORD)
    db.create_all()
    conf = Settings.get_instance()
    conf.sitename = SITE_NAME
    conf.public = PUBLIC 
    db.session.add(conf)
    db.session.commit()
    if not created:
        db.session.add(user)
        db.session.commit()
    admin = User.get_user_by_username("admin")    
    if admin.password is None:
        password = conf.default_password
        ##print(f" [INFO] Enter the username: {admin.username} and password: '{password}' to log in.")
