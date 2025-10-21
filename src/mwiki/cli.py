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

def debughook(etype, value, tb):
    import pdb
    import traceback
    traceback.print_exception(etype, value, tb)
    print() # make a new line before launching post-mortem
    pdb.pm() # post-mortem debugger


def generate_login_token_url(wikipath: Optional[str], user: str):
    """Create URL for authentication without password. The token is valid for 20 seconds."""
    MWIKI_URL = os.getenv("MWIKI_URL", "http://localhost:8000")
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error expected --wikipath=./path-to-wiki or MWIKI_PATH environment variable set to this path.")
        exit(1)
    wikipath = utils.expand_path(wikipath)
    mwiki.models.MwikiConfig.set_path(wikipath)
    secret_key = mwiki.models.get_secret_key()
    ## print(" [TRACE] secret_key = ", secret_key)
    timestamp = utils.now_utc_timestamp_add_timedelta(minutes = 0, seconds = 20)
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
    print("NOTE: This URL is only valid for 20 seconds.")
    print("NOTE: If MWiki URL is not correct, set the environment variable $MWIKI_URL to the app URL."
           "For instance, in bash Unix shell $ export MWIKI_URL=https://mydomain.com before "
           "running this comamnd again." )
    print()


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
@click.option("--auth", is_flag = True, help = "Create 20 seconds authenticatiion token and URL for passwordless login. (default user 'admin')")
@click.option("--auth-user", default = "admin", help = "Default user for the login token. (default admin)")
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
           , auth:       bool
           , auth_user:  str 
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

    if auth:
        generate_login_token_url(_wikipath, auth_user)
    
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
       , "regular": "LogicMonospace-Medium.woff2"
    }
   ,{
          "key":     "garamond-pro"
        , "family":  "Garamond Pro Regular"
        , "regular": "AGaramondPro-Regular.woff2"   
    }
   ,{
         "key":   "libertinus-mono"
       , "family": "Libertinus Mono"
       , "regular": "LibertinusMono-Regular.woff2"
    }
   ,{
           "key": "julia-mono"
         , "family":  "Julia Mono"
         , "regular": "JuliaMono-Regular.woff2"  
         , "italic":  "JuliaMono-RegularItalic.woff2"  
         , "bold":    "JuliaMono-Bold.woff2"  
    }
   ,{
          "key":          "libertinus-sans"
        , "family":       "Libertinus Sans"
        , "regular":      "LibertinusSans-Regular.woff2"
        , "italic":       "LibertinusSans-Italic.woff2"
        , "bold":         "LibertinusSanas-Bold.woff2"
    }
    ,{
          "key":          "libertinus-serif"
        , "family":       "Libertinus Serif"
        , "regular":      "LibertinusSerif-Regular.woff2"
        , "italic":       "LibertinusSerif-Italic.woff2"
        , "bold":         "LibertinusSerif-Bold.woff2"
        , "bold-italic":  "LibertinusSerif-BoldItalic.woff2"
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
          "key":      "range-mono"
        , "family":   "Range Mono"
        , "regular":  "range-mono-medium-webfont.woff"
    }
   ,{
          "key":      "range"
        , "family":   "Range"
        , "regular":  "range-regular-webfont.woff"
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
   ,{
        "key":    "peachi-medium"
      , "family": "Peachi Medium"   
      , "regular": "peachi-medium.woff2"
    }
   ,{
        "key":     "fondamento"
      , "family":  "Fondamento"   
      , "regular": "fondamento-regular.woff2"
   }   
   ,{
         "key":     "bricolage-grotesque"
       , "family":  "Bricolage Grotesque"
       , "regular": "bricolage-grotesque-latin-normal.woff2"
   }
   ,{
          "key":    "saira-thin-normal"
        , "family": "Saira Thin Normal"
        , "regular": "saira-latin-thin.woff2"
    }

    ,{
          "key":    "saira-thin-bold"
        , "family": "Saira Thin Bold"
        , "regular": "saira-latin-thin-bold.woff2"
    }
    ,{
         "key":     "dinweb-light"
       , "family":  "DINWeb-Light"
       , "regular": 'DINWeb-Light.woff'
    }
    ,{
         "key":      "dinweb-medium"
       , "family":   "DINWeb-Medium"
       , "regular":  "DINWeb-Medium.woff"
        
    }
    ,{
        "key":     "dinweb-black"
      , "family":  "DINWeb-Black"
      , "regular": "DINWeb-Black.woff"
        
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
       

def render_font_data(  key: str 
                     , root_url: str                = ""
                     , self_contained: bool         = False
                     , root_path: Optional[pathlib.Path] = None
                     ):
    data = get_font_data(key)
    if not data:
        return ""
    ## print(" [TRACE] root_path = " + str(root_path))
    family = data.get("family")
    has_italic = "italic" in data
    has_bold   = "bold" in data
    has_bold_italic = "bold-italic" in data
    root = "" if root_url == "/" else root_url
    code = """
@font-face {
    font-family: '{{family}}';
    {% if has_italic %}
    font-style: {{font_style}};
    {% endif %}
    {% if has_bold %}
    font-weight: {{font_weight}};
    {% endif %}
    {%if not self_contained %}
    src: url('{{root}}/static/fonts/{{file}}');
    {% else %}
    src: url({{font_data_b64}});
    {% endif %}
}
    """
    tpl = jinja2.Template(code)
    font_face_regular_b64 = ""
    font_face_regular_file: pathlib.Path = root_path / ("static/fonts/" + data.get("regular", ""))
    ## 0print("font_file = ", font_face_regular_file)
    if self_contained and font_face_regular_file.is_file():
        font_face_regular_b64 = mwiki.utils.file_to_base64_data_uri(font_face_regular_file)
        ### print(f" regular font = {key} => " + font_face_regular_b64)
    font_face_regular = tpl.render(  family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("regular")
                                   , font_style = "normal"
                                   , font_weight = "normal"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_regular_b64 
                               )
    font_face_italic = ""
    font_face_italic_b64 = ""
    font_face_italic_file = root_path / ("static/" + data.get("italic", ""))
    if self_contained and font_face_italic_file.is_file():
        font_face_regular_b64 = mwiki.utils.file_to_base64_data_uri(font_face_italic_file)
    if has_italic:
        font_face_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("italic")
                                   , font_style = "italic"
                                   , font_weight = "normal"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_italic_b64 
                               )
    
    font_face_bold = ""
    font_face_bold_b64 = ""
    font_face_bold_file = root_path / ("static/fonts/" + data.get("bold", ""))
    if self_contained and font_face_bold_file.is_file():
        font_face_bold_b64 = mwiki.utils.file_to_base64_data_uri(font_face_bold_file)
    if has_bold:
        font_face_bold = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold")
                                   , font_style = "normal"
                                   , font_weight = "bold"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_bold_b64 
                               )
    font_face_bold_italic = ""
    font_face_bold_italic_b64 = ""
    font_face_bold_italic_file = root_path / ("static/fonts/" + data.get("bold-italic", ""))
    if self_contained and font_face_bold_file.is_file():
        font_face_bold_italic_b64 = mwiki.utils.file_to_base64_data_uri(font_face_bold_italic_file)
    if has_bold_italic:
        font_face_bold_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold-italic", "")
                                   , font_style = "italic"
                                   , font_weight = "bold"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_bold_italic_b64 
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
@click.option( "--page"
             , default = None
             , help = "Export single page to html, instead of the whole wiki.")
