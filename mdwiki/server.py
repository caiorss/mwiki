import os
import glob
from bottle import route, run
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.texmath import texmath_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.container import container_plugin
from bottle import static_file, route, auth_basic, request
import bottle
import mdwiki
import mdwiki.utils as utils

"""
    MarkdownIt("js-default", 
			   {
				    "html": True 
				   ,"linkify": True 
				   ,"breaks": True 
				   ,"typographer": True 
				   ,"quotes": True 
				   
               })

"""

def highlight_code(code, name, attrs):
    """Highlight a block of code"""
    hcode = utils.highlight_code(code, language=name)
    return hcode 


md = (
    MarkdownIt("gfm-like", {
           "linkify":      True 
         , "typographer":  True 
         , "quotes":       True 
         , "html":         True 
         , "breaks":       True 
         , "highlight":    highlight_code
    })
    ## MarkdownIt('commonmark' ,{'breaks':True,'html':True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .use(texmath_plugin)
    .use(deflist_plugin)
    .use(tasklists_plugin)
	#.use(container_plugin)
    .enable('table')
    .enable('strikethrough')
)

## Inline Renderer 
def render_math_inline(self, tokens, idx, options, env):
	token = tokens[idx]
	assert token.type == "math_inline"
	## print(" [TRACE] token = ", token)
	html = r"""<span class="inline-math">\(""" + token.content + r"\)</span>"
	return html 


def render_math_block(self, tokens, idx, options, env):
	token = tokens[idx]
	## assert token.type == "math_inline"
	## print(" [TRACE] token = ", token)
	html = """<div class="math-block"> \n$$\n""" + token.content + "\n$$\n</div>"
	return html 

def render_blank_link(self, tokens, idx, options, env):
    tokens[idx].attrSet("target", "_blank")
    tokens[idx].attrSet("class", "link-external")
    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)


def render_heading_open(self, tokens, idx, options, env):
    content = tokens[idx + 1].children[0].content
    anchor  = "H_" + content.replace(" ", "_")
    tokens[idx].attrSet("class", "document-heading")
    tokens[idx].attrSet("id", anchor) 
    ## breakpoint()
    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)

def render_heading(self, tokens, idx, options, env):
    token = tokens[idx]
    breakpoint()
    pass 


## def render_internal(self, tokens, idx, options, env):
## 	token = tokens[idx]
## 	url = token.attrs["src"]
## 	if url.startsWith("internal://"):
## 		url_ = url.replace("internal://", "base/")
## 		return f"""<a href="{url_}"></a> """

# Register renderers 
md.add_render_rule("math_inline", render_math_inline)
md.add_render_rule("math_block", render_math_block)
md.add_render_rule("link_open", render_blank_link)
## md.add_render_rule("heading", render_heading)
md.add_render_rule("heading_open", render_heading_open)

### breakpoint()

## inp_file = "signals.md"
## out_file = "signals.html"

tpl = utils.read_resource(mdwiki, "template.html")


BASE_PATH =  utils.expand_path( os.getenv("WIKI_BASE_PATH") or "./")

def mdfile_to_html(inp_file, title, toc):
    with open(inp_file) as fd:
        inp = fd.read()
        out = md.render(inp)
        html = ( 
             tpl
                .replace("{{body}}", out)
                .replace("{{title}}", title)
                .replace("{{toc}}", toc)
                
        )
        return html
    ## with open(out_file, "w") as fo:
    ## 	fo.write(html)


def get_headings(markdown: str):
    tokens = md.parse(markdown)
    ast = SyntaxTreeNode(tokens)
    gen = ast.walk()
    sections = []
    while True:
        node = next(gen, None)
        if node is None: break  
        if node.type != "heading": continue
        heading = node.children[0].content
        anchor  = "H_" + heading.replace(" ", "_")
        level = sum([x == "#" for x in node.markup])
        item = (heading, anchor, level)
        sections.append(item)
        print(" [TRACE] heading = ", item)
        ##breakpoint()
    return sections



