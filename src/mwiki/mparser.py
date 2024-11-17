import re
from typing import Any, List, Tuple, Dict
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.texmath import texmath_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.container import container_plugin
from mdit_py_plugins.field_list import fieldlist_plugin
# from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.attrs import attrs_plugin 
from mdit_py_plugins.attrs import attrs_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
import frontmatter
import yaml

import mwiki
import mwiki.utils as utils
import mwiki.plugins 

def highlight_code(code, name, attrs):
    """Highlight a block of code"""
    hcode = utils.highlight_code(code, language=name)
    return hcode 

def render_container_tip(self, tokens, index, options, env):
    print(" [TRACE] Enter fucntion reder_container_tip() ")
    ##breakpoint()
    html = ( '<div class="tip admonition anchor">'
             '\n<p class="tip-admonition-title">Tip</p>'
            )
    return html

MdParser = (
    MarkdownIt("gfm-like", {
           "linkify":      True 
         , "typographer":  True 
         , "quotes":       True 
         , "html":         True 
         #, "breaks":       True 
         , "highlight":    highlight_code
    })
    ## MarkdownIt('commonmark' ,{'breaks':True,'html':True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .use(texmath_plugin)
    .use(deflist_plugin)
    .use(tasklists_plugin)
    .use(attrs_plugin)
    .use(attrs_block_plugin)
	.use(container_plugin, name = "{tip}")
	.use(container_plugin, name = "{note}")
	.use(container_plugin, name = "{info}")
	.use(container_plugin, name = "{warning}")
    # Defintion of math concept or theorem 
	.use(container_plugin, name = "{def}")
	.use(container_plugin, name = "{theorem}")
    .use(myst_block_plugin)
    .use(myst_role_plugin)
    .use(mwiki.plugins.wiki_tag_plugin)
    .use(mwiki.plugins.wiki_text_highlight_plugin)
    .use(mwiki.plugins.wiki_embed_plugin)
    .use(mwiki.plugins.wiki_link_plugin)
   # .use(fieldlist_plugin)
    .enable('table')
    .enable('strikethrough')
    .enable("myst_role")
    .enable("backticks")
)

def parse_file(file: str) -> SyntaxTreeNode:
    with open(file, "r") as fd:
        source: str = fd.read()
        tokens = MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        return ast 
    
def parse_source(source: str) -> SyntaxTreeNode:
    tokens = MdParser.parse(source)
    ast    = SyntaxTreeNode(tokens)
    return ast 

## breakpoint()

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
	html = """<div class="math-block anchor"> \n$$\n""" + token.content + "\n$$\n</div>"
	return html 

def render_hyperlink(self, tokens, idx, options, env):
    """Render hyperlinks using the syntax [label](url)
    """
    token = tokens[idx]
    href = token.attrs.get("href") or ""
    if not href.startswith("#"):
        token.attrSet("target", "_blank")
        token.attrSet("class", "link-external")
        token.attrSet("rel", "noreferrer noopener nofollow")
    else:
        token.attrSet("class", "link-internal")
    ### breakpoint()
    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)


def render_heading_open(self, tokens, idx, options, env):
    content = tokens[idx + 1].children[0].content
    anchor  = "H_" + content.replace(" ", "_")
    tokens[idx].attrSet("class", "document-heading anchor")
    tokens[idx].attrSet("id", anchor) 
    ## breakpoint()
    # pass token to default renderer.
    return self.renderToken(tokens, idx, options, env)

def render_heading(self, tokens, idx, options, env):
    token = tokens[idx]
    ## breakpoint()
    pass 

def render_container_tip_open(self, tokens, index, options, env):
    html = ( '<div class="tip admonition anchor">'
             '\n<p class="tip-admonition-title">Tip</p>'
            )
    return html

def render_container_note_open(self, tokens, index, options, env):
    html = ( '<div class="note admonition anchor">'
             '\n<p class="note-admonition-title">Note</p>'
            )
    return html

def render_container_def_open(self, tokens, index, options, env):
    tok = tokens[index]
    title = tok.info.strip("{def}").strip() 
    # Label is the unique identifier of an AST element
    # it is similar to Html5 DOM id property.
    label_ = tok.attrs.get("label") 
    label  = f'id="{label_}"' if label_ else ""
    ## breakpoint()
    html = ( f'<div class="def admonition anchor" {label}>'
             # f'\n<p class="def-admonition-title"><b>DEFINITION:</b> {title}</p>'
             f'\n<p><u>DEFINITION:</u> <b>({title})</b></p>'
            )
    return html


def render_container_theorem_open(self, tokens, index, options, env):
    tok = tokens[index]
    title = tok.info.strip("{theorem}").strip() 
    # Label is the unique identifier of an AST element
    # it is similar to Html5 DOM id property.
    label_ = tok.attrs.get("label") 
    label  = f'id="{label_}"' if label_ else ""
    ## breakpoint()
    html = ( f'<div class="def admonition anchor" {label}>'
             ##f'\n<p class="theorem-admonition-title"><b>THEOREM:</b> {title}</p>'
             f'\n<p><u>THEOREM:</u> <b>({title})</b></p>'
            )
    return html