@click.option("--website-name", default = "MWiki", help="Name of the static website (default value 'MWiki').") 
@click.option("--root-url", default = "/", help="Root URL that the static website will be deployed to.  (default value '/').") 
@click.option("--locale", default = "en-US", help="Default locale of the user interface. (Default value 'en-US')") 
@click.option("--icon", default = None, help="Favicon of the static website. (Default value MWiki icon)") 
@click.option("--main-font", default = "literata", help="Main font used in document text.") 
@click.option("--code-font", default = "libertinus-mono", help="Code monospace font used in code blocks.") 
@click.option("--title-font", default = "news-reader", help="Title font used in document section headings.") 
@click.option("--list-fonts", is_flag = True, help="List all available fonts.") 
@click.option("--allow-language-switch", is_flag = True
              , help = ( "Allow end-user to switch the user interface language."
                         
             ))
@click.option("--self-contained", is_flag = True
             , help = ( "Embed all attachment within the current wiki page."
                        " JavaScripts and CSS are inlined and images are embedded in base64 encoding. The generated HTML self-contained file is similar to a PDF file."
                        " This flag is useful for generating self-contained documents for offline view."
            ) )
@click.option("--embed-mathjax", is_flag = True, help = ("Self host Mathjax library for rendering math formulas instead "
                                                        "of loading it from a CDN."))
