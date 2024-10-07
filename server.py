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


md = (
    MarkdownIt("gfm-like")
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
    files = glob.glob("*.md")
    pages = [f.split(".")[0] for f in files]
    html =  "\n".join([f"""<li><a href="/wiki/{f}">{f}</a></li>""" for f in pages])
    html = f"""<h1>Markdown Wiki Pages</h1>\n<ul>\n{html}\n</ul>"""
    return html

@route("/wiki/<page>")
def route_wiki_page(page):
    mdfile = page + ".md"
    if not os.path.exists(mdfile):
         return f"<h1>404 NOT FOUND PAGE: {page}</h1>"
    html = mdfile_to_html(mdfile)
    return html
     

@route('/hello')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    run(host='localhost', port=8060, debug=True)
