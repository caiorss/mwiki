"""Command Line Handler 

Module responsible for processing command line switches and options.
"""
import os
import os.path 
import sys
import random
import pathlib
import subprocess
import tomli 
import shutil
from pprint import pprint
from typing import Optional, Tuple, List 
import click
import flask 
import jinja2
##import waitress
## from click.decorators import commmand 
## from gunicorn.app.wsiapp import run 
import multiprocessing
import mwiki.utils as utils
from mwiki.server import make_app_server
import mwiki.convert
import mwiki.search as search
import mwiki.mparser as mparser
import mwiki.watcher
import mwiki.render as render
import mwiki.models
import mwiki.utils as utils
from . import render
from .models import User, Settings
from .app import db, app 


###  # Check whether the OS is a Unix-like operating system
###  if utils.is_os_linux_or_bsd() or utils.is_os_macos():
###      from gunicorn.app.wsgiapp import WSGIApplication
###  else:
###      print("WARNING: Cannot run using gunicorn on Microsoft Windows OS\n" 
###            "Use another WSGI server.")
###  
###  class StandaloneApplication(WSGIApplication):
###      def __init__(self, app_uri, options=None):
###          self.options = options or {}
###          self.app_uri = app_uri
###          super().__init__()
###  
###      def load_config(self):
###          config = {
###              key: value
###              for key, value in self.options.items()
###              if key in self.cfg.settings and value is not None
###          }
###          for key, value in config.items():
###              self.cfg.set(key.lower(), value)
###  
###  
###  def gunicorn_runner(  host:      str
###                      , port:      int
###                      , wikipath:  str
###                      , login:     Optional[str] = None
###                      , secret_key: Optional[str] = None 
###                      ):
###      options = {
###            "bind": f"{host}:{port}"
###          , "workers": (multiprocessing.cpu_count() * 2) + 1
###          ## "worker_class": "uvicorn.workers.UvicornWorker",
###      }
###      environemnt = {
###            "HOST":        host 
###          , "PORT":        str(port)
###          , "LOGIN":       login
###          , "SECRET_KEY":  secret_key
###          , "WIKIPATH":    wikipath
###      }
###      ### print(" [TRACE] wikipath = ", wikipath)
###      for (variable, value) in environemnt.items():
###          ## print(f" [TRACE] variable = {variable} ; value = {value}")
###          if value is not None: os.environ[variable] = value
###      ## See module: mwiki/wsgi, related to file mwiki/wsgi.py 
###      # the inputs of this module are environment variables
###      sapp = StandaloneApplication("mwiki.wsgi:app", options)
###      sapp.run()

def debughook(etype, value, tb):
    import pdb
    import traceback
    traceback.print_exception(etype, value, tb)
    print() # make a new line before launching post-mortem
    pdb.pm() # post-mortem debugger


@click.group()
def cli1():
    pass


@cli1.command()
@click.option("-h", "--host", default = "0.0.0.0", help="Host to be listened, default 0.0.0.0")
@click.option("-p", "--port", default = 8080, help="TCP port to be listend, default 8080.")
@click.option("--login", default = "", help = "Require login to access any page.")
@click.option("--debug", is_flag = True
            , help =( "Run server in debug mode. WARNING: It is unsafe to run" 
                     " the server in debug mode when exposed in the internet since" 
                     " it can display creadentials and tokens passed as environment" 
                     " variables and expose internal details."
                     ))
@click.option("--random-ssl", is_flag  = True
                , help = ( "Run server with random generated SSL certificate. "
                          " It is not necessary to run openssl command line tool"
                          " or create or pass any file in order to use this command line switch."
                          ))
@click.option("--wikipath", default = ".", help = "Path to wiki directory, default '.' current directory.")
@click.option("-c", "--config", default = None, 
                help = ( "Path to TOML configuration file for" 
                        "running the server and loading its settings from the file."))
@click.option("-s", "--secret-key", default = None, 
                help = ( "Secret key of flask application." ))
@click.option("-g", "--wsgi", 
                is_flag = True, 
                help = ( "Run application with gunicorn WSGI server."
                         "NOTE: Gunicorn only works on Unix-like systems, including "
                         "Linux, BSD or Apple's MacOS. This option is recommended for "
                         "deploying the server in production."
                         ))
