import os
import re
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

def escape_html(code):
    """Escape html code."""
    code = code.replace("&", "&amp;")\
                    .replace("<", "&lt;")\
                    .replace(">", "&gt;")\
                    .replace('"', "&quot;")\
                    .replace("'", "&apos;")
    return code

def escape_url(url: str):
    q = urllib.parse.quote(url)
    return q

_language_synonym_db = {
      "py":     "python"
    , "js":     "javascript"
    , "md":     "markdown"
    , "m":      "matlab"
    , "octave": "matlab"
}

def highlight_code(code: str, language: str, verbose: bool = False) -> str:
    _code = ""
    result = None 
    if language == "": 
        _code = escape_html(code)
        # result =  err, _code
        result = f"""<div class="source-code">{_code}</div>"""
    else:
        try:
            language = _language_synonym_db.get(language, language)
            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter()
            ## print(f" [TRACE] Highlight code for '{name}' Ok.")
            _code =  highlight(code, lexer, formatter)
            result = _code
            ## breakpoint()
        except pygments.util.ClassNotFound:
            if verbose:
                print(f" [TRACE] Warning not found Python's pygment lexer for '{language}'")
            _code =  escape_html(code)
            result = f"""<div class="source-code">{_code}</div>"""
            ## resut = err, _code
    return result 

def file_contains(fileName: str, query: str, opt = "exact"):
    """Check whether a file (full path) contains a queyr string.
    Returns true if file contains a query string.
    NOTE: This function is case-indepedent.
    """
    with open(fileName) as fd:
        result = False
        query = query.lower()
        # Split whitespace
        queries = query.split()
        queries_ = queries.copy()
        # WARNING: Never read the whole file to memory, becasue
        # if the file is 1 GB, then 1 GB memory will be consumed,
        # what can case OOM (Out-Of-Memory) issues and slow down
        # the server.
        while line := fd.readline():
            # Ignore case
            if opt == "exact" and query in line.lower():
                result = True
                break
            # (OR) Returns true if is the file contains at
            # at least one word of the query.
            elif opt == "or_all":
                for q in queries:
                    if q in line.lower():
                        result = True
                        break
            # (AND) Returns treu if the file contains all words
            # from the input query
            elif opt == "and_all":
                for q in queries:
                    if q in line.lower() and q in queries_:
                        queries_.remove(q)
                if len(queries_) == 0:
                    result = True
                    break
        return result

def grep_file(fileName: str, query: str):
    """Return lines of a file that contains a given query string."""
    query = query.lower()
    lines = []
    n = 1
    with open(fileName) as fd:
        while line := fd.readline():
            if query in line.lower():
                lines.append((n, line))
            n += 1
    return lines  

def replace_ci(text, entry, replacement):
    """Case insensitive text replacement"""
    out = re.sub(re.escape(entry), replacement, text, flags = re.IGNORECASE)
    return out

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

class TempSSLCert:

    def __init__(self) -> None:
        self._tmp_keyfile = None
        self._tmp_certfile = None

    def __enter__(self):
        import tempfile
        import datetime
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        key = rsa.generate_private_key( public_exponent=65537, key_size=2048, )
        # Various details about who we are. For a self-signed certificate the
        # subject and issuer are always the same.
        subject = issuer = x509.Name([
              x509.NameAttribute(NameOID.COUNTRY_NAME, "US")
            , x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California")
            , x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco")
            , x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company")
            , x509.NameAttribute(NameOID.COMMON_NAME, "mysite.com")
        ])
        # Our certificate will be valid for 2000 days
        end_date =  datetime.datetime.now(datetime.timezone.utc) + \
            datetime.timedelta(days=2000)
        cert = ( x509.CertificateBuilder()
		     .subject_name( subject)
		     .issuer_name( issuer )
		     .public_key( key.public_key() )
		     .serial_number( x509.random_serial_number() )
		     .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
		     .not_valid_after(end_date)
		     .add_extension(
		        x509.SubjectAlternativeName([x509.DNSName("localhost")])
		      , critical=False,)
		# Sign our certificate with our private key
			 .sign(key, hashes.SHA256())
	        )
        self._tmp_keyfile  = tempfile.NamedTemporaryFile(delete=False)
        self._tmp_certfile = tempfile.NamedTemporaryFile(delete=False)
        with open(self._tmp_keyfile.name, "wb") as f:
            f.write(key.private_bytes(
                  encoding=serialization.Encoding.PEM
                , format=serialization.PrivateFormat.TraditionalOpenSSL
                , encryption_algorithm=serialization.NoEncryption()
                ##, encryption_algorithm=serialization.BestAvailableEncryption(b"")
                ))
        with open(self._tmp_certfile.name, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        ## print(" [TRACE] Enter context")
        return self 
    
    def __exit__(self, exc_type, exc_value, traceback):
        import os
        self._tmp_certfile.close()
        os.unlink(self._tmp_certfile.name)
        self._tmp_keyfile.close()
        os.unlink(self._tmp_keyfile.name)
        ## print(" [TRACE] Exit context ok")
        return True 
    
    def certkey(self):
        """Return tuple containing certificate and key"""
        return (self._tmp_certfile.name, self._tmp_keyfile.name)


__all__ = (  "escape_html"
           , "escape_url"
           , "highlight_code"
           , "file_contains"
           , "expand_path"
           , "get_wiki_path"
          )