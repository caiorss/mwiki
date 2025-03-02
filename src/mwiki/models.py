from typing import Any, Tuple, List, Optional
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy as sa 
import sqlalchemy
from sqlalchemy import ForeignKey
import sqlalchemy.orm as so 
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import yaml.scanner
from . import utils
from . constants import *
from . import render 
from . import mparser
import pathlib
import frontmatter
import yaml
import flask

## db = SQLAlchemy(app)
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    username: so.Mapped[str] = so.mapped_column(index=True, nullable=False, unique=True)
    email:    so.Mapped[str] = so.mapped_column(nullable=True, unique=True)
    ## TODO IT should be stored only the password hash, never the password in plain text
    password: so.Mapped[str] = so.mapped_column(sqlalchemy.String(256), nullable= True)
    description: so.Mapped[str] = so.mapped_column(sqlalchemy.String(5000), nullable= True, default = "")
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


class WikiPage():
    """Model class representing a wiki page markdown file."""

    def __init__(self, base_path: pathlib.Path, path: pathlib.Path, title: str):
        self._base_path = base_path
        self._title = title 
    
    def path(self):
        """Get path of Wiki page file"""
        p = next(self._base_path.rglob(self._title + ".md"), None)
        return p

    def read(self) -> str:
        """Get markdown content of wiki page file."""
        path = self.path()
        text = path.read_text()
        return text 

    def write(self, text: str) -> None:
        """Update markdown content of wiki page file"""
        path = self.path()
        path.write_text(text)

    def render_html(self, latex_macros = "") -> str:
        """Render MWiki page to html"""
        text = self.read()
        headings = mparser.get_headings(text)
        root = mparser.make_headings_hierarchy(headings)
        toc = mparser.headings_to_html(root)
        pagefile = str(self.path())
        base_path = str(self._base_path)
        content = render.pagefile_to_html(pagefile, base_path)
        html = flask.render_template(  "content.html"
                                             , title   = self._title 
                                             , page    = self._title
                                             , content = content
                                             , toc     = toc
                                             , latex_macros = latex_macros)
        return html

    def frontmatter(self):
        """Return wikipage metadata"""
        out = {  "title":   ""
               , "subject": ""
               , "keywords": ""
               , "uuid": ""
               , "label": ""
               }
        parser = frontmatter.Frontmatter()
        try:
            path = str(self.path())
            data = parser.read_file(path)
            data = data.get("attributes")
        except yaml.scanner.ScannerError as err:
            pass
        return out


class WikiRepository():
    
    def __init__(self, wikipath: str):
        self._wikipath = wikipath
        self._base_path =  pathlib.Path(wikipath)

    def find_page(self, title: str) -> Optional[pathlib.Path]:
        """Get path to Wiki page"""
        mdfile = title  + ".md" 
        result = next(self._base_path.rglob(mdfile), None)
        return result 

    def get_wiki_page(self, title: str) -> Optional[WikiPage]:
        path = self.find_page(title)
        if path is None: 
            return None 
        wikipage = WikiPage(base_path = self._base_path, path = path, title = title)
        return wikipage
        




