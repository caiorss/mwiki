import urllib.parse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.util

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
