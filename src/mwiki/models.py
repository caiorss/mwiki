from typing import Any, Tuple, List, Optional
import os
import enum 
import json
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

CACHE_FILE_FORMAT_VERSION = "0.1"

class Config:
    """Singletion containg wiki settings

    NOTE: Instances of this class should only be modified
    during the application initialization.
    """
    def __init__(self):
        self._path: str = os.environ.get("MWIKI_PATH", ".")
        self._debug: bool = False
        self._host: str = os.environ.get("MWIKI_HOST", "0.0.0.0")
        self._port: int = utils.parse_int(os.getenv("MWIKI_PORT", "8000")) or 8000

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def port(self) -> int:
        return self._port

    @property
    def host(self) -> str:
        """Returns the host IP address that the server will listen for.
        The default host is 0.0.0.0 (Listen to all network interfaces)
        """
        return self._host

    @property
    def path(self) -> str:
        return self._path

    def enable_debug(self):
        self._debug = True

    def set_path(self, path_: str):
        self._path = path_

MwikiConfig = Config()


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

    def set_password(self, password: Optional[str]) -> None:
        if password is None: return
        password_hash = generate_password_hash(password)
        self.password = password_hash

    def check_password(self, password: str) -> bool:
        out =  check_password_hash(self.password, password)
        ## print(" [TRACE] password = ", password)
        return out

    def __repr__(self):
        return f"User{{ id = {self.id} ; username = {self.username}  ; type = {self.type} }}"

    def to_Dict(self):
        obj = {
              "__class":   "User"
            , "id":        self.id
            , "username":  self.username
            , "email":     self.email
            , "type":      self.type
        }
        return obj

    @classmethod
    def get_user_by_username(self, username: str) -> Optional['User']:
        query = sqlalchemy.select(User).where(User.username.like(username))
        result = db.session.execute(query).scalars().first()
        return result

class FontFamiliyEnum(enum.Enum):
    # Default LaTeX font created by professor Donald Knuth
    computer_modern = "Computer Modern"
    crimson = "Crimson"
    comorant_light = "Comorant Light"
    literata = "Literata"
    # Serif typeface font designed for google books.
    literata_variable = "Literata Variable"
    garamond_pro_regular = "Garamond Pro Regular"
    neo_euler = "Neo Euler"
    # IBM old-chool monospace that gives back the 
    # nolstagic feeling of typewriters.
    ibm_plex_mono = "IBM Plex Mono"
    go_mono = "GO Mono"
    logic_monospace_regular = "Logic Monospace Regular"
    logic_monospace_medium  = "Logic Monospace Medium"
    commit_mono = "Commit Mono"
    julia_mono = "Julia Mono"
    julia_mono_light = "Julia Mono Light"
    libertinus_mono = "Libertinus Mono"
    libertinus_sans = "Libertinus Sans"
    libertinus_serif = "Libertinus Serif"
    range_font = "Range"
    range_mono = "Range Mono"
    bricolage_grotesque = "Bricolage Grotesque"
    textura_modern = "Textura Modern"
    bastarda = "Bastarda"


class CodeFontFamily(enum.Enum):
    """Font families for code (source code). They must be monospace typefaces."""
    ibm_plex_mono = "IBM Plex Mono"
    go_mono = "GO Mono"
    logic_monospace_regular = "Logic Monospace Regular"
    logic_monospace_medium  = "Logic Monospace Medium"
    commit_mono = "Commit Mono"
    libertinus_mono = "Libertinus Mono"
    julia_mono = "Julia Mono"
    julia_mono_light = "Julia Mono Light"
    range_mono = "Range Mono"


