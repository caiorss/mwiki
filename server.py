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
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.util

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
    ##if attrs:
    ##    rich.print(f"Ignoring {attrs=}")
    ### breakpoint()
    if name == "": return code
    try:
        lexer = get_lexer_by_name(name)
        formatter = HtmlFormatter()
        print(f" [TRACE] Highlight code for '{name}' Ok.")
        result = highlight(code, lexer, formatter)
        ## breakpoint()
        return result 
    except pygments.util.ClassNotFound:
        print(f" [TRACE] Warning not found Python's pygment lexer for '{name}'")
        return code


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


## inp_file = "signals.md"
## out_file = "signals.html"
inp_file = "sample.md"
## out_file = "sample.html"
tpl = open("template.html").read()


BASE_PATH = os.getenv("WIKI_BASE_PATH") or "./"

def mdfile_to_html(inp_file):
    with open(inp_file) as fd:
        inp = fd.read()
        out = md.render(inp)
        html = tpl.replace("{{body}}", out)
        return html
    ## with open(out_file, "w") as fo:
    ## 	fo.write(html)

from bottle import static_file, route

@route("/")
def route_index():
    files = [f for f in os.listdir(BASE_PATH) if f.endswith(".md")]
    sorted_files = sorted(files)
    pages = [f.split(".")[0] for f in sorted_files]
    html =  "\n".join([f"""<li><a href="/wiki/{f}">{f}</a></li>""" for f in pages])
    html = f"""<h1>Markdown Wiki Pages</h1>\n<ul>\n{html}\n</ul>"""
    return html


@route("/wiki/<page>")
def route_wiki_page(page):
    mdfile = os.path.join(BASE_PATH, page + ".md")
    if not os.path.exists(mdfile):
         return f"<h1>404 NOT FOUND PAGE: {page}</h1>"
    html = mdfile_to_html(mdfile)
    return html
     

@route('/hello')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    run(host='0.0.0.0', port=8060, debug=True)