def make_headings_hierarchy(headings):
    """
    Algorithm from:  
        Question:  /parse-indented-text-tree-in-java 
        https://stackoverflow.com/questions/21735468

    Algorithm Pseudocode:

        intialize a stack
        push first line to stack
        while (there are more lines to read) {
         S1 = top of stack // do not pop off yet
         S2 = read a line
         if depth of S1 < depth of S2 {
          add S2 as child of S1
          push S2 into stack
         }
         else {
             while (depth of S1 >= depth of S2 AND there are at least 2 elements in stack) 
             {
                pop stack
                S1 = top of stack // do not pop
             }
             add S2 as child of S1
             push S2 into stack
         }
        }
        return bottom element of stack (stack[0])
    
    """
    stack = []
    def push(n):
        stack.append(n)
    def pop():
        if len(stack) == 0:
            raise RuntimeError("Stack is empty")
        top = stack.pop()
        return top 
    def top():
        return stack[-1]
    def empty(): return len(stack) == 0
    root = { "type": "ul", "level": -1, "children": [] }
    push(root)
    LEVEL = 2 
    for n in headings:
        (heading, anchor, level) = n 
        ## breakpoint()
        s1 = top()
        s2 = { "type": "li", "level": level
              , "anchor": anchor, "heading": heading, "children": [] }
        if s1["level"] < s2["level"]:
            # Add s2 as a child of s1 
            s1["children"].append(s2)
            # Push s2 onto stack
            push(s2)
        else:
            while s1["level"] >= s2["level"] and len(stack) >= 2:
                pop()
                s1 = top() 
            # Add s2 as a child of s1 
            s1["children"].append(s2)
            # Push s2 into the stack 
            push(s2)
    ## print(" [TRACE] root ", root)
    print(" ---------- generate_heading_html() ----------------")
    from pprint import pprint
    pprint(root)
    return root
    ## pprint(root)

    
def headings_to_html(root):
    children = root["children"]
    heading  = root.get("heading", "")
    anchor   = root.get("anchor", "") 
    temp = ""
    for n in children: 
        node_html = headings_to_html(n)
        temp += node_html 
    inner = f"<ul>\n{temp}\n</ul>" if len(children) !=0 else ""
    print("[ TRACE] inner = \n", inner)
    if heading == "":
        html = f"""<ul>{inner}</ul>"""
    else:
        _anchor = utils.encode_url(anchor)
        _heading = utils.escape_code(heading)
        html = f"""<li><a href="#{anchor}" class="link-internal" >{_heading}</a>\n{inner}</li>"""
    return html

#
#  For setting a username and password, just 
# set the environment variable LOGIN, 
# export LOGIN="<USERNAME>;<PASSWORD>"
#
LOGIN = os.getenv("LOGIN") or ""
USERNAME = ""
PASSWORD = ""
if LOGIN != "": 
    t = LOGIN.split(";")
    if len(t) == 2:
        USERNAME = t[0]
        PASSWORD = t[1]

def is_authhenticated(user, passwd):
    # Disable Login if environment variable is not set 
    if LOGIN == "": 
        return True 
    is_auth = user == USERNAME and passwd == PASSWORD 
    return is_auth

@route("/")
@auth_basic(is_authhenticated)
def route_index():
    query = request.query.get("search") or ""
    files = []
    if query == "":
        files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md")]
    else:
        files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md") \
                 and utils.file_contains(os.path.join(BASE_PATH, f), query)]
    sorted_files = sorted(files)
    pages = [f.split(".")[0] for f in sorted_files]
    content =  "\n".join([f"""<li><a href="/wiki/{f}" target="_blank" class="link-internal">{f}</a></li>""" for f in pages])
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
    html = ( 
         tpl
            .replace("{{body}}", content)
            .replace("{{title}}", "Index Patge")
            .replace("{{toc}}", "")
    )
    return html

@route("/wiki/<page>")
@auth_basic(is_authhenticated)
def route_wiki_page(page):
    mdfile = os.path.join(BASE_PATH, page + ".md")
    print(" [TRACE] mdfile = ", mdfile, "\n\n")
    if not os.path.exists(mdfile):
         return f"<h1>404 NOT FOUND PAGE: {page}</h1>"
    headings = []
    with open(mdfile) as fd:
        inp = fd.read()
        headings = get_headings(inp)
    root = make_headings_hierarchy(headings)
    ## breakpoint()
    toc = headings_to_html(root)
    # TOC - Table of Contents
    ## toc = ""
    ## for (label, id, _) in headings:
    ##      toc += f"""<li ><a href="#{id}" class="link-internal" >{label}</a></li>"""
    ## toc = f"<lu>\n{toc}\n</lu>"
    html = mdfile_to_html(mdfile, page, toc)
    make_headings_hierarchy(headings)
    return html
     

@auth_basic(is_authhenticated)
def hello():
    return "Hello World!"