class TitleFontFamily(enum.Enum):
    # Default LaTeX font created by professor Donald Knuth
    computer_modern = "Computer Modern"
    neo_euler = "Neo Euler"
    crimson = "Crimson"
    chicago_macos_system6 = "Chicago MacOS"
    garamond_pro_regular = "Garamond Pro Regular"
    # IBM old-chool monospace that gives back the nolstagic
    # feeling of the typewriter 
    ibm_plex_mono = "IBM Plex Mono"
    go_mono = "GO Mono"
    # Font suitable for title
    news_reader = "NewsReader"
    literata = "Literata"
    literata_variable = "Literata Variable"
    textura_modern = "Textura Modern"
    bastarda = "Bastarda"
    logic_monospace_regular = "Logic Monospace Regular"
    logic_monospace_medium  = "Logic Monospace Medium"
    commit_mono = "Commit Mono"
    julia_mono = "Julia Mono"
    julia_mono_light = "Julia Mono Light"
    libertinus_mono = "Libertinus Mono"
    libertinus_sans = "Libertinus Sans"
    libertinus_serif = "Libertinus Serif"
    libertinus_serif_display = "Libertinus Serif Display"
    range_mono = "Range Mono"
    range_font = "Range"
    bricolage_grotesque = "Bricolage Grotesque"
    graphik_regular_web = "Graphik Regular"