@click.option("--pdb", is_flag = True, 
                help = ( "Enable post-mortem debugger." ))
def server(  host:       str
           , port:       int
           , debug:      bool
           , login:      str
           , wikipath:   str
           , random_ssl: bool
           , config:     str
           , secret_key: Optional[str]
           , pdb:        bool
           , wsgi:       bool
           ):
    """Run the mwiki server."""
    _login = None  
    if pdb:
        print("[INFO] Enabled Post-mortem debugger.")
        sys.excepthook = debughook
    # Default value for configuration variables
    _host = host 
    _port = port 
    _debug = debug
    _do_login = login
    _login = login.split(",")
    _username = _login[0] if len(_login) == 2 else ""
    _password = _login[1] if len(_login) == 2 else ""
    _wikipath = wikipath
    ## print(" [TRACE] (before) wikipath = ", _wikipath)
    _secret_key = secret_key
    _random_ssl = random_ssl
    ##_pdb = pdb 
    _wsgi = wsgi 
    ## ---- Load server settings from a configuration file --- ## 
    if config is not None:
        if not os.path.isfile(config):
            print(f"Error file '{config} does not exist")
            exit(1)
        conf = {}
        with open(config, 'rb') as fd:
            conf = tomli.load(fd)
        if "server" not in conf:
            print(f"Error - missing section [server] in toml config file '{config}'.")
            exit(1)
        server      = conf.get("server", {})
        _host       = server.get("host", "127.0.0.1")
        _port       = server.get("port", 8080)
        _debug      = server.get("debug", False)
        _do_login   = server.get("login", False)
        _username   = server.get("username", "")
        _password   = server.get("password", "")
        _wikipath   = utils.expand_path( server.get("wikipath", ".") )
        _random_ssl = server.get("random-ssl", False)
        _login = (_username, _password) if _do_login else None 
        _secret_key = server.get("secret_key", None)
        #make_app_server(_host, _port, _debug, _login, _wikipath, _random_ssl, _secret_key)
    _wikipath = utils.expand_path(_wikipath)
    if debug:
        mwiki.models.MwikiConfig.enable_debug()
    if not os.path.isdir(_wikipath):
        print("ERROR: Expected an existing wiki directory files (markdown repository).")
        print(f"Directory {_wikipath} not found.")
        exit(1)
    if login != "":
        #os.environ["DO_LOGIN"] = "true"
        if len(_login) != 2:
            ### print("Error expected login in format --login=<USERNAME>;<PASSWORD>")
            exit(1)
    # Add all markdown files (Wiki pages) to the search index database (powered by Whoosh Python library)
    base_path = pathlib.Path(_wikipath)
    mwiki.models.MwikiConfig.set_path(_wikipath)
    if not search.search_index_exists(base_path):
        search.index_markdown_files(base_path)
    if wsgi:
        _loginp = f"{_username},{_password}" if _username != "" else None
        os.environ["SERVER_SOFTWARE"] = "waitress"
        os.environ["WIKIPATH"] = _wikipath
        os.environ["MWIKI_PATH"] = _wikipath
        pyexecutable = sys.executable
        procWatcher =  subprocess.Popen([  pyexecutable
                                      ,"-m" , "mwiki.watcher"
                                      ]) 
        ## print(" [TRACE] procWatcher = ", procWatcher.pid)
        proc = subprocess.Popen([  pyexecutable
                                 , "-m" , "waitress"
                                 , f"--port={port}"
                                 , f"--host={host}"
                                 , "mwiki.wsgi:app"
                                 ]) 
        proc.wait()
        ## print(" [TRACE] Starting flask app using WSGI, wikipath = ", _wikipath)
        ### gunicorn_runner(_host, _port, _wikipath
        ###                 , login = _loginp 
        ###                 , secret_key= _secret_key
        ###                 )
        exit(0)
    _login =  x if len(x := login.split(",")) == 2 else None
    app = make_app_server(  host       = _host
                          , port       = _port
                          , debug      = _debug
                          , login      = _login
                          , wikipath   = _wikipath
                          , secret_key = _secret_key
                          , random_ssl = _random_ssl
                          )
    app.run(host = host, port = port, debug = debug)
    ## app.run(host = host, port = port, debug=True)


