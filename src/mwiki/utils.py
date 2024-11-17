from importlib.resources import Package
import os
import sys
import re
import urllib.parse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.util
from typing import IO, Any, List, Dict, Optional, Tuple 

def mkdir(path: str):
    """Create directory if it does not exist yet."""
    try:
      os.makedirs(path)
    except OSError:
      pass

def is_os_linux_or_bsd() -> bool:
	"""Returns true if the current Linux or BSD."""
	output = "linux" in sys.platform or "bsd" in sys.platform
	return output

def is_os_windows() -> bool:
	"""Returns true if the current OS is Windows NT."""
	output = "windows" in sys.platform or "win" in sys.platform
	return output

def is_os_macos() -> bool:
	"""Return true if the current OS (Operating System) is MacOSX."""
	output = "darwin" in sys.platform
	return output

def is_os_unix() -> bool:
    """Return true if the current operating systems is a unix-like OS."""
    for x in ["linux", "bsd", "darwin"]:
         if x in sys.platform:
            return True
    return False

def xdg_config_home() -> str:
	"""Return OS-specific base path user-editable cofiguration files."""
	out = ""
	if is_os_linux_or_bsd(): 
		HOME = os.getenv("HOME")
		tmp = os.getenv("XDG_CONFIG_HOME") or ".config"
		out = os.path.join(HOME, tmp)
	elif is_os_windows(): 
		out = os.getenv("RoamingAppData")
	elif is_os_macos(): 
		out = os.path.join(HOME, "Library/Application Support")
	else:
		msg = f"Not implemented for sys.platform = {sys.platform}"
		raise NotImplementedError(msg)
	return out

def xdg_data_home() -> str:
	"""Return OS-specific base path of program data."""
	out = ""
	if is_os_linux_or_bsd(): 
		HOME = os.getenv("HOME")
		tmp = os.getenv("XDG_DATA_HOME") or ".local/share"
		out = os.path.join(HOME, tmp)
	elif is_os_windows(): 
		out = os.getenv("LocalAppData")
	elif is_os_macos(): 
		out = os.path.join(HOME, "Library/Application Support")
	else:
		msg = f"Not implemented for sys.platform = {sys.platform}"
		raise NotImplementedError(msg)
	return out

def xdg_cache_dir() -> str:
	"""Return OS-specific base path of cache directory."""
	out = ""
	if is_os_linux_or_bsd(): 
		HOME = os.getenv("HOME")
		tmp = os.getenv("XDG_CACHE_HOME") or ".cache"
		out = os.path.join(HOME, tmp)
	elif is_os_windows(): 
		out = os.getenv("LocalAppData")
	elif is_os_macos(): 
		out = os.path.join(HOME, "Library/Application Support")
	else:
		msg = f"Not implemented for sys.platform = {sys.platform}"
		raise NotImplementedError(msg)
	return out

def project_config_dir(project: str) -> str:
    """Return path to project configuration folder."""
    base = xdg_config_home() 
    output = os.path.join(base, project)
    return output

def project_data_dir(project: str) -> str:
    """Return path to project configuration folder."""
    base = xdg_data_home() 
    output = os.path.join(base, project)
    return output

def project_cache_dir(project: str) -> str:
    """Return path to project cache folder."""
    base = xdg_cache_dir() 
    output = os.path.join(base, project)
    return output

def open_project_config_dir(project, file, mode = "", fpath: str = "") -> IO[Any]:
    """Open file for reading or writing in project directory of config files."""
    path = project_config_dir(project)
    mkdir(path)
    pfile = os.path.join(path, fpath, file)
    path_ = os.path.join(path, fpath)
    mkdir(path_)
    fd = open(pfile, mode)
    return fd 

def open_project_data_dir(project: str, file: str, mode: str = "", fpath: str = "") -> IO[Any]: 
    """Open file for reading or writing in project data dir."""
    path = project_data_dir(project)
    mkdir(path)
    path_ = os.path.join(path, fpath)
    mkdir(path_)
    pfile = os.path.join(path, fpath, file)
    fd = open(pfile, mode)
    return fd 

def open_project_cache_dir(project: str, file: str, mode: str = "", fpath: str = "") -> IO[Any]: 
    """Open file for reading or writing in project cache dir."""
    path = project_cache_dir(project)
    mkdir(path)
    path_ = os.path.join(path, fpath)
    mkdir(path_)
    pfile = os.path.join(path, fpath, file)
    fd = open(pfile, mode)
    return fd 

def project_config_path(project: str, path: str = "") -> str:
    out = os.path.join(project_config_dir(project), path)
    return out 

def project_data_path(project: str, path: str = "") -> str:
    out = os.path.join(project_data_dir(project), path)
    return out 

def project_cache_path(project: str, path: str = "") -> str:
    out = os.path.join(project_cache_dir(project), path)
    return out 

def file_project_config_dir_exists(project: str, file: str, fpath: str = "") -> bool:
    """Return true if file exists in project config directory"""
    path = project_config_dir(project)
    pfile = os.path.join(path, fpath, file)
    out = os.path.isfile(pfile)
    return out 

