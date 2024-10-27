import glob
from markdown_it.tree import SyntaxTreeNode
import os 
import tempfile
import subprocess
from . import utils
from . import mparser

class TempDirectory:

    def __init__(self):
        self._prev = ""
        self._tempdir = None

    def name(self):
        out = self._tempdir.name
        return out 

    def __enter__(self):
        self._prev = os.getcwd()
        self._tempdir = tempfile.TemporaryDirectory()
        path = self._tempdir.name 
        os.chdir(path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._prev)
        self._tempdir.cleanup()
        return False

class Renderer:
    """Renderer abstract class providing a framework for concrete renderers classes.
    This renderer class is a basic building block for creating new renderer types,
    including html and LaTeX/PDF renderers.     
    """

    def __init__(self):
        self._handlers = {
              "root":                       self.render_root
            , "text":                       self.render_text
            , "strong":                     self.render_strong
            , "em":                         self.render_em_italic
            , "inline":                     self.render_inline 
            , "paragraph":                  self.render_paragraph
            , "s":                          self.render_strikethrough
            , "code_inline":                self.render_code_inline
            , "math_single":                self.render_math_single
            , "math_inline":                self.render_math_inline
            , "math_block":                 self.render_math_block
            , "softbreak":                  self.render_softbreak
            , "hardbreak":                  self.render_hardbreak
            , "hr":                         self.render_horizontal_line_hr
            , "heading":                    self.render_heading
            , "blockquote":                 self.render_blockquote
            , "link":                       self.render_link
            , "wikilink_inline":            self.render_wikilink_inline
            , "wiki_text_highlight_inline": self.render_wiki_text_highlight_inline
            , "wiki_image":                 self.render_wiki_image 
            # Code block 
            , "code_block":                 self.render_code_block
            , "fence":                      self.render_fence 
            # Bullet list and Ordered List 
            , "bullet_list":                self.render_bullet_list
            , "ordered_list":               self.render_ordered_list
            , "list_item":                  self.render_list_item
            # MyST Syntax Extensions
            , "myst_role":                  self.render_myst_role 
            , "myst_line_comment":          self.render_myst_line_comment
            # Render Definition List 
            , "dl":                         self.render_dl 
            , "dt":                         self.render_dt 
            , "dd":                         self.render_dd
            # Table 
            , "table":                      self.render_table
            , "thead":                      self.render_thead 
            , "tbody":                      self.render_tbody 
            , "tr":                         self.render_tr 
            , "th":                         self.render_th
            , "td":                         self.render_td
            # Html (Github-Flavoured Markdown)
            , "html_block":                 self.render_html_block
            , "html_inline":                self.render_html_inline
            , "image":                      self.render_image
            # Front matter (metadata)
            , "front_matter":               self.render_frontmatter
            # Footnotes 
            , "footnote_ref":               self.render_footnote_ref
            , "footnote_block":             self.render_footnote_block
        }
    
    def render(self, node: SyntaxTreeNode) -> str:
        handler = self._handlers.get(node.type)
        result = ""
        if handler is None:
            if "container_" in node.type:
                result = self.render_container(node)
            else: 
                raise RuntimeError(f"Rendering not implemented for node type '{node.type}' => node = {node} ")
        else:
            result = handler(node)
        return result

    def render_text(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_strong(self, node: SyntaxTreeNode) -> str:
        """Render bold text"""
        raise NotImplementedError() 

    def render_em_italic(self, node: SyntaxTreeNode) -> str:
        """Render emphasis text, aka Italic text"""
        raise NotImplementedError() 

    def render_strikethrough(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_root(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_softbreak(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_hardbreak(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_frontmatter(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_footnote_block(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_code_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 
    
    def render_math_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_math_single(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_math_block(self, node: SyntaxTreeNode) -> str: 
        raise NotImplementedError()
    
    def render_horizontal_line_hr(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_paragraph(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_heading(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_blockquote(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_container(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_link(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_wikilink_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_wiki_text_highlight_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_image(self, node: SyntaxTreeNode):
        raise NotImplementedError()

    def render_wiki_image(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_code_block(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_fence(self, node: SyntaxTreeNode) -> str:
        """Render code block using three backticks.

        Example:

        ```python
            for x in os.listdir("/"):
                print("file = ", x)
        ```
        """
        raise NotImplementedError()

    def render_bullet_list(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_ordered_list(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_list_item(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_myst_role(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_dl (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_dt (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 
        
    def render_dd(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_table(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_tbody (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 
    
    def render_thead (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_tr (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_th(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_td(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_html_block(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_html_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_myst_line_comment(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_frontmatter(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_footnote_block(self, ndoe: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

class HtmlRenderer(Renderer):

    def __init__(self, render_math_svg = False, embed_math_svg = False):
        super().__init__()
        self._render_math_svg =  render_math_svg  
        self._embed_math_svg = False
        self._myst_line_comment_enabled = False

    def enable_render_math_mathjax(self, value):
        self._render_math_svg = not value

    def enable_render_math_svg(self, value):
        self._render_math_svg = value 

    def render_root(self, node: SyntaxTreeNode) -> str:
        html = "\n\n".join([ self.render(n) for n in node.children ])
        return html
    
    def render_text(self, node: SyntaxTreeNode) -> str:
        html = node.content
        return html 

    def render_softbreak(self, node: SyntaxTreeNode) -> str:
        return "" 

    def render_hardbreak(self, node: SyntaxTreeNode) -> str:
        return "" 

    def render_inline(self, node: SyntaxTreeNode) -> str:
        html = "".join([ self.render(n) for n in node.children ])
        return html 

    def render_paragraph(self, node: SyntaxTreeNode) -> str:
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<p>\n{inner}\n</p>"""
        return html

    def render_strong(self, node: SyntaxTreeNode) -> str:
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"<strong>{inner}</strong>"
        return html 

    def render_em_italic(self, node: SyntaxTreeNode) -> str:
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"<em>{inner}</em>"
        return html

    def render_strikethrough(self, node: SyntaxTreeNode) -> str:
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"<s>{inner}</s>"
        return html        

    def render_heading(self, node: SyntaxTreeNode) -> str:
        title  = node.children[0].content
        anchor = "H_" + title.replace(" ", "_")
        value  = utils.escape_html(title)
        link   = f"""<a class="link-heading" href="#{anchor}">¶</a>"""
        tag    = node.tag if hasattr(node, "tag") else ""
        html   = f"""<{tag} id="{anchor}" class="document-heading anchor">{value} {link}</{tag}>"""
        return html  
 
    def render_html_inline(self, node: SyntaxTreeNode) -> str:
        html = node.content
        return html 
    
    def render_html_block(self, node: SyntaxTreeNode) -> str:
        html = node.content       
        return html 

    def render_blockquote(self, node: SyntaxTreeNode) -> str:
        inner = "\n".join([ self.render(n) for n in node.children ])
        # Remove Obsidian tag [!qupte]
        inner = inner.replace("[!quote]", "")
        html  = f"""<blockquote>\n{inner}\n</blockquote>"""
        return html 

    def render_math_block(self, node: SyntaxTreeNode) -> str:
        html = ""
        if self._render_math_svg:
            html = _latex_to_html(node.content, inline = False)
        else:
            html = """<div class="math-block anchor"> \n$$\n""" \
                 + utils.escape_html(node.content) + "\n$$\n</div>"
        return html 

    def render_math_inline(self, node: SyntaxTreeNode) -> str:
        # NOTE: It is processed by MathJax
        #html = f"""<span class="math-inline">${node.content}$</span>"""
        html = ""
        if self._render_math_svg:
            html = _latex_to_html(node.content, inline = True)
        else:
            html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        return html

    def render_math_single(self, node: SyntaxTreeNode) -> str:
        # NOTE: It is processed by MathJax
        #html = f"""<span class="math-inline">${node.content}$</span>"""
        html = ""
        if self._render_math_svg:
            html = _latex_to_html(node.content, inline = True)
        else:
            html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        ## html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        return html 

    def render_wiki_image(self, node: SyntaxTreeNode) -> str:
        assert node.type == "wiki_image"
        src = node.content
        html = f"""<img class="wiki-image anchor" src="/wiki/img/{src}  ">"""
        return html

    def render_link(self, node: SyntaxTreeNode) -> str:
        inner = "".join([ self.render(n) for n in node.children ])
        href =  node.attrs.get("href") or ""
        attrs = "" 
        if href.startswith("#"):
            attrs = """ class="link-internal" """
        else:
            attrs = """ target="_blank" class="link-external" rel="noreferrer noopener nofollow" """
        html = f"""<a href="{href}" {attrs}>{inner}</a>"""
        return html

    def render_wikilink_inline(self, node: SyntaxTreeNode) -> str:
        page = node.content
        html = f"""<a href="/wiki/{page}" class="link-internal wiki-link">{page}</a>"""
        return html 

    def render_myst_role(self, node: SyntaxTreeNode) -> str:
        role = node.meta.get("name", "")
        content = utils.escape_html(node.content)
        html = ""
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
        return html

    def render_code_inline(self, node: SyntaxTreeNode) -> str:
        code = utils.escape_html(node.content)
        html = f"""<code>{code}</code>"""
        return html

    def render_code_block(self, node: SyntaxTreeNode) -> str:
        assert node.type == "code_block"
        code = utils.escape_html(node.content)
        html = f"""<pre class="code_block">\n{code}\n</pre>"""
        return html

    def render_fence(self, node: SyntaxTreeNode) -> str:
        assert node.tag == "code"
        info = node.info if node.info != "" else "text" 
        if info == "{math}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = ""
            if self._render_math_svg:
                html = _latex_to_html(content, inline = False)
            else:
                html = f"""<div class="math-block anchor" {label} > \n$$\n""" \
                    + utils.escape_html(content) + "\n$$\n</div>"
        elif info == "{quote}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = f"""<blockquote {label} >\n{utils.escape_html(content)}\n</blockquote>"""
        # Compatible with Obsidian's pseudo-code plugin
        elif info == "pseudo" or info == "{pseudo}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            #content_ = utils.escape_html(content)
            html = f"""<pre {label} class="pseudocode" >\n{content}\n</pre>\n"""
        else:
            code = utils.highlight_code(node.content, language = info)
            html = f"""<pre>\n<code class="language-{info.strip()}">{code}</code>\n</pre>"""
        return html

    def render_wiki_text_highlight_inline(self, node: SyntaxTreeNode) -> str:
        assert node.type == "wiki_text_highlight_inline"
        ##inner = "".join([ self.render(n) for n in node.children ])
        inner = node.content
        html = f"""<span class="text-highlight">{inner}</span>"""
        ## breakpoint()
        return html 
    
    def render_image(self, node: SyntaxTreeNode):
        assert node.type == "image"
        src = node.attrs.get("src", "")
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<img class="external-image anchor" src="{src}" alt="{inner}" >"""
        return html 

    def render_bullet_list(self, node: SyntaxTreeNode) -> str:
        inner = "\n".join([ self.render(n) for n in node.children ])
        html = f"""<ul class="">\n{inner}\n</ul>"""
        return html 

    def render_ordered_list(self, node: SyntaxTreeNode) -> str:
        assert node.type == "ordered_list"
        inner = "\n".join([ self.render(n) for n in node.children ])
        html = f"""<ol class="anchor">\n{inner}\n</ol>"""
        return html 

    def render_list_item(self, node: SyntaxTreeNode) -> str:
        assert node.type == "list_item"
        if len(node.children) >= 1 and node.children[0].type == "paragraph":
            first = self.render(node.children[0].children[0])
            rest = "".join([ self.render(n) for n in node.children[1:] ])
            inner = first + " " + rest
        else:
            inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<li>\n{inner}\n</li>"""
        return html

    def render_dl(self, node: SyntaxTreeNode) -> str:
        assert node.type == "dl"
        inner = "\n".join([ self.render(n) for n in node.children ])
        html = f"""<dl class="anchor">\n{inner}\n</dl>"""
        return html 

    def render_dt(self, node: SyntaxTreeNode) -> str:
        assert node.type == "dt"
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<dt class="anchor">{inner}</dt>"""
        return html

    def render_dd(self, node: SyntaxTreeNode) -> str:
        assert node.type == "dd"
        if len(node.children) == 1 and node.children[0].type == "paragraph":
            inner = self.render(node.children[0].children[0])
        else:
            inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<dd class="anchor">{inner}</dd>"""
        return html

    def render_table(self, node: SyntaxTreeNode) -> str:
        assert node.type == "table"
        inner = "\n ".join([ self.render(n) for n in node.children ])
        html = f"""\n<table>\n{inner}\n</table>"""
        return html

    # Table body 
    def render_tbody(self, node: SyntaxTreeNode) -> str:
        assert node.type == "tbody"
        inner = "\n ".join([ self.render(n) for n in node.children ])
        html = f"""\n<tbody>\n{inner}\n</tbody>"""
        return html 

    # Table element
    def render_thead(self, node: SyntaxTreeNode) -> str:
        assert node.type == "thead"
        inner = "\n ".join([ self.render(n) for n in node.children ])
        html = f"""\n<thead>\n{inner}\n</thead>"""
        return html 

    # Table row
    def render_tr(self, node: SyntaxTreeNode) -> str:
        assert node.type == "tr"
        inner = "\n ".join([ self.render(n) for n in node.children ])
        html = f"""\n<tr>\n{inner}\n</tr>"""
        return html 

    # Table element
    def render_th(self, node: SyntaxTreeNode) -> str:
        assert node.type == "th"
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""\n<th>{inner}</th>"""
        return html 

    # Table data
    def render_td(self, node: SyntaxTreeNode) -> str:
        assert node.type == "td"
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""\n<td>{inner}</td>"""
        return html 

    def render_container(self, node: SyntaxTreeNode) -> str:
        cond  =  len(node.children) >= 1 and node.children[0].type == "paragraph"
        first = node.children[0].children[0].content if cond else None 
        metadata = {}
        if first:
            _, metadata  = mparser.get_code_block_directives(first) 
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
            inner = "".join([ self.render(n) for n in node.children ])
        else:
            inner = "".join([ self.render(n) for n in node.children[1:] ])
        iconsdb = {
              "info": """<img class="admonition-icon" src="/static/icon-info.svg"/> """
            , "note": """<img class="admonition-icon" src="/static/icon-info.svg"/> """
            , "tip":  """<img class="admonition-icon" src="/static/icon-lightbulb.svg"/> """
            , "warning":  """<img class="admonition-icon" src="/static/icon-warning1.svg"/> """
        }
        icon = iconsdb.get(admonition_type, "")
        title = f"""\n<span class="admonition-title">{icon}{admonition_title}</span>\n""" \
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
        return html
    
    def render_footnote_block(self, node: SyntaxTreeNode) -> str:
        print(" [WARNING] Note implemented html rendering for foot_note_block = ", node)
        return ""

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        print(" [WARNING] Note implemented html rendering for foot_note_block = ", node)
        return ""

    def render_frontmatter(self, node: SyntaxTreeNode) -> str:
        print(" [WARNING] Frontmatter not renderend to HTML")
        return "" 

    def render_horizontal_line_hr(self, node: SyntaxTreeNode) -> str:
        return "<hr>" 

    def render_myst_line_comment(self, node: SyntaxTreeNode) -> str:
        html = ""
        if self._myst_line_comment_enabled:
            html = f"<!-- {node.content} -->"
        else:
            html = utils.escape_html(node.content)       
        return html

svg_cache_folder = utils.project_cache_path("mwiki", "svg")
utils.mkdir(svg_cache_folder)

##def _latex_to_svg(eqtex, inline = False):
##    import subprocess
##    args =  ["tex2svg", eqtex ]
##    if inline: args.append("--inline")
##    proc = subprocess.run(args, capture_output=True , text=True)
##    if proc.returncode != 0: 
##        print(f"[WARN] tex2vg failed to process the latex equation:\n{eqtex}")
##    ## breakpoint()
##    output = proc.stdout #.decode("utf-8")
##    return output

_latex_template = r"""
\documentclass[12pt]{article}
\usepackage[paperwidth=12in, paperheight=12in]{geometry}
\pagestyle{empty}
\usepackage[dvipsnames]{xcolor}
\usepackage{cancel}
\usepackage{algcompatible}
\usepackage{algpseudocode}
\usepackage{algorithm}
%% \usepackage{algorithmic}
\definecolor{darkred}{rgb}{0.6,0,0}
\definecolor{darkgreen}{rgb}{0,0.6,0}
\definecolor{darkblue}{rgb}{0,0,0.6}
\definecolor{amber}{rgb}{0.9,0.6,0}
\usepackage{amsmath}
\usepackage{unicode-math}

 %% --- Begin Fonts Section --------%%
\setmainfont[Ligatures=TeX]{TeX Gyre Pagella}
\setmathfont{TeX Gyre Pagella Math}

 %% --- Macros ----------%%

\newcommand{\To}{ {\textbf{to}} } 
 
\DeclareMathOperator{\sgn}{sgn}
\DeclareMathOperator*{\argmax}{\mathrm{\arg\,max}\,}
\DeclareMathOperator*{\argmin}{\mathrm{\arg\,min}\,}

\begin{document}
{{math}}
\end{document}
""".strip()

def _latex_to_svg(latex: str, inline = False) -> str:
    """Compile Latex code or document to SVG images.
    This function abstract away the process of compiling 
    LaTeX, aka TeX, formulas to SVG images and returns 
    the SVG XML code.

    In order to this piece of code work, it is necessary 
    to installl Xelatex, pdfcrop and pdf2svg external executable.
    In Debian or Ubuntu-derivate Linux distributions, these 
    dependencies can be installed by using the following set
    of commands:

    ```sh
    $ sudo apt-get install -y texlive-extra-utils texlive-science
    $ sudo apt-get install -y pdf2svg
    ```
    """
    # Replace tabs by 4 spaces 
    code = latex
    code = code.replace("\t", "   ")
    # Remove empty lines
    code = "\n".join([x for x in code.splitlines() if x.strip() != '']).strip()
    code = ( code
                .replace(r"\begin{align}", r"\begin{split}") 
                .replace(r"\end{align}", r"\end{split}") 
                .replace(r"\begin{equation}", r"") 
                .replace(r"\end{equation}", r"") 
                .replace(r"\begin{equation*}", r"") 
                .replace(r"\end{equation*}", r"") 
                .replace(r"\begin{eqnarray}", r"\begin{split}") 
                .replace(r"\end{eqnarray}", r"\end{split}") 
                .replace(r"\begin{eqnarray*}", r"\begin{split}") 
                .replace(r"\end{eqnarray*}", r"\end{split}") 
                # Remove MathJax \require{cancel}
                .replace(r"\require{cancel}", "")
                # .replace(r"\begin{equation}", r"\[") 
                # .replace(r"\end{equation}", r"\]") 
                # .replace(r"\begin{equation*}", r"\[") 
                # .replace(r"\end{equation*}", r"\]") 
                .strip()
            )
    # Remove empty lines
    code = "\n".join([x for x in code.splitlines() if x.strip() != '']).strip()
    print(" [TRACE] code = \n", code)
    if inline:
        code = code.strip("$")
        if code != r"\LaTeX": 
            code = f"${code}$"
    else:
        if not code.startswith(r"\begin{align}") \
           and not code.startswith(r"\begin{align*}")\
           and not code.startswith(r"\begin{algorithm}"):
            # and not code.startswith(r"\begin{split}"):
            code = "\\[\n" + code + "\n\\]"
    tex  = _latex_template.replace("{{math}}", code)
    # breakpoint()
    print(" [TRACE] texfile = \n", tex)
    BASEFILE = "input"
    TEXFILE  = BASEFILE + ".tex"
    PDFFILE  = BASEFILE + ".pdf"
    CROP_PDFILE = BASEFILE + "-crop.pdf"
    SVGFILE     = BASEFILE + ".svg"
    ### print(" [TRACE] tex = ", tex)
    svg = ""
    with TempDirectory() as d:
        ## breakpoint()
        print(" [TRACE] within directory ", d.name())
        with open(TEXFILE, "w") as fd:
            fd.write(tex)
        print(" [INFO] Compiling with xelatex")
        proc = subprocess.run([  "xelatex"
                               , "-output-directory=."
                               , "-interaction=batchmode"
                              # , "-no-console"
                               , TEXFILE]
                               , capture_output=True , text=True)
        print(" [TRACE] proc = ", proc)
        ## breakpoint()
        if proc.returncode != 0:
            print(" [ERROR] Failed to compile latex formula ", latex)
            print(" [ERROR] stderr = ", proc.stderr)
            log = ""
            with open("input.log", "r") as fd:
                log = fd.read()
            print(f" [ERROR LOG FILE] input.log = \n{log}\n")
            ## breakpoint()
            return proc.stderr
        assert os.path.isfile(PDFFILE)
        proc = subprocess.run([  "pdfcrop" , PDFFILE ]
                               , capture_output=True , text=True)
        print(" [INFO] Croping PDF .... ")
        if proc.returncode != 0:
            print(f" [ERROR] Failed to crop pdf of latex formula:\n{latex}")
            return ""
        assert os.path.isfile(CROP_PDFILE)
        print(" [INFO] Turnin PDF into SVG .... ")
        proc = subprocess.run([ "pdf2svg" , CROP_PDFILE, SVGFILE ]
                               , capture_output=True , text=True)
        if proc.returncode != 0:
            print(f" [ERROR] Failed to turn pdf of latex formula into SVG. => \n{latex}")
            return ""
        with open(SVGFILE, "r") as fd:
            svg = fd.read()
        ##breakpoint()
    print(" [TRACE] Current directory after exit = ", os.getcwd())
    if svg == "": 
        print(" [ERROR] failed to compile latex = ", latex)
        ## breakpoint()
    return svg  

def _sha1_hash_string(text: str):
    import hashlib 
    data = text.encode("utf-8")
    hash = hashlib.sha1(data).hexdigest()
    return hash


def _get_image_file_from_latex(eqtext, inline = False, embed = False):
    """Get unique image file file name of latex formula.
    The file name is computed as the hash of the latex formula.
    """
    import os
    import os.path
    ## if eqtext in self._cache: return self._cache.get(eqtext)
    eqtext = eqtext.strip()
    hash =  _sha1_hash_string(eqtext)
    svgfile = hash + ".svg"
    #  svgfile = os.path.join(svg_cache_folder, eqhash) + ".svg"
    return hash, svgfile

def _latex_to_html(eqtext, inline = False, embed = False):
    eqhash, svgfile_ = _get_image_file_from_latex(eqtext, inline, embed) 
    html = ""
    if embed: 
        html = ""
        ## html = self._svg2b64_image(  svg
        ##                            , alt = utils.escape_html(eqtext)
        ##                            , inline = inline)
    else:
        klass = "inline-math" if inline else "math"
        alt = utils.escape_html(eqtext)
        html = f"""<a href="#{eqhash}"><img id="{eqhash}" class="{klass} anchor" src="/wiki/math/{svgfile_}" alt="{alt}" loading="lazy" ></a>"""
        ## html = f'<img class="{klass}" src="/wiki/math/{svgfile_}" alt="{alt}" loading="lazy" >'
        if not inline: 
            html = f"""<div class="math-container">\n{html}\n</div>"""
            ## print(" [DEBUG] math html = ", html)
    return html 
    

def _latex_to_html2(eqtext, inline = False, embed = False):
    """Compile LaTeX equations to SVG and store the images in cache folder."""
    import os
    import os.path
    ## if eqtext in self._cache: return self._cache.get(eqtext)
    eqtext = eqtext.strip()
    eqhash = _sha1_hash_string(eqtext)
    svgfile = os.path.join(svg_cache_folder, eqhash) + ".svg"
    svg = ""
    if os.path.isfile(svgfile):
        with open(svgfile, "r") as fd:
            svg = fd.read()
    # The condition svg == "" tries to compile latex to SVG file again 
    # if the variable svg is set to an empty string, which indicates
    # that the last compilation failed.
    ## breakpoint()
    if not os.path.isfile(svgfile) or svg == "": 
        print(f"\n[TRACE] Compiling equation to {svgfile}\nEquation= \n", eqtext)
        svg = _latex_to_svg(eqtext, inline)
        print("\n\n--------------------------------------")
        with open(svgfile, "w") as fd:
            fd.write(svg)
    html = ""
    if embed: 
        html = ""
        ## html = self._svg2b64_image(  svg
        ##                            , alt = utils.escape_html(eqtext)
        ##                            , inline = inline)
    else:
        klass = "inline-math" if inline else "math"
        alt = utils.escape_html(eqtext)
        svgfile_ = eqhash + ".svg"
        html = f"""<a href="#{eqhash}"><img id="{eqhash}" class="{klass}" src="/wiki/math/{svgfile_}" alt="{alt}" loading="lazy" ></a>"""
        if not inline: 
            html = f"""<div class="math-container">\n{html}\n</div>"""
            ## print(" [DEBUG] math html = ", html)
    return html 


__html_render = HtmlRenderer( render_math_svg = True)

def node_to_html(node: SyntaxTreeNode):
    html = __html_render.render(node)
    return html

def pagefile_to_html(pagefile: str):
    import re
    with open(pagefile) as fd:
        source: str = fd.read()
        ## source = re.sub(r"^$$", "\n$$", source) 
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        html    = node_to_html(ast)
        return html

def compile_pagefile_(pagefile: str):
    with open(pagefile) as fd:
        source: str = fd.read()
        ## source = re.sub(r"^$$", "\n$$", source) 
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        print(" [*] Comiling File: ", pagefile)
        # Get generator object to iterate over the AST
        # (Abstract Syntax Tree nods)
        gen = ast.walk()
        while True:
            node = next(gen, None)
            if node is None: break
            if node.type == "math_block":
                _latex_to_html2(node.content, inline = False)
            elif node.type == "math_inline" \
                or node.type == "math_single":
                 _latex_to_html2(node.content, inline = True)
            # Code block ```{math} ... ```
            elif node.type == "fence":
                assert node.tag == "code"
                info = node.info if node.info != "" else "text" 
                if info == "{math}":
                    content, directives = mparser.get_code_block_directives(node.content)
                    #label = f'id="{u}"' if (u := directives.get("label")) else ""
                    _latex_to_html2(content, inline = False)

        print(" [*]  Compilation Finished => File: ", pagefile)
        print("\n\n-------------------------------------------")

# Parallelb compilation with multiprocess 
def get_latex_expressions(pagefile: str):
    with open(pagefile) as fd:
        source: str = fd.read()
        ## source = re.sub(r"^$$", "\n$$", source) 
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        # Get generator object to iterate over the AST
        # (Abstract Syntax Tree nods)
        gen = ast.walk()
        mathblocks = []
        while True:
            node = next(gen, None)
            if node is None: break
            if node.type == "math_block":
                x = (node.content, False)
                mathblocks.append(x)
            elif node.type == "math_inline" \
                or node.type == "math_single":
                x = (node.content, True)
                mathblocks.append(x)
            # Code block ```{math} ... ```
            elif node.type == "fence":
                assert node.tag == "code"
                info = node.info if node.info != "" else "text" 
                if info == "{math}":
                    content, directives = mparser.get_code_block_directives(node.content)
                    #label = f'id="{u}"' if (u := directives.get("label")) else ""
                    x = (content, False)
                    mathblocks.append(x)
        return mathblocks

def compile_(x):
    out = _latex_to_html2(x[0], x[1])
    return out

def compile_pagefile(pagefile: str):
    import multiprocessing
    print(" [*] Comiling File: ", pagefile)
    equations = get_latex_expressions(pagefile)
    with multiprocessing.Pool(6) as p:
        p.map(compile_, equations) 
    print(" [*]  Compilation Finished => File: ", pagefile)
    print("\n\n-------------------------------------------")
        

def compile_folder(path_to_folder: str):
    pattern = os.path.join(path_to_folder, "*.md")
    files = glob.glob(pattern)
    print(" [***] Compiling Latex Formulas of Folder: ", path_to_folder)
    for f in files:
        compile_pagefile(f)
    print(" [***] Total Compilation Finished")