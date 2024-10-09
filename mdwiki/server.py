import os
import bottle
from bottle import route, run
from bottle import static_file, route, auth_basic, request
import mdwiki.utils as utils
import mdwiki.mparser as mparser 

BASE_PATH = utils.get_wiki_path()

#  For setting a username and password, just 
# set the environment variable LOGIN, 
# export LOGIN="<USERNAME>;<PASSWORD>"
#
LOGIN = os.getenv("WIKI_LOGIN") or ""
USERNAME = ""
PASSWORD = ""
if LOGIN != "": 
    t = LOGIN.split(";")
    if len(t) == 2:
        USERNAME = t[0]
        PASSWORD = t[1]

def is_authhenticated(user, passwd):
    print(" [TRACE] LOGIN = ", LOGIN)
    breakpoint()
    # Disable Login if environment variable is not set 
    if LOGIN == "": 
        return True 
    is_auth = user == USERNAME and passwd == PASSWORD 
    return is_auth

##@auth_basic(is_authhenticated)
@route("/pages")
def route_pages():
    query = request.query.get("search") or ""
    highlight =  f"#:~:text={ utils.encode_url(query) }" if query != "" else ""
    files = []
    if query == "":
        files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md")]
    else:
        files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md") \
                 and utils.file_contains(utils.get_wiki_path(f), query)]
                 ##and utils.file_contains(os.path.join(BASE_PATH, f), query)]
    sorted_files = sorted(files)
    pages = [f.split(".")[0] for f in sorted_files]
    content =  "\n".join([f"""<li><a href="/wiki/{f}{highlight}" target="_blank" class="link-internal">{f}</a></li>""" for f in pages])
    content = f"""<h1>Markdown Wiki Pages</h1>\n<ul>\n{content}\n</ul>"""
    content = f"""
        <form>
            <label for="site-search-bar">Search all Markdown Files</label>
            <br>
            <input type="search" 
                   id="site-search-bar" 
                   name="search"
                   placeholder="Search..."
                   value="{query}"
                   />
            <button>Search</button>
        </form>
        """ + content
    html = mparser.fill_template("Index Page", content, "")
    return html

@route("/")
def route_index_page():
    bottle.redirect("/wiki/Index")

@bottle.get("/wiki/img/<filepath>")
def route_wiki_image(filepath):
    ## print(" [TRACE] Enter filepath route => filepath = ", filepath)
    root = utils.get_wiki_path("images")
    ## print(" [TRACE] root = ", root)
    resp = static_file(filepath, root)
    ## print(" [TRACE] resp = ", resp)
    return resp

@route("/wiki/<page>")
##@auth_basic(is_authhenticated)
def route_wiki_page(page):
    mdfile = os.path.join(BASE_PATH, page + ".md")
    ## print(" [TRACE] mdfile = ", mdfile, "\n\n")
    if not os.path.exists(mdfile):
         return f"<h1>404 NOT FOUND PAGE: {page}</h1>"
    headings = []
    with open(mdfile) as fd:
        inp = fd.read()
        headings = mparser.get_headings(inp)
    root = mparser.make_headings_hierarchy(headings)
    ## breakpoint()
    toc = mparser.headings_to_html(root)
    # TOC - Table of Contents
    ## toc = ""
    ## for (label, id, _) in headings:
    ##      toc += f"""<li ><a href="#{id}" class="link-internal" >{label}</a></li>"""
    ## toc = f"<lu>\n{toc}\n</lu>"
    html = mparser.mdfile_to_html(mdfile, page, toc)
    mparser.make_headings_hierarchy(headings)
    return html
     

@auth_basic(is_authhenticated)
def hello():
    return "Hello World!"