def file_project_data_dir_exists(project: str, file: str, fpath: str = "") -> bool:
    """Return true if file exists in project data directory"""
    path = project_data_dir(project)
    pfile = os.path.join(path, fpath, file)
    out = os.path.isfile(pfile)
    return out 

def file_project_cache_dir_exists(project: str, file: str, fpath: str = "") -> bool:
    """Return true if file exists in project cache directory"""
    path = project_cache_dir(project)
    pfile = os.path.join(path, fpath, file)
    out = os.path.isfile(pfile)
    return out 

def read_resource(module: Package, resource_file: str) -> str:
    """Read resource file packaged with a given module."""
    import importlib.resources
    data = ""
    with importlib.resources.open_text(module, resource_file) as fd:
        data =  fd.read()
    return data

def escape_html(code) -> str:
    """Escape html code."""
    code = code.replace("&", "&amp;")\
                    .replace("<", "&lt;")\
                    .replace(">", "&gt;")\
                    .replace('"', "&quot;")\
                    .replace("'", "&apos;")
    return code

def escape_url(url: str) -> str:
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
    """"Performs server-side code syntax of source code.
    This function is a high level wrapper for Pygment package.
    """
    _code = ""
    result = None 
    if language == "": 
        _code = escape_html(code)
        # result =  err, _code
        result = f"""<div class="source-code">{_code}</div>"""
    else:
        try:
            language = _language_synonym_db.get(language, language)
            lexer = get_lexer_by_name(language, stripall = True)
            formatter = HtmlFormatter(linelos = True)
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

def normalize_text(text: str) -> str:
    """Remove accents, such as ú or ç for making searching easier."""
    out = (text 
                .replace("ã", "a")
                .replace("á", "a")
                .replace("à", "a")
                .replace("â", "a")
                .replace("ó", "o")
                .replace("ô", "o")
                .replace("í", "i")
                .replace("é", "e")
                .replace("ê", "e")
                .replace("ú", "u")
                .replace("ç", "c")
            )
    return out

_ENGLISH_STOP_WORDS = [ 
                "and", "or", "any", "of", "some"
             , "in", "at", "on", "off", "our"
             , "your", "we", "yours", "yourself"
             , "his", "he", "himself", "her", "hers"
             , "it", "its", "itself", "they", "them"
             , "what", "which", "whom", "that", "these"
             , "those" 
             ]


def file_contains(fileName: str, query: str, opt = "and_all") -> bool:
    """Check whether a file (full path) contains a queyr string.
    Returns true if file contains a query string.
    NOTE: This function is case-indepedent.
    """
    with open(fileName) as fd:
        result = False
        basename = normalize_text(os.path.basename(fileName).lower())
        ## print(f" [TRACE] fileName = {fileName} ; basename = {basename}")
        query = normalize_text(query.lower())
        # Split whitespace
        ## queries = query.split()
        queries = [ x for q in query.split() 
                    if (x := normalize_text(q))  not in _ENGLISH_STOP_WORDS  ]
        queries_ = queries.copy()
        score = 0
        # WARNING: Never read the whole file to memory, becasue
        # if the file is 1 GB, then 1 GB memory will be consumed,
        # what can case OOM (Out-Of-Memory) issues and slow down
        # the server.
        while line := fd.readline():
            line_ = normalize_text(line.lower())
            # Ignore case
            if opt == "exact" and query in line_ :
                result = True
                break
            # (OR) Returns true if is the file contains at
            # at least one word of the query.
            elif opt == "or_all":
                for q in queries:
                    if q in line_: 
                        score += 1
                        result = True
                        ##break
            # (AND) Returns treu if the file contains all words
            # from the input query
            elif opt == "and_all":
                for q in queries:
                    if (q in line_ and q in queries_):
                        queries_.remove(q)
                    if (q in basename and q in queries_):
                        score += 2
                        queries_.remove(q)
                if len(queries_) == 0:
                    score += 1
                    queries_ =  queries.copy() 
                    result = True
                    ##break
        ## if score != 0:
        ##     print(f" [DEBUG] score = {score} ; file =  {fileName} ")
        return score

def grep_file(fileName: str, query: str) -> List[str]:
    """Return lines of a file that contains a given query string."""
    query = normalize_text(query.lower())
    queries = [normalize_text(q) for q in query.split()]
    lines = []
    n = 1
    with open(fileName) as fd:
        while line := fd.readline():
            line_ = normalize_text(line.lower())
            for q in queries:
                if q in line_: 
                    lines.append((n, line))
            n += 1
            # if query in normalize_text(line.lower()):
            #     lines.append((n, line))
            n += 1
    return lines  

def replace_ci(text, entry, replacement) -> str:
    """Case insensitive text replacement"""
    out = re.sub(re.escape(entry), replacement, text, flags = re.IGNORECASE)
    return out

def expand_path(path: str) -> str:
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

def parse_int(x: Optional[str]) -> Optional[int]:
    if x is None: return None
    out: Optional[int] = -1
    try:
        out = int(x)
    except ValueError:
        out = None 
    return out

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