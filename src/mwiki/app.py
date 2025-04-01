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
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = session_folder ## 'M:/code/flaskLoginTest/sessions'
# Set the maximum number of stored sessions
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days = 30)
app.config['SESSION_FILE_THRESHOLD'] = 1000  # Adjust the limit as needed
# Configure Flask to use FileSystemSessionInterface with the custom options
app.config["SESSION_PERMANENT"] = True

MWIKI_REPOSITORY_PATH = utils.expand_path(os.getenv("MWIKI_PATH", os.getcwd()))
dbpath = os.path.join(MWIKI_REPOSITORY_PATH, "database.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbpath}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.filters['encode_url'] = lambda u: urllib.parse.quote_plus(u) 
app.jinja_env.globals.update(config_sitename = lambda:  Settings.get_instance().sitename)

db.init_app(app)

def current_user():
    """Get user logged in to the server."""
    user: User = session.get("user") or User( username = "anonymous"
                                            , password = "dummy"
                                            , type = USER_ANONYMOUS)
    return user 

app.jinja_env.globals.update(current_user = current_user)



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
