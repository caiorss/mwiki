import re
from typing import List, Tuple, Dict
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

import mdwiki
import mdwiki.utils as utils
import mdwiki.plugins 

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
	.use(container_plugin, name = "{tip}",  render = render_container_tip)
	.use(container_plugin, name = "{note}")
    # Defintion of math concept or theorem 
	.use(container_plugin, name = "{def}")
	.use(container_plugin, name = "{theorem}")
    .use(myst_block_plugin)
    .use(myst_role_plugin)
    .use(mdwiki.plugins.wiki_text_highlight_plugin)
    .use(mdwiki.plugins.wiki_image_plugin)
    .use(mdwiki.plugins.wiki_link_plugin)
   # .use(fieldlist_plugin)
    .enable('table')
    .enable('strikethrough')
    .enable("myst_role")
    .enable("backticks")
)

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

MainTemplate = utils.read_resource(mdwiki, "template.html")

def fill_template(title: str, content: str, toc: str, query: str = ""):
    html = (
        MainTemplate
        .replace("{{body}}", content)
        .replace("{{title}}", title)
        .replace("{{toc}}", toc)
        .replace("{{query}}", query)
    )
    return html

def mdfile_to_html(inp_file, title, toc, query = ""):
    with open(inp_file) as fd:
        source: str = fd.read()
        tokens = MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        out    = node_to_html(ast)
        ## out = MdParser.render(inp)
        html = ( 
             MainTemplate
                .replace("{{body}}", out)
                .replace("{{title}}", title)
                .replace("{{toc}}", toc)
                .replace("{{query}}", query)
                
        )
        return html


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
    html = ""
    children = node.children
    tag = node.tag if hasattr(node, "tag") else ""
    if node.type == "root":
        html = "\n\n".join([ node_to_html(n) for n in children ])
    elif node.type == "myst_line_comment":
        if MYST_LINE_COMMENT:
            html = f"<!-- {node.content} -->"
        else:
            html = utils.escape_html(node.content)
    elif node.type == "front_matter":
        pass
    elif node.type == "footnote_block":
        ## html = MdParser.render(node)
        # TODO Implement rendering of footnote_block
        print(" [WARNING] Note implemented html rendering for foot_note_block = ", node)
        pass
    elif node.type == "footnote_ref":
        # TODO Implment rendering of footnote_ref
        print(" [WARNING] Note implemented html rendering for footnot_ref node = ", node)
        pass
    elif node.type == "html_block":
        html = node.content
    elif node.type == "html_inline":
        html = node.content
    elif node.type == "text":
        html = utils.escape_html(node.content)
    elif node.type == "code_inline":
        code = utils.escape_html(node.content)
        html = f"""<code>{code}</code>"""
    # Bold text 
    elif node.type == "strong":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"<strong>{inner}</strong>"
    # Italic text
    elif node.type == "em":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"<em>{inner}</em>"
    # Strikthrough 
    elif node.type == "s":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"<s>{inner}</s>"
    elif node.type == "hr":
        html = "<hr>"
    elif node.type == "softbreak":
        # Tag <br>
        html =  "\n"
    elif node.type == "hardbreak":
        # Tag <br>
        html =  "\n"
    elif node.type == "code_block":
        code = utils.escape_html(node.content)
        html = f"""<pre class="code_block">\n{code}\n</pre>"""
    elif node.type == "math_inline" or node.type == "math_single":
        # NOTE: It is processed by MathJax
        #html = f"""<span class="math-inline">${node.content}$</span>"""
        html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
    elif node.type == "inline":
        html = "".join([ node_to_html(n) for n in children ])
    elif node.type == "paragraph":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"""<p>\n{inner}\n</p>"""
        ## print(" [DEBUG] paragraph = \n", html)
    elif node.type == "heading":
        title =  node.children[0].content
        anchor  = "H_" + title.replace(" ", "_")
        ## tokens[idx].attrSet("class", "document-heading anchor")
        ## tokens[idx].attrSet("id", anchor) 
        value = utils.escape_html(title)
        link = f"""<a class="link-heading" href="#{anchor}">¶</a>"""
        html = f"""<{tag} id="{anchor}" class="document-heading anchor">{value} {link}</{tag}>"""
        ## print(" [TRACE] heading = ", html)
    elif node.type == "math_block":
        html = """<div class="math-block anchor"> \n$$\n""" \
            + utils.escape_html(node.content) + "\n$$\n</div>"
        ## print(" [TRACE] math_block = \n", html)
    elif node.type == "blockquote":
        inner = "\n".join([ node_to_html(n) for n in children ])
        # Remove Obsidian tag [!qupte]
        inner = inner.replace("[!quote]", "")
        html  = f"""<blockquote>\n{inner}\n</blockquote>"""
    elif node.type.startswith("container_"):
        cond  =  len(children) >= 1 and children[0].type == "paragraph"
        first = children[0].children[0].content if cond else None 
        metadata = {}
        if first:
            _, metadata  = get_code_block_directives(first) 
        ## print(" [TRACE] metadata = ", metadata)
        class_ = metadata.get("class") or ""
        is_dropdown = class_ == "dropdown"
        label = f'id="{x}"' if (x := metadata.get("label")) else ""
        ## css_class = x if (x := metadata.get("class")) else ""
        style = f'style="background: {x};"' if (x := metadata.get("background")) else ""
        admonition_type = node.type.strip("container_").strip("{").strip("}")
        admonition_title = node.info.strip("{" + admonition_type + "}").strip()
        if admonition_type == "def":
            admonition_title = f"DEFINITION: <strong>({admonition_title})</strong> "
        elif admonition_type == "theorem":
            admonition_title = f"THEOREM: <strong>({admonition_title})</strong> "
        else:
            rest = "" if admonition_title == "" else ": " + admonition_title
            admonition_title = admonition_type.title() + rest 
        attrs =  f""" {label} class="{admonition_type} admonition anchor" {style}""".strip()
        inner = ""
        if metadata == {}:
            inner = "".join([ node_to_html(n) for n in children ])
        else:
            inner = "".join([ node_to_html(n) for n in children[1:] ])
        title = f"""\n<span class="admonition-title">{admonition_title}</span>\n""" \
                if admonition_title != "" else ""
        if is_dropdown:
            html = ( f"""<div {attrs}>""" 
                     f"""<details>\n<summary>{title}</summary>""" 
                     f"""\n<div class="details-content">\n{inner}\n</div> <!-- EoF div.details-content -->""" 
                      """\n</details>""" 
                      """\n</div>"""
                    )
        else:
            html = f"""<div {attrs}>{title}{inner}\n</div>"""
        ##print(" [TRACE] container = \n", html)
        ##breakpoint()
    elif node.type == "link":
        inner = "".join([ node_to_html(n) for n in children ])
        href =  node.attrs.get("href") or ""
        attrs = "" 
        if href.startswith("#"):
            attrs = """ class="link-internal" """
        else:
            attrs = """ target="_blank" class="link-external" rel="noreferrer noopener nofollow" """
        html = f"""<a href="{href}" {attrs}>{inner}</a>"""
    elif node.type == "wikilink_inline":
        page = node.content
        html = f"""<a href="/wiki/{page}" class="link-internal wiki-link">{page}</a>"""
    elif node.type == "wiki_text_highlight_inline":
        text = utils.escape_html(node.content)
        html = f"""<span class="text-highlight">{text}</span>"""
    elif node.type == "wiki_image":
        src = node.content
        html = f"""<img class="wiki-image anchor" src="/wiki/img/{src}">"""
    elif node.type == "image":
        src = node.content
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"""<img class="external-image anchor" src="{src}" alt="{inner}" >"""
    # Code block with ```<CODE>```
    elif node.type == "fence":
        assert node.tag == "code"
        info = node.info if node.info != "" else "text" 
        if info == "{math}":
            content, directives = get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = f"""<div class="math-block anchor" {label} > \n$$\n""" \
                + utils.escape_html(content) + "\n$$\n</div>"
        else:
            code = utils.highlight_code(node.content, language = info)
            html = f"""<pre>\n<code class="language-{info.strip()}">{code}</code>\n</pre>"""
    elif node.type == "bullet_list":
        inner = "\n".join([ node_to_html(n) for n in children ])
        html = f"""<ul class="">\n{inner}\n</ul>"""
    elif node.type == "ordered_list":
        inner = "\n".join([ node_to_html(n) for n in children ])
        html = f"""<ol class="anchor">\n{inner}\n</ol>"""
    elif node.type == "list_item":
        if len(children) >= 1 and children[0].type == "paragraph":
            first = node_to_html(children[0].children[0])
            rest = "".join([ node_to_html(n) for n in children[1:] ])
            inner = first + " " + rest
        else:
            inner = "".join([ node_to_html(n) for n in children ])
        html = f"""<li>\n{inner}\n</li>"""
    # Definition list <dt>
    elif node.type == "dl":
        inner = "\n".join([ node_to_html(n) for n in children ])
        html = f"""<dl class="anchor">\n{inner}\n</dl>"""
        ## breakpoint()
        print(" [TRACE] definition list => html = \n", html)
    elif node.type == "dt":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"""<dt class="anchor">{inner}</dt>"""
    elif node.type == "dd":
        if len(children) == 1 and children[0].type == "paragraph":
            inner = node_to_html(children[0].children[0])
        else:
            inner = "".join([ node_to_html(n) for n in children ])
        html = f"""<dd class="anchor">{inner}</dd>"""
    elif node.type == "table":
        inner = "\n ".join([ node_to_html(n) for n in children ])
        html = f"""\n<table>\n{inner}\n</table>"""
    # Table body 
    elif node.type == "tbody":
        inner = "\n ".join([ node_to_html(n) for n in children ])
        html = f"""\n<tbody>\n{inner}\n</tbody>"""
    # Table element
    elif node.type == "thead":
        inner = "\n ".join([ node_to_html(n) for n in children ])
        html = f"""\n<thead>\n{inner}\n</thead>"""
    # Table row
    elif node.type == "tr":
        inner = "\n ".join([ node_to_html(n) for n in children ])
        html = f"""\n<tr>\n{inner}\n</tr>"""
    # Table element
    elif node.type == "th":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"""\n<th>{inner}</th>"""
    # Table data
    elif node.type == "td":
        inner = "".join([ node_to_html(n) for n in children ])
        html = f"""\n<td>{inner}</td>"""
    elif node.type == "myst_role":
        role = node.meta.get("name", "")
        content = utils.escape_html(node.content)
        ## MyST math role. Exmaple: {math}`f(x) = \sqrt{x^2 - 10x}`
        if role == "math":
            html = f"""<span class="math-inline">\\({content}\\)</span>"""
        # MyST sub role for superscript H{sub}`2`O compiles to H<sub>2</sub>O
        elif role == "sub":
            html = f"""<sub>{content}</sub>"""
        # MyST sub role for superscript 4{sup}`th` compiles to 4<sup>th</sup>O
        elif role == "sup":
            html = f"""<sup>{content}</sup>"""
        else:
            raise NotImplementedError(f"Rendering MyST role '{role} not implemented yet.")
        ##breakpoint()
    else:
        ## print(" Note implemented for ", node)
        ## breakpoint()
        raise NotImplementedError(f"Not implemented for node of type {node.type} of object {node}")
    return html