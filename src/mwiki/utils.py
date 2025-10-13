from importlib.resources import Package
import os
import sys
import re
import unicodedata
import hmac
import hashlib
import json
import datetime
import base64
import shutil
import json.decoder
import pathlib
import binascii
from typing import Optional
from typing import IO, Any, List, Dict, Optional, Tuple 
import urllib.parse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.util


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def strip_prefix(prefix: str, s: str):
    """Strip prefix of string."""
    out = s
    if s.startswith(prefix):
         out = s[len(prefix):]
    return out

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

def get_path_to_resource_file(module: Package, resource_file: str) -> pathlib.Path:
    module_path = pathlib.Path(module.__file__).resolve().parent
    path = module_path / resource_file
    return path 

def copy_resource_file(module: Package, resource_file: str, dest: pathlib.Path):
    src = get_path_to_resource_file(module,resource_file)
    shutil.copy(src, dest)

def copy_resource_files_ext(module: Package, file_extesion: str, dest: pathlib.Path):
    """Copy all module resource files to destination folder."""
    module_path = pathlib.Path(module.__file__).resolve().parent
    files       = module_path.glob(file_extesion)
    for f in files:
        shutil.copy(f, dest)
    

def copy_folder(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok = True)
    
def base64_encode(text: str) -> str:
    data = text.encode("utf-8")
    out = base64.b64encode(data).decode("utf-8")
    return out

def base64_decode(base64str: str) -> str:
    out = base64.b64decode(base64str).decode("utf-8")
    return out

def encode_json_to_base64(obj: any) -> str:
    """Encode jsonable data base64 string.

    Usage example:

    >>> data = {"timestamp": 1005205, "user": "dummy"}
    >>> out = encode_json_to_base64(data)
    >>> out
    'eyJ0aW1lc3RhbXAiOiAxMDA1MjA1LCAidXNlciI6ICJkdW1teSJ9'
    """
    json_str: str = json.dumps(obj)
    data = json_str.encode("utf-8")
    out = base64.b64encode(data).decode("utf-8")
    return out

def decode_json_from_base64(base64str: str) -> Optional[any]:
    """Decode jsonable data from base64 string.

    Usage example:

    >>> data = {"timestamp": 1005205, "user": "dummy"}
    >>> out = encode_json_to_base64(data)
    >>> out
    'eyJ0aW1lc3RhbXAiOiAxMDA1MjA1LCAidXNlciI6ICJkdW1teSJ9'
    >>> decode_json_from_base64(out)
    {'timestamp': 1005205, 'user': 'dummy'}

    """
    data = None
    try:
        json_str = base64.b64decode(base64str).decode("utf-8")
        data = json.loads(json_str)
    except (binascii.Error, json.decoder.JSONDecodeError, UnicodeDecodeError) as ex:
        pass
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
    """Encode URL"""
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

def generate_password(size: int = 20) -> str:
    """Generate an random alphanumeric password of given size."""
    import string 
    import random 
    result = ''.join(random.SystemRandom()\
                     .choice( string.ascii_uppercase + string.digits) 
                              for _ in range(size))
    return result 


def hmac_signature(secret: str, message: str) -> str:
    """Generate hmac signature of a particular message
    NOTE: HMAC stands for Hash-Based Message Authentication Code
    """
    signature = hmac.new( secret.encode("utf8")
                         , message.encode("utf8")
                         , hashlib.sha256).hexdigest()
    return signature

def hmac_compare(secret: str, message: str, expected_signature: str) -> bool:
    """Check whether a message is valid given its hmac signature"""
    signature = hmac_signature(secret, message)
    is_valid = hmac.compare_digest(signature, expected_signature)
    return is_valid

def now_utc_timestamp() -> int:
    utc = datetime.timezone.utc
    now = datetime.datetime.now(utc).timestamp()
    out = int(now)
    return out

def now_utc_timestamp_add_minutes(minutes: int) -> int:
    utc = datetime.timezone.utc
    now = datetime.datetime.now(utc)
    out = now + datetime.timedelta(minutes = minutes)
    out = int(out.timestamp())
    return out

def timestamp_has_expired(timestamp: int) -> bool:
    """Return true if the timestamp has expired."""
    now = now_utc_timestamp()
    has_expired = timestamp - now < 0
    return has_expired

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