@cli1.command()
@click.option("--wikipath", default = "", help = "Path to wiki directory, default '.' current directory.")
def watch(wikipath: str):
    """Start watcher process manually for debugging purposes.
    """
    _wikipath = utils.expand_path( wikipath ) \
                if  wikipath != "" else os.environ.get("MWIKI_PATH", ".")
    mwiki.models.MwikiConfig.set_path(_wikipath)
    #os.environ["SERVER_SOFTWARE"] = "waitress"
    ## os.environ["WIKIPATH"] = _wikipath
    os.environ["MWIKI_PATH"] = _wikipath
    mwiki.watcher.watch()


fonts_database  = [
    {
          "key":     "computer-modern"
        , "family":  "Computer Modern"
        , "regular": "computer-modern-normal.ttf"
        , "italic":  "computer-modern-italic.ttf"
        , "bold":    "computer-modern-bold.ttf"
    }
   ,{
          "key":          "ibm-plex-mono"
        , "family":       "IBM Plex Mono"
        , "regular":      "IBM-computer-modern-normal.ttf"
        , "italic":       "computer-modern-italic.ttf"
        , "bold":         "computer-modern-bold.ttf"
        , "bold-italic":  "computer-modern-bold.ttf"
    }
   ,{
          "key":     "chicago"
        , "family":  "Chicago MacOS"
        , "regular": "ChicagoFLF.ttf"
    }
   ,{
          "key":     "news-reader"
        , "family":  "NewsReader"
        , "regular":  "NewsReader.woff2"
    }
   ,{
          "key":          "literata"
        , "family":       "Literata"
        , "regular":      "Literata-Regular.ttf"
        , "italic":       "Literata-Italic.ttf"
        , "bold":         "Literata-Bold.ttf"
    }
   ,{
          "key":         "literata-variable"
        , "family":      "Literata-Regular" 
        , "regular":     "literata-variable-font-opsz.ttf" 
        , "italic":      "literata-variable-font-italic-opsz.ttf" 
    }
   ,{
         "key":          "commint-mono"
       , "family":       "Commit Mono"
       , "regular":      "CommitMono-400-Regular.otf"
       , "italic":       "CommitMono-400-Italic.otf"
       , "bold":         "CommitMono-700-Regular.otf"
       , "bold-italic":  "CommitMono-700-Italic.otf"
    }
    ,{
         "key":    "logic-monospace-regular"
       , "family":  "Logic Monospace Regular"
       , "regular": "LogicMonospace-Regular.woff2"
    }
    ,
    {
         "key":    "logic-monospace-medium"
       , "family": "Logic Monospace Medium"
    }
   ,{
         "key":   "libertinus-mono"
       , "family": "Libertinus Mono"
       , "regular": "LibertinusMono-Regular.woff2"
   }
   ,{
        "key":         "commint-mono"
      , "family":      "Commint Mono"
      , "regular":     "CommitMono-400-Regular.otf"
      , "italic":      "CommitMono-400-Italic.otf"
      , "bold":        "CommitMono-700-Regular.otf"
      , "bold-italic": "CommitMono-700-Italic.otf"
    
    }
   ,{
        "key":     "crimson"
      , "family":  "Crimson"
      , "regular": "crimson-roman.woff"
      , "italic":  "crimson-italic.woff"
      , "bold":    "crimson-bold.woff"
        
    }

   ,{
        "key":     "munson"
      , "family":  "Munson"
      , "regular": "munson-roman.woff2"
      , "italic":  "munson-italic.woff2"
      , "bold":    "munson-bold.woff2"
    }
   ,{
        "key":     "jackwrite"
      , "family":  "Jackwrite"
      , "regular": "Jackwrite.woff2"
   }

   ,{
        "key":     "jackwrite-bold"
      , "family":  "Jackwrite Bold"
      , "regular": "JackwriteBold.woff2"
   }
   ,{
       "key":    "cmu-concrete"
      ,"family": "CMU Concrete"
      ,"regular": "cmu-concrete-regular.woff"
      ,"italic": "cmu-concrete-italic.woff"
   }

   ,{
       "key":    "cmu-sans-serif"
      ,"family": "CMU Sans Serif"
      ,"regular": "cmu-sans-serif-regular.woff"
      ,"italic":  "cmu-sans-serif-bold.woff"
   }
   
]