class Settings(db.Model):
    """Singleton model class (SQL table) containing site settings.
    """
    __tablename__ = "settings"
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    # Public => Indicates whether the wiki can be viewed (not edited) by everybody.
    public:   so.Mapped[bool] = so.mapped_column(default = False)
    # Display Page Source => If enabled, the menu page will present a button for 
    # showing the Markdown code of the current page
    show_source:   so.Mapped[bool] = so.mapped_column(default = False)
    # Display edit button [E]. If this setting is enabled, an edit button [X] (CSS class 'link-edit')
    # will be displayed for all users. If this setting is disabled, the edit button will only be shown
    # for admins or users with permission for editing.
    display_edit_button: so.Mapped[bool] = so.mapped_column(default = True)
    ## Display open source licenses
    # If enabled shows a menu option that displays all open source licenses of dependencies used by
    # this project and information about this server.
    # server and displaying
    show_licenses: so.Mapped[bool] = so.mapped_column(default = True)
    # Always use default locale regardless of user preferred locale provided
    # by the web browser.
    use_default_locale: so.Mapped[bool] = so.mapped_column(default = True)
    # Enable/disable VIM editor emulation
    vim_emulation: so.Mapped[bool] = so.mapped_column(default = False)
	# Default language/locale => The default English is the American English locale (en-US)
    default_locale: so.Mapped[str] = so.mapped_column( default = "en-US" )
    # Web Site Name 
    sitename: so.Mapped[str] = so.mapped_column(default= "MWiki")
    default_password: so.Mapped[str] = so.mapped_column(nullable=False)
    # Wiki Site Description 
    description: so.Mapped[str] = so.mapped_column(default="MWiki Website")

    ## main_font: so.Mapped[Optional[FontFamiliyEnum]]
    main_font: so.Mapped[str] = so.mapped_column(default = FontFamiliyEnum.computer_modern.value)
    title_font: so.Mapped[str] = so.mapped_column(default = FontFamiliyEnum.computer_modern.value)
    code_font: so.Mapped[str] = so.mapped_column(default = CodeFontFamily.ibm_plex_mono.value )
    code_font: so.Mapped[str] = so.mapped_column(default = CodeFontFamily.ibm_plex_mono.value )

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
            ## s.main_font = FontFamiliyEnum.computer_modern
            db.session.add(s)
            db.session.commit()
            return s 
        else:
            return q

    def save(self):
        """Update database entry"""
        self.date_modified = datetime.datetime.now(datetime.timezone.utc)           
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

    def __init__(self, base_path: pathlib.Path, path: pathlib.Path, title: str, debug: bool = False):
        self._base_path: pathlib.Path = base_path
        self._cache: pathlib.Path = base_path / ".data/cache"
        self._title = title 
        # Create cache directory if it does not exist yet.
        self._cache.mkdir(exist_ok=True)
        self._path = self.path()
        self._debug = debug
    
    def path(self):
        """Get path of Wiki page file"""
        p = next(self._base_path.rglob(self._title + ".md"), None)
        return p

    def _cache_html_file(self) -> pathlib.Path:
        ## breakpoint()
        p = self._path
        rel = self._cache / p.relative_to(self._base_path)
        folder =  rel.parent
        folder.mkdir(exist_ok = True)
        cpath = folder / rel.name.replace(".md", ".html")
        return cpath

    def read(self) -> str:
        """Get markdown content of wiki page file."""
        path = self.path()
        text = path.read_text()
        return text 

    def write(self, text: str) -> None:
        """Update markdown content of wiki page file"""
        path = self.path()
        path.write_text(text)

    def is_dirty(self):
        """Returns true if cached html needs update (be recompiled)."""
        if self._debug:
            return True
        out = self._cache_html_file()
        src = self._path
        src_time = src.lstat().st_mtime
        out_time = out.lstat().st_mtime if out.exists() else 0
        res =  src_time > out_time \
            or datetime.datetime.utcfromtimestamp(out_time) < Settings.get_instance().date_modified
        if res:
            return True
        # Json metadata file about wiki page containing dependencies (list of embedded wiki pages)
        info = out.parent / out.name.replace(".html", ".json")
        if not info.exists():
            return res
        deps = []
        links = []
        with open(str(info), "r") as fd:
            data = json.load(fd)
            # Recompile markdown file if the version in the
            # metadata file does not match the expected version.
            file_format_version = data.get("version", "")
            if file_format_version != CACHE_FILE_FORMAT_VERSION:
                return True
            # Recompile the markdown page if using an older version
            # of the json metadata file.
            if "dependencies" not in data and "links" not in data:
                ## print(" [TRACE] Recompile page due to older version of info json file.")
                return True
            deps = data.get("dependencies", [])
            links = data.get("links", [])
        for x in deps:
            p = self._base_path / x
            if p.exists() and p.lstat().st_mtime > out_time:
                return True
        for entry in links:
            exists = entry.get("exists", False)
            afile   = self._base_path / (entry.get("link") + ".md")
            if exists and not afile.exists():
                return True
            if not exists and afile.exists():
                return True
        return False


    def _update_cached_html(self, latex_macros = "" ):
        ## breakpoint()
        if not self.is_dirty():
            return
        ## print(" [TRACE] Recompiling page %s" % str(self._path))
        out = self._cache_html_file()
        text = self.read()
        ## print(" [TRACE] Updating cache = " + str(out))
        headings = mparser.get_headings(text)
        root = mparser.make_headings_hierarchy(headings)
        toc = mparser.headings_to_html(root)
        pagefile = str(self.path())
        base_path = str(self._base_path)
        renderer, content = render.pagefile_to_html(pagefile, base_path)
        title = renderer.title if renderer.title != "" else self._title
        info = out.parent / out.name.replace(".html", ".json")
        ###breakpoint()
        # List eof embedded pages
        dependencies = [ str(x.relative_to(self._base_path)) for x in renderer.dependencies]
        ## List of internal links pointed by this Wiki page
        internal_links = [ {  "link":    x
                            , "exists":  (self._base_path / (x + ".md")).exists() }
                            for x in renderer._internal_links ]
        if dependencies != [] or internal_links != []:
            data = {
                      "version":      CACHE_FILE_FORMAT_VERSION
                    , "dependencies": dependencies
                    , "links":        internal_links
                }
            with open(str(info), "w") as fd:
                json.dump(data, fd)
        else:
            if info.exists(): info.unlink()
        html = flask.render_template(  "content.html"
                                             , title   = title
                                             , page    = self._title
                                             , page_link = self._title.replace(" ", "_")
                                             , pagename = self._title
                                             , content = content
                                             , toc     = toc
                                             , latex_macros = latex_macros
                                             , equation_enumeration = renderer.equation_enumeration
                                             )
        out.write_text(html)

    def render_html(self, latex_macros = "") -> str:
        """Render MWiki page to html"""
        out = self._cache_html_file()
        self._update_cached_html(latex_macros)
        data = out.read_text()
        return data

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
    
    def __init__(self, wikipath: str, debug = False):
        self._wikipath = wikipath
        self._base_path =  pathlib.Path(wikipath)
        self._debug = debug

    def find_page(self, title: str) -> Optional[pathlib.Path]:
        """Get path to Wiki page"""
        mdfile = title  + ".md" 
        result = next(self._base_path.rglob(mdfile), None)
        return result 

    def get_wiki_page(self, title: str) -> Optional[WikiPage]:
        path = self.find_page(title)
        if path is None: 
            return None 
        wikipage = WikiPage(base_path = self._base_path, path = path, title = title, debug = self._debug)
        return wikipage
        