@click.option("--author", default = None, help = (
                                            'Override the frontmatter attribute author in all wiki pages. '
                                            'The author field is compiled to <meta name="author" content="AUTHOR NAME"> '
                                            'This setting only makes sense if there is a single author.'
                                            ))
def compile(  wikipath:              Optional[str]
            , output:                Optional[str]
            , page:                  Optional[str]
            , website_name:          str
            , root_url:              str 
            , locale:                str
            , icon:                  Optional[str]
            , main_font:             str 
            , code_font:             str 
            , title_font:            str 
            , list_fonts:            bool 
            , allow_language_switch: bool
            , self_contained:        bool 
            , embed_mathjax:         bool
            , author:                str 
            ):
    """Compile a MWiki repository to a static website."""
    bool_to_on_off = lambda x: "on" if x else "off"
    if list_fonts:
        print("%30s%30s"  % ("KEY", "FONT FAMILY"))            
        for fdata in fonts_database:
            key = fdata.get("key", "")
            family = fdata.get("family", "")
            print("%30s%30s" % (key, family))
        exit(0)
    if not wikipath and not page:
        print("Error expected --wikipath or --page command line switches.")
        exit(1)
    out = pathlib.Path(output) if output else pathlib.Path("./out")
    out.mkdir(exist_ok = True)
    root = pathlib.Path(wikipath)
    if not root.exists():
        print(f"Error not found {root.resolve()}")
        exit(1)
    if root_url != "/" and root_url.endswith("/"):
        root_url = "/" + root_url.strip("/")
    # mwiki.models.MwikiConfig.set_path(wikipath)
    base_path = str(wikipath)
    # secret_key = mwiki.models.get_secret_key()
    # app.config["SECRET_KEY"] = secret_key
    print("Root URL\n - ", root_url)
    print("Compiling wiki repository\n - ", root.resolve())
    print("Generating static website at\n - ", out.resolve())
    print()
    root_url = "" if root_url == "/" else root_url
    pages = []
    if page:
        page_path = pathlib.Path(page)
        if not page_path.exists():
            print(f"Error file {page_path} not found.")
            exit(1)
        pages = [ page_path ]
    else:
        pages = root.rglob("*.md")
    static = out / "static"
    static.mkdir(exist_ok = True)
    if not self_contained:
        mwiki.utils.copy_resource_files_ext(mwiki, "static/*.svg", static)
        mwiki.utils.copy_resource_file(mwiki, "static/main.js", static )
        mwiki.utils.copy_resource_file(mwiki, "static/static_style.css", static )
    main_js = mwiki.utils.get_path_to_resource_file(mwiki, "static/main.js")
    style_css = mwiki.utils.get_path_to_resource_file(mwiki, "static/static_style.css")
    main_code = main_js.read_text()
    style_code = style_css.read_text()
    if embed_mathjax:
        mwiki.utils.copy_resource_directory(mwiki, "static/mathjax", static / "mathjax" )
    # images = out / "images"
    # pasted = out / "pasted"
    # src_upload = root / "upload"
    # src_images = root / "images"
    # src_pasted = root / "pasted"
    # if src_images.exists():
    #     images.mkdir(exist_ok = True)
    #     mwiki.utils.copy_folder(src_images, images)
    # if src_pasted.exists():
    #     pasted.mkdir(exist_ok = True)
    #     mwiki.utils.copy_folder(src_pasted, pasted)
    # if src_upload.exists():
    #     mwiki.utils.copy_folder(src_upload, out / "upload")
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
    root_path = mwiki.utils.get_module_path(mwiki)
    ### print(" [TRACE] root_path => (718) = " + str(root_path))
    font_face_main_font =  render_font_data(main_font
                                            , root_url = root_url
                                            , root_path = root_path
                                            , self_contained = self_contained)
    font_face_title_font = render_font_data(title_font
                                            , root_url = root_url
                                            , root_path = root_path
                                            , self_contained = self_contained)
    font_face_code_font = render_font_data(code_font
                                           , root_url = root_url
                                           , root_path = root_path
                                           , self_contained = self_contained)
    if not self_contained:
        fonts = out / "static/fonts"
        fonts.mkdir(exist_ok = True)
        copy_font_files(main_font, fonts)
        copy_font_files(title_font, fonts)
        copy_font_files(code_font, fonts)
    main_font_family  = (get_font_data(main_font) or {}).get("family") 
    title_font_family = (get_font_data(title_font) or {}).get("family")  
    code_font_family  = (get_font_data(code_font) or {}).get("family")  
    unfold_icon_url = f"{root_url}/static/dots-vertical.svg"
    menu_icon_url   = f"{root_url}/static/hamburger-menu.svg"
    home_icon_url   = f"{root_url}/static/icon-home.svg"
    if self_contained:
        unfold_icon_url = mwiki.utils.file_to_base64_data_uri(root_path / "static/dots-vertical.svg")
        menu_icon_url = mwiki.utils.file_to_base64_data_uri(root_path / "static/hamburger-menu.svg")
        home_icon_url = mwiki.utils.file_to_base64_data_uri(root_path / "static/icon-home.svg")
    print()
    print("Compilation Settings")
    print()
    print(" [*]                              Author: ", author or "")
    print(" [*]                        Website Name: ", website_name)
    print(" [*]                            Root URL: ", "/" if root_url == "" else root_url)
    print(" [*]  Default User Interface (UI) Locale: ", locale)
    print(" [*]               Allow language switch: ", bool_to_on_off(allow_language_switch))
    print(" [*]                       Embed Mathjax: ", bool_to_on_off(embed_mathjax))
    print(" [*]               Load Mathjax from CDN: ", bool_to_on_off(not embed_mathjax))
    print(" [*]                    Main font family: ", main_font_family)
    print(" [*]                   Title Font Family: ", title_font_family)
    print(" [*]                    Code Font Family: ", code_font_family)
    print()
    print("Status:")
    print()
    for p in pages:
        outfile = out / str(p.relative_to(root))\
                .replace("Index", "index")\
                .replace(".md", ".html")\
                .replace(" ", "_")
        print(f" [*] Compiling {p} to {outfile}")
        pagefile = str(p)
        renderer, content = render.pagefile_to_html(  pagefile
                                                    , base_path
                                                    , static_compilation = True
                                                    , self_contained = True
                                                    , root_url = root_url
                                                    )
        files = renderer.files
        if not self_contained:
            for file  in files:
                f = file.relative_to(root)
                dest = out / f.parent
                dest.mkdir( exist_ok = True)
                shutil.copy(file, dest)
        title = renderer.title if renderer.title != "" else str(p.name ).split(".")[0]
        # Generate table of contents 
        page_source = p.read_text()
        headings    = mparser.get_headings(page_source)
        root_       = mparser.make_headings_hierarchy(headings)
        toc         = mparser.headings_to_html(root_)
             # print(" [TRACE] needs pseudocode_js ", renderer.needs_latex_algorithm)
        env = {
                 "title":                title.replace("about", "About")
               , "page":                 title
               , "page_link":            title.replace(" ", "_")
               , "root_url":             root_url
               , "pagename":             title
               , "allow_language_switch": allow_language_switch
               , "main_font":            main_font_family  
               , "title_font":           title_font_family
               , "font_face_main":       font_face_main_font
               , "font_face_code":       font_face_code_font
               , "font_face_title":      font_face_title_font
               , "favicon":              icon_path 
               , "favicon_mimetype":     icon_mimetype
               , "page_description":     renderer.description
               , "page_author":          renderer.author or author 
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
               , "embed_mathjax":        embed_mathjax 
               , "self_contained":       self_contained
               , "main_script_code":     main_code
               , "style_sheet_code":     style_code
               , "menu_icon_url":        menu_icon_url 
               , "unfold_icon_url":      unfold_icon_url 
               , "home_icon_url":        home_icon_url
              }
        html = tpl.render(env)
        outfile.write_text(html)
    print(" [*] Compilation terminated successfully ok.")
    exit(0)
        
 
 
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
    """Create token and url for authentication without password. The URL is valid for 20 seconds."""
    wikipath = wikipath or os.getenv("MWIKI_PATH")
    if wikipath is None:
        print("Error extepected --wikipath or enviroment variable $MWIKI_PATH")
        exit(1)
    if not pathlib.Path(wikipath).resolve().is_dir():
        print(f"Error directory not found: {wikipath}")
        exit(1)
    generate_login_token_url(wikipath, user)
    exit(0)



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