def get_code_block_directives(code: str) -> Tuple[str, Dict[str, str]]:
    _directive_pattern = re.compile(":(\S+):\s+(.*)")
    lines = code.splitlines()
    # Filter lines containing directives
    # :<directive>: <value>
    directives = dict([ (m.group(1), m.group(2).strip()) 
      for x in lines if (m := _directive_pattern.match(x)) ])
    ##print(" [TRACE] directive = ", directives)
    # Filter lines without directives
    content = "\n".join( [ x for x in lines if not _directive_pattern.match(x)] ) 
    out =  (content, directives)
    return out


_default_fencer_renderer = MdParser.renderer.rules.get("fence")

def render_code_block(self, tokens, index, options, env):
    """Implement some MyST code block markdown syntax

    For instance, it implements now the following syntax,
    that is rendered as a LaTeX expression/equation.

    ```{math}
    :label:  eq-uniquer-identifier-for-this-equation 

     \| v \|^2 = x^2 + y^2 + z^2 
    ```
    
    """
    ## print(" [TRACE] Enter render code block ")
    ## breakpoint()
    token = tokens[index]
    ## print(" [TRACE] token = ", token)
    assert token.type == "fence"
    ## breakpoint()
    if token.tag == "code" and token.block and token.info == "{math}":
        content, directives = get_code_block_directives(token.content)
        label = f'id="{u}"' if (u := directives.get("label")) else ""
        output = f"""<div class="math-block anchor" {label} > \n$$\n""" \
            + utils.escape_html(content) + "\n$$\n</div>"
    else:
        ## print(" [TRACE] Execute this branch")
        ## output = self.renderToken(tokens, index, options, env)
        output =  _default_fencer_renderer(tokens, index, options, env) 
    ## print(" [TRACE] output = ", output)
    return output

## breakpoint()




# Register renderers 
MdParser.add_render_rule("math_inline", render_math_inline)
MdParser.add_render_rule("math_block", render_math_block)
MdParser.add_render_rule("fence", render_code_block)
# MdParser.renderer.rules["fence"] = render_code_block

MdParser.add_render_rule("link_open", render_hyperlink)
## md.add_render_rule("heading", render_heading)
MdParser.add_render_rule("heading_open", render_heading_open)
MdParser.add_render_rule("container_{tip}", render_container_tip)
###MdParser.add_render_rule("container_{tip}_open", render_container_tip_open)
MdParser.add_render_rule("container_{note}_open", render_container_note_open)
MdParser.add_render_rule("container_{def}_open", render_container_def_open)
MdParser.add_render_rule("container_{theorem}_open", render_container_theorem_open)

_FrontMatter = frontmatter.Frontmatter()
_default_attr = {  "description": ""
                 , "subject":     ""
                 , "keywords":    ""
                 , "uuid":        ""
                 , "title":       ""
                 }

def get_pagefile_metadata(pagefile: str) -> Dict[str, Any]:
    metadata = _default_attr
    try:
        data     = _FrontMatter.read_file(pagefile)
        metadata = data.get("attributes", metadata)
    except yaml.scanner.ScannerError:
        metadata = _default_attr
    return metadata

def get_headings(markdown: str):
    tokens = MdParser.parse(markdown)
    ast = SyntaxTreeNode(tokens)
    gen = ast.walk()
    sections = []
    while True:
        node = next(gen, None)
        ## breakpoint() 
        if node is None: break  
        if node.type != "heading": continue
        heading = node.children[0].content
        anchor  = "H_" + heading.replace(" ", "_")
        level = sum([x == "#" for x in node.markup])
        item = (heading, anchor, level)
        sections.append(item)
        ## print(" [TRACE] heading = ", item)
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
    ## LEVEL = 2 
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
    ## print(" ---------- generate_heading_html() ----------------")
    ## from pprint import pprint
    ## pprint(root)
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
    inner = f"<ol>\n{temp}\n</ol>" if len(children) !=0 else ""
    ## print("[ TRACE] inner = \n", inner)
    if heading == "":
        html = f"""<ol>{inner}</ol>"""
    else:
        ## _anchor = utils.escape_url(anchor)
        _heading = utils.escape_html(heading)
        html = f"""<li><a href="#{anchor}" class="link-sidebar" >{_heading}</a>\n{inner}</li>"""
    return html



def disp(node: SyntaxTreeNode):
    """Helper function for displaying nodes in the Debugger"""
    info = f""" 
{node}
      node.type = {node.type}
      node.tag  = "{node.tag}"
     node.level = {node.level}
      node.info = "{node.info}"
     node.attrs = {node.attrs}
      node.meta = {node.meta}
   node.content = "{node.content}"
     node.block = {node.block}
    node.markup = "{node.markup}"
node.children() = {node.children}
"""
    print(info)

MYST_LINE_COMMENT = False

def node_to_html(node: SyntaxTreeNode):
    pass