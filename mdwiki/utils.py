import os
import urllib.parse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.util

def read_resource(module, resource_file: str):
    """Read resource file packaged with a given module."""
    import importlib.resources
    data = ""
    with importlib.resources.open_text(module, resource_file) as fd:
        data =  fd.read()
    return data

def escape_code(code):
    """Escape html code."""
    code = code.replace("&", "&amp;")\
                    .replace("<", "&lt;")\
                    .replace(">", "&gt;")\
                    .replace('"', "&quot;")\
                    .replace("'", "&apos;")
    return code  

def encode_url(url: str):
    q = urllib.parse.quote(url)
    return q

def highlight_code(code: str, language: str, verbose: bool = False) -> str:
    if language == "": return code
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter()
        ## print(f" [TRACE] Highlight code for '{name}' Ok.")
        result = highlight(code, lexer, formatter)
        ## breakpoint()
        return result 
    except pygments.util.ClassNotFound:
        if verbose:
            print(f" [TRACE] Warning not found Python's pygment lexer for '{language}'")
        return code

def file_contains(fileName: str, query: str):
    """Check whether a file (full path) contains a queyr string.
    Returns true if file contains a query string.
    NOTE: This function is case-indepedent.
    """
    with open(fileName) as fd:
        result = False
        while line := fd.readline():
            # Ignore case
            if query.lower() in line.lower(): 
                result = True
                break
        return result

def expand_path(path: str):
    """ Expand path such as '~/home_file.text` to full path.
    """
    import os 
    HOME_PATH = os.getenv("HOME", "")
    path_ = ( path
                .replace("$HOME", HOME_PATH)
                .replace("~", HOME_PATH) 
                .replace(".", os.getcwd())
            )
    return path_

def get_wiki_path(file: str = "") -> str: 
    path = expand_path( os.getenv("WIKI_BASE_PATH") or "./")
    path = os.path.join(path, file)
    return path 


__all__ = (  "escape_code"
           , "encode_url"
           , "highlight_code"
           , "file_contains"
           , "expand_path"
           , "get_wiki_path"
          )