def get_font_data(font_key: str):
    for x in fonts_database:
        key = x.get("key", "")
        ## print(" [TRACE] key = ", key)
        if key == font_key:
            return x 
    return None


def copy_font_files(font_key: str, dest: pathlib.Path):
    data = get_font_data(font_key)
    if not data:
        return
    regular = data.get("regular")
    italic = data.get("italic")
    bold = data.get("bold")
    bold_italic = data.get("bold-italic")
    if regular:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + regular) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if italic:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + italic) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if bold:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + bold) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if bold_italic:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + bold_italic) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
       

def render_font_data(key):
    data = get_font_data(key)
    if not data:
        return ""
    family = data.get("family")
    has_italic = "italic" in data
    has_bold   = "bold" in data
    has_bold_italic = "bold-italic" in data
    code = """
@font-face {
    font-family: '{{family}}';
    {% if has_italic %}
    font-style: {{font_style}};
    {% endif %}
    {% if has_bold %}
    font-weight: {{font_weight}};
    {% endif %}
    src: url('/static/fonts/{{file}}');
}
    """
    tpl = jinja2.Template(code)
    font_face_regular = tpl.render(  family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("regular")
                                   , font_style = "normal"
                                   , font_weight = "normal"
                               )
    font_face_italic = ""
    if has_italic:
        font_face_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("regular")
                                   , font_style = "italic"
                                   , font_weight = "normal"
                               )
    
    font_face_bold = ""
    if has_bold:
        font_face_bold = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold")
                                   , font_style = "normal"
                                   , font_weight = "bold"
                               )
    font_face_bold_italic = ""
    if has_bold_italic:
        font_face_bold_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold-italic")
                                   , font_style = "italic"
                                   , font_weight = "bold"
                               )
    out = font_face_regular 
    out = out + "\n\n" + font_face_italic if font_face_italic != "" else out
    out = out + "\n\n" + font_face_bold   if font_face_bold   != "" else out
    out = out + "\n\n" + font_face_bold_italic   if font_face_bold_italic != "" else out
    return out 



@cli1.command()
@click.option("--wikipath", default = None, 
                help = ( "Path to folder containing *.md files." )
                )
@click.option("-o", "--output", default = None, 
                help = ( "Directory that will contain the compilation output (default value ./out)." )
                )
@click.option("--website-name", default = "MWiki", help="Name of the static website (default value 'MWiki').") 
@click.option("--locale", default = "en-US", help="Default locale of the user interface. (Default value 'en-US')") 
@click.option("--icon", default = None, help="Favicon of the static website. (Default value MWiki icon)") 
@click.option("--main-font", default = "literata", help="Main font used in document text.") 
@click.option("--code-font", default = "libertinus-mono", help="Code monospace used in code blocks.") 
@click.option("--title-font", default = "news-reader", help="Title font used in document section headings.") 
@click.option("--list-fonts", default = False, help="List all available fonts.") 
def compile(  wikipath: Optional[str], output: Optional[str]
            , website_name: str
            , locale: str
            , icon
            , main_font
            , code_font 
            , title_font
            , list_fonts
            ):
    """Compile a MWiki repository to a static website."""
    if list_fonts:
        print("%30s%30s"  % ("KEY", "FONT FAMILY"))            
        for fdata in fonts_database:
            key = fdata.get("key", "")
            family = fdata.get("family", "")
            print("%30s%30s" % (key, family))
        exit(0)
    if not wikipath:
        print("Error expected path to wiki folder --wikipath=/path/to/repository")
        exit(1)
    out = pathlib.Path(output) if output else pathlib.Path("./out")
    out.mkdir(exist_ok = True)
    root = pathlib.Path(wikipath)
    if not root.exists():
        print(f"Error not found {root.resolve()}")
        exit(1)
    # mwiki.models.MwikiConfig.set_path(wikipath)
    base_path = str(wikipath)
    # secret_key = mwiki.models.get_secret_key()
    # app.config["SECRET_KEY"] = secret_key
    print(" [*] Compiling ", root)
    pages = root.rglob("*.md")
    static = out / "static"
    static.mkdir(exist_ok = True)
    mwiki.utils.copy_resource_files_ext(mwiki, "static/*.svg", static)
    mwiki.utils.copy_resource_file(mwiki, "static/main.js", static )
    mwiki.utils.copy_resource_file(mwiki, "static/static_style.css", static )
    images = out / "images"
    pasted = out / "pasted"
    src_upload = root / "upload"
    src_images = root / "images"
    src_pasted = root / "pasted"
    if src_images.exists():
        images.mkdir(exist_ok = True)
        mwiki.utils.copy_folder(src_images, images)
    if src_pasted.exists():
        pasted.mkdir(exist_ok = True)
        mwiki.utils.copy_folder(src_pasted, pasted)
    if src_upload.exists():
        mwiki.utils.copy_folder(src_upload, out / "upload")
    icon_mimetypes_database = {
          "ico":   "image/x-icon"
        , "png":   "image/png"
        , "jpg":   "image/jpeg"
        , "jpgeg": "image/jpeg"
        , "svg":   "image/svg+xml"
    }
    icon_mimetype = "image/x-icon"
    icon_path = ""
    if icon is not None:
        p = pathlib.Path(icon)
        if not p.is_file():
            print(f"Error not found icon file: {p} ")
            exit(1)
        print(" [*] Using favicon ", icon)
        shutil.copy(p, out)
        icon_path = str(p.name)
        extension = str(p.name).split(".")[0].strip(".")
        icon_mimetype = icon_mimetypes_database.get(extension) or icon_mimetype
    template  = utils.read_resource(mwiki, "templates/static.html")
    tpl = jinja2.Template(template)
    font_face_main_font =  render_font_data(main_font)
    # print(" [TRACE] font_face_main_font = \n", font_face_main_font)
    font_face_title_font = render_font_data(title_font)
    fonts = out / "static/fonts"
    fonts.mkdir(exist_ok = True)
    copy_font_files(main_font, fonts)
    copy_font_files(title_font, fonts)
    copy_font_files(code_font, fonts)
    main_font_family  = (get_font_data(main_font) or {}).get("family") 
    title_font_family = (get_font_data(title_font) or {}).get("family")  
    code_font_family  = (get_font_data(code_font) or {}).get("family")  
    print(" [*] Main font  family: ", main_font_family)
    print(" [*] Title Font Family: ", title_font_family)
    print(" [*]  Code Font Family: ", code_font_family)
      
    for p in pages:
        outfile = out / str(p.relative_to(root))\
                .replace("Index", "index")\
                .replace(".md", ".html")\
                .replace(" ", "_")
        print(f" [*] Compiling {p} to {outfile}")
        pagefile = str(p)
        renderer, content = render.pagefile_to_html(pagefile, base_path, static_compilation = True)
        title = renderer.title if renderer.title != "" else str(p.name ).split(".")[0]
        # Generate table of contents 
        page_source = p.read_text()
        headings = mparser.get_headings(page_source)
        root_ = mparser.make_headings_hierarchy(headings)
        toc = mparser.headings_to_html(root_)
      
        # print(" [TRACE] needs pseudocode_js ", renderer.needs_latex_algorithm)
        env = {
                 "title":                title.replace("about", "About")
               , "page":                 title
               , "page_link":            title.replace(" ", "_")
               , "pagename":             title
               , "main_font":            main_font_family  
               , "title_font":           title_font_family
               , "font_face_main":       font_face_main_font
               , "font_face_title":      font_face_title_font
               , "favicon":              icon_path 
               , "favicon_mimetype":     icon_mimetype
               , "page_description":     renderer.description
               , "page_author":          renderer.author
               , "toc":                  toc 
               , "content":              content               
               , "mathjax_enabled":      renderer.needs_mathjax
               , "graphviz_enabled":     renderer.needs_graphviz 
               , "latex_algorithm":      renderer.needs_latex_algorithm
               , "equation_enumeration": renderer.equation_enumeration
               , "config_sitename":      lambda: website_name 
               , "config_main_font":     lambda: main_font_family
               , "config_code_font":     lambda: code_font_family
               , "config_title_font":    lambda: title_font_family
               , "default_locale":       lambda: locale
               , "use_default_locale":   lambda: True
              }
        html = tpl.render(env)
        outfile.write_text(html)
        
 
 
@cli1.command()
@click.option("-p", "--path", default = None, 
                help = ( "Path to folder containing *.md files." )
                )
@click.option("-f", "--file", default = None, 
                help = ( "Path to *.md file to be compiled." )
                )
def compile_latex(path: Optional[str], file: Optional[str]):
    """Compile Latex Formulas of .md file or folder to SVG images.
    The images are stored in the cache folder.
    """
    if file is not None:
        if not os.path.isfile(file):
            print(f" [ERROR] File {file} does not exist.")
            exit(1)
        render.compile_pagefile(file)
        exit(0)
    if path is None:
        print("Error expected path to folder")
        exit(1)
    ##pattern = os.path.join(path, "*.md")
    ## files = glob.glob(pattern)
    render.compile_folder(path)
    ###print(" [INFO] Start compilation of ", path)
    ###with multiprocessing.Pool(4) as p:
    ###    p.map(render.compile_pagefile, files)
    ###print(" [INFO] End compilation of latex formulas in ", path)
    ##with multiprocessing.Pool(5) as p:
    ### # Create process pool 
    ### p = multiprocessing.Pool(5)
    ### p.map(render.compile_pagefile, files)
    ### p.close()
    # Wait for all task termination  
    ## p.join()
    ## input("Type RETURN to exit")
    ## render.compile_folder(path)

@cli1.command()
@click.option("--admin-password", 
                help = ( "Set admin password." )
                )
@click.option("--sitename", 
                help = ( "Change site name" )
                )
def manage(admin_password = None, sitename = None):
    """Manage MWiki settings, including accounts, passwords and etc."""
    if admin_password is not None:
        with app.app_context():
            admin = User.get_user_by_username("admin")
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(" [*] Password changed for admin. Ok.")
    if sitename is not None:
        with app.app_context():
            settings = Settings.get_instance()
            settings.sitename = sitename
            settings.save()
            print(f" [*] Site name changed to: {sitename}")


@cli1.command()
@click.option("--wikipath", default = None, help = "Path to wiki directory, default '.' current directory.")
@click.option("--user", default = "admin", help = "Username to authenticate.")
def auth(wikipath: Optional[str], user: str):
    """Create URL for authentication without password. The URL is valid for 1 minute."""
    MWIKI_URL = os.getenv("MWIKI_URL", "http://localhost:8000")
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error expected --wikipath=./path-to-wiki or MWIKI_PATH environment variable set to this path.")
        exit(1)
    wikipath = utils.expand_path(wikipath)
    mwiki.models.MwikiConfig.set_path(wikipath)
    secret_key = mwiki.models.get_secret_key()
    ## print(" [TRACE] secret_key = ", secret_key)
    timestamp = utils.now_utc_timestamp_add_minutes(1)
    salt = random.randint(1, 1000)
    message = user + "/" + str(timestamp) + "/" + str(salt)
    signature = utils.hmac_signature(secret_key, message)
    data = { "user": user, "salt": salt, "expiration": timestamp, "signature": signature}
    authtoken = utils.encode_json_to_base64(data)
    url = f"{MWIKI_URL}/auth?token={ utils.escape_url(authtoken) }"
    print("Copy and paste the following URL in the web browser to authenticate.")
    print()
    print(" ", url)
    print()
    print(f"Or paste the following token in the log in form {MWIKI_URL} ")
    print(" \n", authtoken)
    print()
    print("NOTE: This URL is only valid for 1 minute.")
    print("NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL. For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before running this comamnd again.")

@cli1.command()
@click.option("-f", "--file", default = None, 
                help = ( "Input markdown file to be converted." )
                )
@click.option("-o", "--output", default = None, 
                help = ( "Output file." )
                )
def convert(file: Optional[str], output: Optional[str]):
    """Convert from org-mode markup to markdown"""
    mwiki.convert.convert_file(file, output)


def main():
    cli = click.CommandCollection(sources = [ cli1 ])
    cli()

