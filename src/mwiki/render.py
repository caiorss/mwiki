"""Rendering of MWiki to html and other formats."""
import glob
import json
import re 
import yaml                     # Python3 stdlib Yaml Parser
import pathlib
from typing import Optional, Tuple, List 
from markdown_it.tree import SyntaxTreeNode
import urllib.parse
import os 
import tempfile
import subprocess
from . import utils
from . import mparser

_STOP_SENTINEL = "{{STOP}}"

FOOTNOTES_DIV_FORWARD_REFERENCE = "{{{@FOOTNOTES-DIV-FOWARD-REFERENCE-TAG}}}"


def get_yoututbe_video_id(video_url_or_id: str) -> str:
    """Get video ID of a youtube video URL. 
    The input argument can either be a video URL or video ID.

     Example: 

    ```python
    >>> get_yoututbe_video_id("https://m.youtube.com/watch?v=T95k9m5zcX4&pp=0gcJCdgAo7VqN5\
tD")
'T95k9m5zcX4'

    ```
    """
    url = video_url_or_id
    video_id = ""
    if not url.startswith('https://'):
        video_id = url
    else:
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query)
        x = query.get('v') 
        video_id = "" if x is None or not isinstance(x, list) \
            or len(x) == 0 else x[0]
    return video_id

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

class AbstractAstRenderer:
    """Renderer abstract class providing a framework for concrete renderers classes.
    This renderer class is a basic building block for creating new renderer types,
    including html and LaTeX/PDF renderers.     

    New renderer types can be implemented by overriding abstract methods of this class,
    which raise NonImplementedError exceptions.
    """

    def __init__(self, document = "", base_path = "", embed_page = False):
        # Path to the notes repository
        self._base_path: pathlib.Path = pathlib.Path(base_path)
        """Root directory of current MWiki repository"""

        self._is_embedded_page: bool = embed_page
        """Flag which indicates whether the current page is embedded within another wiki page."""

        self._embedded_page: str = ""
        """Current embedded wiki page within the current one.
        An embedded wiki page is created by using the syntax 

        ```md
        ![[Name of embedded wiki page file]]
        ```
        
        which embeds the wiki page 'Name of embedded wiki page file.md'
        within the current wiki.
        """

        self._count_h1: int = 0
        """Current count of h1 headline - '## h1 headline level'"""

        self._count_h2: int = 0
        """Current count of h2 headline - '### h2 headline level'"""

        self._title: int = ""
        """Optional Page Title that may be defined in the document YAML front-matter"""

        self._count_h3: int = 0
        self._count_h4: int = 0

        self._figure_counter: int = 1
        """Counter of figures (images with metadata). """

        self._video_counter: int = 1
        """Counter of videos (videos with metadata)"""

        self._footnotes_counter: int = 1

        self._footnotes: List[str] = []

        self._dependecies: List[pathlib.Path] = []
        """List of embedded markdown pages (md -markdown files) in this page"""

        self._internal_links: List[str] = []

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
            , "mastodon_handle_inline":     self.render_mastodon_handle_link
            , "wiki_text_highlight_inline": self.render_wiki_text_highlight_inline
            , "wiki_embed":                 self.render_wiki_embed 
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
            , "wiki_tag_inline":            self.render_wiki_tag_inline
        }

    @property
    def title(self):
        return self._title

    @property
    def dependencies(self) -> List[pathlib.Path]:
        """Return list of MWiki pages embedded in the current page."""
        return self._dependecies
    
    @property
    def internal_links(self) -> List[str]:
        """Return list of internal links"""
        return self._internal_links

    def find_page(self, name: str) -> Optional[pathlib.Path]:
        """Find path to note file, given its name."""
        mdfile_ = name + ".md"
        match = next(self._base_path.rglob(mdfile_), None)
        return match 

    def page_exists(self, name: str) -> bool:
        path = self.find_page(name)
        out = path is not None
        return out

    def render_note(self, name: str) -> Optional[str]:
        """Render a embedded wiki page (note file of *.md extension) given its name."""
        p = self.find_page(name)
        if not p: return "" 
        if not p.is_file(): return ""
        self._dependecies.append(p)
        source = p.read_text()
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)       
        self._is_embedded_page = True 
        self._embedded_page = name
        html = self.render(ast)
        self._is_embedded_page = False
        self._embedded_page = ""
        return html

    def render(self, node: SyntaxTreeNode) -> str:
        """Render MWiki AST - SyntaxTreeNode to the target format.
        Compiles a MWiki AST (Abstract Syntax Tree) node, which is the same 
        as SyntaxTreeNode to the target format of the concrete renderer class.
        For instance, the target format can be html, UNIX texinfo, LaTex, or other 
        simpler markdown format. 

        """
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

    def render_root(self, node: SyntaxTreeNode) -> str:
        """Render document root node."""
        raise NotImplementedError()

    def render_text(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_strong(self, node: SyntaxTreeNode) -> str:
        """Render bold text, equivalent to html '<strong>text</strong>'"""
        raise NotImplementedError() 

    def render_em_italic(self, node: SyntaxTreeNode) -> str:
        """Render emphasis text, aka italic text, equivalent to html <em>Italic text.</em>"""
        raise NotImplementedError() 

    def render_strikethrough(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_softbreak(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_hardbreak(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_frontmatter(self, node: SyntaxTreeNode) -> str:
        """Render frontamtter node, which contains YAML metadata and is not visible."""
        raise NotImplementedError() 

    def render_footnote_block(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_code_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 
    
    def render_math_inline(self, node: SyntaxTreeNode) -> str:
        """Render Markdown inlince code, akin to html <code>import sys</code>.
        Example: This method could render `import sys` to '<code>import sys</code>' (html5).
        """
        raise NotImplementedError()
    
    def render_math_single(self, node: SyntaxTreeNode) -> str:
        """Render inline LateX math code, such as '$f(x) = \sin \\theta$' """
        raise NotImplementedError()
    
    def render_math_block(self, node: SyntaxTreeNode) -> str: 
        """Render display mode LaTeX math blocks.
        For instance, it renders LateX formulas such as

        ```
        $$
          \mathbf{v} = \\frac{d \mathbf{r}}{dt}
        $$
        ```
        
        """
        raise NotImplementedError()
    
    def render_horizontal_line_hr(self, node: SyntaxTreeNode) -> str:
        """Render horizontal line (---) equivalent to <hr> html5 element."""
        raise NotImplementedError()

    def render_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_paragraph(self, node: SyntaxTreeNode) -> str:
        """Render paragraph elements, akin to html5 <p> element, such as <p>paragraph</p>."""
        raise NotImplementedError()

    def render_heading(self, node: SyntaxTreeNode) -> str:
        """Render document headings, akin to <h1>, <h2>, ..., <h5>
        For instance a html renderer implementation of this abstract class can
        render MWiki syntax '## Heading Level 2' to <h2>Heading Level 2</h2>.
        """
        raise NotImplementedError()

    def render_blockquote(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_container(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()
    
    def render_link(self, node: SyntaxTreeNode) -> str:
        """Render external hyperlink, akin to html5 element <a src="http://some_url.com">Label</a> 

        Syntax of MWiki rendered element:
            [label of hyperlink](http://url-of-the-hyperlink.com)
        """
        raise NotImplementedError()

    def render_wikilink_inline(self, node: SyntaxTreeNode) -> str:
        """Render internal hyperlinks for pages or files hosted in the wiki server.

        For instance, the hyperlink to the page 'Linux Debian Distribution', 
        which corresponds to the file 'Linux Debian Distribution.md' can be defined as

        + [[Linux Debian Distribution]]

        """
        raise NotImplementedError()

    def render_mastodon_handle_link(self, node: SyntaxTreeNode) -> str:
        """Render hyperlinks to Mastodon handles of the format @<USERNAME>@<SERVER>

        For instance, a matodon handler `@kde@floss.social`, which is the Mastodon handle 
        (username) of the KDE project in the server https://floss.social 
        could be rendered by a html implementation of the Renderer class as

        + `<a src="http://floss.social/@kde">@kde@floss.social</a>`

        This is just a shortcut for creating hyperkinks to Mastodon handles.
        """
        raise NotImplementedError()
    
    def render_wiki_text_highlight_inline(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_image(self, node: SyntaxTreeNode):
        """Render external images.
        
        This abstract method renders the syntax 
        
        ```markdown
        Embed image image1.png in the current page.

        ![](https://www.some-site.com/assets/image1.png)
        
        Embed image image2.jpg in the current page.

        ![](/relative/url/to/image.jpg)
        ```
        
        for embeddding external images in the current wiki page.
        Note that the syntax for embedding internal image is ![[name-of-image.jpeg]] and it is 
        handled the the abstract method `render_wiki_embed`.
        """
        raise NotImplementedError()

    def render_wiki_embed(self, node: SyntaxTreeNode) -> str:
        """Render internal resources embedded in a wiki page, including images and other multimedia files."""
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
        """Render bullet lists, akin to html5 <ul> element."""
        raise NotImplementedError()

    def render_ordered_list(self, node: SyntaxTreeNode) -> str:
        """Render ordered lists, akin to html5 <ol> element."""
        raise NotImplementedError()

    def render_list_item(self, node: SyntaxTreeNode) -> str:
        """Render items of bullet lists or ordered, akin to html5 <li> element."""
        raise NotImplementedError()

    def render_myst_role(self, node: SyntaxTreeNode) -> str:
        """Render MySt role syntax.

        MyST roles are syntax MyST markdown constructs with the format

        ```
        {role-name}`inline text with metadata.`
        ```

        This function renders the following MyST role syntax:

        Abbreviation:

        ```
        {abbr}`abbreviation (explanation here)`
        ```

        Underline Text
        ```
        {u}`Underline Text here`
        ```

        Inline LaTeX math text (Rendered by MathJax)
        ```
        {math}`f(x) = x^2 - 10x + 2`
        ```

        Youtube embedded video

        ```
        {youtube}`https://video-url`
        {youtube}`VIDEO-ID-HERE`
        ```

        """
        raise NotImplementedError() 

    def render_dl (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_dt (self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 
        
    def render_dd(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError() 

    def render_table(self, node: SyntaxTreeNode) -> str:
        """Render markdown tables, akink to html5 <table>."""
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
        """Render raw html block"""
        raise NotImplementedError()

    def render_html_inline(self, node: SyntaxTreeNode) -> str:
        """Render raw inline html block."""
        raise NotImplementedError()

    def render_myst_line_comment(self, node: SyntaxTreeNode) -> str:
        """Render Wiki comments, which starts with % syntax. This element is not rendered."""
        raise NotImplementedError()

    def render_footnote_block(self, ndoe: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        raise NotImplementedError()

    def render_wiki_tag_inline(self, node: SyntaxTreeNode) -> str:
        """Render hashtags, akin to Mastodon or Twitter hashtags, which are shortcuts for searching.

        For instance, a hashtag #foss is rendered to a html5 hyperlink. 
        When users clicks at this hyperlink, MWiki searches for all pages containing the '#foss' text, 
        which standas for 'free and open source software'.
        """
        raise NotImplementedError()

class HtmlRenderer(AbstractAstRenderer):
    """MWiki renderer which compiles MWiki markup language to html.
    This class compiles .md wiki page files to html.
    """

    def __init__(self, page_name = ""
                     , render_math_svg = False
                     , embed_math_svg = False
                     , base_path: str = ""
                     , preview: bool = False):
        super().__init__(base_path = base_path)
        self._pagefile = page_name
        self._page_path: Optional[pathlib.Path] = self.find_page(page_name.split(".")[0])
        self._timestemap = int(100000 * self._page_path.lstat().st_mtime) \
                                if self._page_path is not None else 0
        ## assert self._page_path is not None
        self._render_math_svg =  render_math_svg  
        self._section_enumeration = False
        self._embed_math_svg = False
        self._myst_line_comment_enabled = True
        self._equation_enumeration = "section"
        self._theorem_counter = 1
        """Current theorem number"""

        self._needs_mathjax = False
        """Flag used for only including MathJax in the html template
        if it is necessary to render equation. MathaJax is only
        loaded in the template base.html if this flag is True.
        """

        self._footnotes_html_rendering = ""

        self._preview = preview
        
        self._abbreviations = {}
        """Dictionary/hash map/hash database of of abbreviations defined in the wiki page frontmatter.."""
        
        self._wordlinks = {}
        """ 
        Dictionary where the keys are the words and the values
        are the corresponding heyperlinks. 

        This database is defined in the frontmatter of the current document. 
        """

        self._unicode_database = [
              ("(TM)", "™") # Trademark 
            , ("{TM}", "™")  # Trademark 
            ##, ("(C)",  "©") # Copyright 
            , ("{C}",  "©") # Copyright 
            ##, ("(R)",  "®") # Registered
            , ("{R}",  "®") # Registered
            , ("{deg}", "°")     # Degrees (angle)
            , ("{degrees}", "°") # Degrees (angle)
            , ("{euros}", "€")  # Euro 
            , ("{pounds}", "£") # Great Britain Pound (aka pounds)
            , ("{gbp}",    "£")  # Great Britain Pound (aka pounds)
            , ("{yen}", "¥")     # Yen (Currency)
            , ("{yens}", "¥")     # Yen (Currency)
            , ("{paragraph}", "¶")
            , ("{pilcrow}", "¶")
            , ("{section}", "§")

        ]


    @property
    def needs_mathjax(self) -> bool:
        """Returns true if mathjax needs to be included in the template base.html
        The purpose of this flag is allowing lazy load of MathJax for
        increasing the page loading speed.
        """
        return self._needs_mathjax

    @property
    def equation_enumeration(self):
        return self._equation_enumeration

    def _add_abbreviations(self, text: str) -> str:
        """Replace abbreviation words in a text by <abbr> html5 elements."""
        html = text 
        for (abbreviation, description) in self._abbreviations.items():
            rep =  f"""<abbr title="{description}">{abbreviation}</abbr>""" 
            ## html = html.replace(abbreviation, rep) 
            html = re.sub(r"\b%s\b" % abbreviation.replace(".", r"\."), rep, html)
        return html 
        
    def _add_wordlinks(self, text: str) -> str:
        """Replace workds defined in self._wordlinks by their corresponding hyperlinks."""
        html = text 
        for (word, url) in self._wordlinks.items():
            rep =  f"""<a target="_blank" class="link-external" rel="noreferrer noopener nofollow" href="{url}">{word}</a>""" 
            html = re.sub(r"\b%s\b" % word.replace(".", r"\."), rep, html)
        return html 

    def enable_render_math_mathjax(self, value):
        self._render_math_svg = not value

    def enable_render_math_svg(self, value):
        self._render_math_svg = value 

    def render_root(self, node: SyntaxTreeNode) -> str:
        html = ""
        ### html = "\n\n".join([ self.render(n) for n in node.children ])
        for n in node.children:
            node_html = self.render(n)
            if node_html == _STOP_SENTINEL:
                break
            html += node_html + "\n\n" 
        ## Render footnotes foward references
        counter = 0
        for note in self._footnotes:
            n = counter + 1
            forward_reference = "{{{@FOOTNOTE-FORWARD-REFERENCE-%d}}}" % n
            html = html.replace(forward_reference, self._footnotes[counter])
            #block = '\n <p class="footnote-item"><a class="link-internal" href="#footnote-reference-link-%d">[%d]</a> %s</p>' % (n, n, note)
            counter += 1
        #
        # Resolve forward reference to footnotes listing
        #
        # ```{footnotes}
        # ```
        html = html.replace(FOOTNOTES_DIV_FORWARD_REFERENCE, self._footnotes_html_rendering)
        return html
    
    def render_text(self, node: SyntaxTreeNode) -> str:
        html = node.content
        for (entry, replacement) in self._unicode_database:
            html = html.replace(entry, replacement)
        html = self._add_wordlinks(html)
        html = self._add_abbreviations(html)
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
        html = ""
        if inner == "{{@stop}}":
            html =  _STOP_SENTINEL
        ## Custom Markdown syntax for <br> Html new line
        elif inner == "{nl}":
            html = "\n<br>"
        elif "div-wiki-image" in inner:
            html = inner 
        else:
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
        """Render markdown heading #, ## ... to html heading <h1>, <h2> and etc.       
        """
        ##print(f" [TRACE] redender_heading => self._pagefile = {self._pagefile}")
        # Unix timestamp of last update of source file
        ###print(f" [TRACE] Timestamp of last file update = {timestamp}")
        title  = node.children[0].content.strip()
        anchor = "H_" + title.replace(" ", "_")
        value  = utils.escape_html(title)
        link   = f"""<a class="link-heading" href="#{anchor}">¶</a>"""
        # h1 => 1, h2 => 2, ..., h6 => 6
        tag = ""
        tex_command = ""
        if self._is_embedded_page:
            ## breakpoint()
            heading_level = int(node.tag.strip("h"))
            tag = f"h{heading_level + 1}"
            ## print(" [TRACE] embed tag = ", tag, " title = ", title)
        else:
            tag = node.tag if hasattr(node, "tag") else ""
        ## Add automatic enumeration to headings 
        if tag == "h2":
            # not (a OR b) = (not a) AND (not B)
            if title.lower() != "overview" and title.lower() != "related":
                self._count_h2 += 1
                self._count_h3 = 0
                if self.equation_enumeration != "cont" and self.equation_enumeration != "continuous":
                    # Reset MathJax/LaTeX equation enumeration every subsection 
                    # if the 'equation_enumeration_style: <style>' settings in the 
                    # document frontmatter is set not set to continous or subsection
                    tex_command = r'<span class="tex-section-command" style="display:none">\(\setSection{%s}\)</span>' % self._count_h2
                    tex_command += "\n" + r'<span class="tex-section-command" style="display:none">\(\setSubSection{%s}\)</span>' % self._count_h3
                value = f"{self._count_h2} {value}" if self._section_enumeration else value
        elif tag == "h3":
            self._count_h3 += 1
            self._count_h4 = 0
            if self.equation_enumeration != "cont" and self.equation_enumeration != "continuous":
                tex_command += "\n" + r'<span class="tex-section-command" style="display:none" data-code="\setSubSection{%s}">\(\setSubSection{%s}\)</span>' % (self._count_h3, self._count_h3)
            value  =  f"{self._count_h2}.{self._count_h3} {value}" \
                            if self._section_enumeration else value
        elif tag == "h4":
            self._count_h4 += 1
            value =  f"{self._count_h2}.{self._count_h3}.{self._count_h4} {value}" \
                        if self._section_enumeration else value
        ## Edit link for editing only part
        # of the document 
        next_sibling = None 
        line_start = node.map[0]
        ##breakpoint()
        for x in node.siblings:
            if x.tag == node.tag \
                and id(x) != id(node) and x.map[1] >= line_start:
                next_sibling = x 
                break
        assert id(next_sibling) != id(node)
        line_end   = next_sibling.map[1] - 1 if next_sibling else "end"
        ## assert line_start <= line_end
        ## breakpoint()
        if tag == "h2" or tag == "h3":
            pagename = self._pagefile.split(".")[0] if not self._is_embedded_page else self._embedded_page
            page_link = pagename.replace(" ", "_")
            url =  f"/edit/{page_link}?start={line_start}&end={line_end}&anchor={anchor}&page={pagename}&timestamp={self._timestemap}"
            edit_link = f"""<a data-i18n="edit-section-button" class="link-edit" style="display:none" href="{url}" title="[i18n]: {value}" class="edit-button"><img class="img-icon" src="/static/pencil.svg"></a>"""
            ## breakpoint()
            html   = (f"""<div class="div-heading">""" 
                      f""" \n<{tag} id="{anchor}" class="document-heading anchor">{value} {link}</{tag}>"""
                      f""" \n{edit_link}{tex_command}"""  
                       "\n</div>" 
                      )
            if tag == "h2":
               html = html + """\n<hr class="line-under-heading">""" 
        else:
            html = f"""<{tag} class="document-heading">{title}</{tag}>""" 
        # Add horizontal line below heading if it is h2.
        return html  
 
    def render_html_inline(self, node: SyntaxTreeNode) -> str:
        html = node.content
        return html 
    
    def render_html_block(self, node: SyntaxTreeNode) -> str:
        html = node.content       
        return html 

    def _render_blockquote(self, node: SyntaxTreeNode) -> str:
        inner = "\n".join([ self.render(n) for n in node.children ])
        # Remove Obsidian tag [!qupte]
        inner = inner.replace("[!quote]", "")
        html  = f"""<blockquote>\n{inner}\n</blockquote>"""
        return html 

    def render_blockquote(self, node: SyntaxTreeNode) -> str:
        html = ""
        if len(node.children) == 0:
            html =  self._render_blockquote(node)
            return html 
        tag = node.children[0].children[0].children[0].content.strip() 
        if tag.startswith("[!note]") or tag.startswith("![example]+") or tag == "[!info]" or tag == "[!tip]" or tag == "[!def]" or tag == "![proof]":
            admonition_title = "".join([ self.render(x) 
                                        for x in node.children[0].children[0].children[1:]])
            rest = node.children[1:]
            ## breakpoint()
            content = "\n".join([ self.render(x) for x in rest])
            html = f"""<div class="note admonition anchor">
                         <span class="admonition-title">{admonition_title}</span>
                         <div>
                         {content}
                         </div>
                    </div> """
            return html
        html =  self._render_blockquote(node)
        return html 

    def render_math_block(self, node: SyntaxTreeNode) -> str:
        html = ""
        content = node.content.replace("\n>", "")
        if self._render_math_svg:
            html = _latex_to_html(content, inline = False)
        else:
            self._needs_mathjax = True
            html = """<div class="math-block anchor"> \n$$\n""" \
                 + utils.escape_html(content) + "\n$$\n</div>"
        return html 

    def render_math_inline(self, node: SyntaxTreeNode) -> str:
        # NOTE: It is processed by MathJax
        #html = f"""<span class="math-inline">${node.content}$</span>"""
        html = ""
        if self._render_math_svg:
            html = _latex_to_html(node.content, inline = True)
        else:
            self._needs_mathjax = True
            html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        return html

    def render_math_single(self, node: SyntaxTreeNode) -> str:
        # NOTE: It is processed by MathJax
        #html = f"""<span class="math-inline">${node.content}$</span>"""
        html = ""
        if self._render_math_svg:
            html = _latex_to_html(node.content, inline = True)
        else:
            self._needs_mathjax = True
            html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        ## html = f"""<span class="math-inline">\\({node.content}\\)</span>"""
        return html 

    def render_wiki_embed(self, node: SyntaxTreeNode) -> str:
        assert node.type == "wiki_embed"
        src = node.content
        html = ""
        if "." not in src:
            note_name = src 
            href = utils.escape_url(f"/wiki/{note_name}")
            caption = f"The page '{note_name}' does not exist yet. Click on it to create the page." 
            html_ = f"""<hr>Embedded note: <a class="link-internal-missing" href="{href}" title="{caption}">{note_name}</a>  """
            html = html_ + self.render_note(note_name) or ""
            ## print(" [TRACE] html = ", html)
        elif src.endswith(".mp4"):
            if self._preview:
                html = """
                <div class="divi-wiki-image">
                    <video controls width="80%">
                        <source src="/wiki/%s" type="video/mp4">
                        Download the <a href="/wiki/%s}">MP4 Video</a>
                    </video>
                </div>
                """ % (src, src)
            else:
                html = """ 
                        <div class="div-wiki-image lazy-load-video"  
                             data-src="/wiki/{0}" data-type="video/mp4">
                        </div>
                       """.format(src, src)
        elif src.endswith(".webm"):
            if self._preview:
                html = """
                <div class="divi-wiki-image">
                    <video controls width="80%">
                        <source src="/wiki/%s" type="video/webm">
                        Download the <a href="/wiki/%s}">WEBM4 Video</a>
                    </video>
                </div>
                """ % (src, src)
            else:
                html = """ 
                    <div class="div-wiki-image lazy-load-video" 
                         data-src="/wiki/{0}" data-type="video/webm" >
                    </div>
                   """.format(src, src)
        else:
            if self._preview:
                html = """<div class="div-wiki-image"><img class="wiki-image anchor" src="/wiki/%s" alt=""></div>""" % src
            else:
                html = """<div class="div-wiki-image"><img class="wiki-image lazy-load anchor" data-src="/wiki/%s" alt=""></div>""" % src
        return html

    def render_link(self, node: SyntaxTreeNode) -> str:
        """Render markdown hyperlink.

        Render the following syntax for markdown hyperlink:

        [<LABEL>](<UR>)
    
        => Hyperlink to US patent US7139686
          `<patent:7,139,686>`
        
        => Hyperlink to DOI (Document Object Indentifier)
           `<doi:$DOI-IDENTIFIER>` 

        => Hyperlink to IEFT RFC standard 
           `<rfc:$RFC-NUMBER>`, example `<rfc:7221e`
        
        => Hyperlink to Common Vulnerability Exposures (CVE):
           `<cve:$CVE-NUMBER-HERE>`

        """
        ## breakpoint()
        label = "".join([ self.render(n) for n in node.children ])
        href =  node.attrs.get("href") or ""
        attrs = "" 
        ## breakpoint()
        if href.startswith("#"):
            attrs = """ class="link-internal" """
        else:
            ## breakpoint()
            title = ""
            fullLinkFlag = href.startswith("r-")
            # Trim prefix 'r-'
            href =  href[2:] if fullLinkFlag else href 
            ## DOI - Digital Object Identifier
            if href.startswith("doi:") or href.startswith("DOI:"):
                temp = utils.escape_url(href.strip("doi:").strip("DOI:"))
                title = "Digital Object Identifier"
                href = f"https://doi.org/{temp}"
            # arXiv Bibliographic Identifier for resarch paper pre-print 
            elif href.startswith("arxiv:") or href.startswith("arXiv:"):
                temp = utils.escape_url(href.strip("arxiv:").strip("arXiv:"))
                title = "arXiv preprint identifier"
                href = f"https://arxiv.org/abs/{temp}"
            # CiteSeerX Bibliographic Identifier 
            elif href.startswith("CiteSeerX:"):
                temp = utils.escape_url(href.strip("CiteSeerX:"))
                title = "CiteSeerX identifier - citerseerx.ist.psu.edu"
                href = f"https://citeseerx.ist.psu.edu/viewdoc/summary?doi={temp}"
            # Semantic Scholar Bibliographic Identifier 
            elif href.startswith("S2CID:"):
                title = "Semantic Scholar Bibliographic Identifier"
                temp = utils.escape_url(href.strip("S2CID:"))               
                href = f" https://api.semanticscholar.org/CorpusID:{temp}"
            elif href.startswith("issn") or href.startswith("ISSN"):
                title = "International Standard Serial Number identifier"
                temp = utils.escape_url(href.strip("issn:").strip("ISSN"))               
                href = f"https://search.worldcat.org/search?q=issn+{temp}"
            # Bibcode identifier for astronomical data Bibcode:2020ISysJ..14.1921B
            elif href.startswith("Bibcode:"):
                title = "Bbibcode identifier for astronomical data"
                temp = utils.escape_url(href.strip("Bibcode:"))
                href = f"https://ui.adsabs.harvard.edu/abs/{temp}"
            # Request For Comment => IETF (Internet Engineering Task Force) Technical Standard
            elif href.startswith("rfc:") or href.startswith("RFC"):
                title = "Request For Comment - IETF (Internet Engineering Task Force) Technical Standard"
                temp = utils.escape_url(href.strip("rfc:").strip("RFC"))
                href = f"https://datatracker.ietf.org/doc/html/rfc{temp}"
                label = f"RFC {temp}"
            # WorldCat Identifier OCLC Number 
            elif href.startswith("oclc:") or href.startswith("OCLC:"):
                title = "WorldCat Identifier OCLC Number "
                temp = utils.escape_url(href.strip("oclc:").strip("OCLC:"))
                href = f"https://search.worldcat.org/oclc/{temp}"
                label = f"{temp}"
            # PMID - PubMedID 
            elif href.startswith("pmid:") or href.startswith("PMID:"):
                title = "PubMed Identifier"
                temp = utils.escape_url(href.strip("pmid:").strip("PMID:"))
                href = f"https://pubmed.ncbi.nlm.nih.gov/{temp}"
                label = f"PMID {temp}"
            elif href.startswith("patent:") or href.startswith("PATENT:"):
                title = "Patent number"
                temp = href.strip("patent:").strip("PATENT:").replace(",", "")
                temp = ("US" + temp) if temp[0].isdigit else temp
                href = f"https://patents.google.com/patent/{temp}"
                label = f"Patent {temp}"
            ## PEP - Python Enhancement Proposal 
            ## Alows create links to PEPs using <pep:333>, creates 
            ## lik to https://peps.python.org/pep-333 - Pythons' PEP 333
            elif href.startswith("pep:") or href.startswith("PEP:"):
                title = "PEP - Python Enhancement Proposal"
                temp = utils.escape_url(href.strip("pep:").strip("PEP:"))
                label = f"PEP {temp}"
                href = f"https://peps.python.org/pep-{temp}"
            ## Hyperlink to Python package 
            elif href.startswith("pypi:") or href.startswith("PYPI:"):
                title = "Python Package - pypi.org"
                temp = utils.escape_url(href.strip("pypi:").strip("PYPI:"))
                label = temp 
                href = f"https://pypi.org/project/{temp}"
            # Hyperlink to CVE (Common Exposure Vulnerability) bug database 
            elif href.startswith("cve:") or href.startswith("CVE:"):
                title = "CVE - Common Vulnerability Exposures"
                temp = href[4:]
                label = temp 
                href = f"https://www.cve.org/CVERecord?id={temp}"
            # Hyperlink to subreddit 
            elif href.startswith("rd:") or href.startswith("reddit:"):
                ## breakpoint()
                temp = utils.strip_prefix("reddit:", href)
                temp = utils.strip_prefix("rd:", temp)
                label = temp 
                title = f"Subreddit {temp}"
                href = f"https://old.reddit.com" + temp
            label = href if fullLinkFlag else label
        title = node.attrs.get("title", title)
        title = f'title="{title}"' if title != "" else ""
        attrs = f""" target="_blank" {title} class="link-external" rel="noreferrer noopener nofollow" """
        html = f"""<a href="{href}" {attrs}>{label}</a>"""
        return html

    def render_wikilink_inline(self, node: SyntaxTreeNode) -> str:
        href = ""
        label = ""
        ## breakpoint()
        x = node.content.split("|")
        if len(x) == 1:
            href = x[0].strip()
            label = x[0].strip()
        elif len(x) == 2:
            href = x[0].strip()
            label = x[1].strip()
        ## if "." not in node.content:
        ##     href = node.content
        ##     label = href
        html = ""
        href_ = utils.escape_url(f"/wiki/{ href.replace(' ', '_') }")
        if "." not in href:
            self._internal_links.append(href)
            match =  self.find_page(href)
            class_name = "link-internal" if match else "link-internal-missing"
            description = ""
            if match:
                data = mparser.get_pagefile_metadata(match) or {}
                description = data.get("description", "")
            # In this case, href refers to a Wiki page (has no extension)
            html = f"""<a href="{href_}" class="{class_name} wiki-link" title="{description}">{label}</a>"""
        else:
            # In this case, href refers to some file, that is opened in a new tab 
            html = f"""<a href="{href_}" target="_blank" class="link-internal wiki-link">{label}</a>"""
        return html 


    def render_mastodon_handle_link(self, node: SyntaxTreeNode) -> str:
        ## breakpoint() 
        username =  node.content
        server = node.info
        title = f'title="Mastdon account from server {server}"' 
        attrs = f""" target="_blank" {title} class="link-external" rel="noreferrer noopener nofollow" """
        html = f"""<a href="https://{server}/@{username}" {attrs}>@{username}@{server}</a>"""
        return html 

    def render_myst_role(self, node: SyntaxTreeNode) -> str:
        role = node.meta.get("name", "")
        content = utils.escape_html(node.content)
        html = ""
        # MyST Underline role
        if role == "u":
            html = f"""<u>{content}</u>"""
        ## MyST math role. Exmaple: {math}`f(x) = \sqrt{x^2 - 10x}`
        elif role == "math":
            html = f"""<span class="math-inline">\\({content}\\)</span>"""
        # MyST sub role for superscript H{sub}`2`O compiles to H<sub>2</sub>O
        elif role == "sub":
            html = f"""<sub>{content}</sub>"""
        # MyST sub role for superscript 4{sup}`th` compiles to 4<sup>th</sup>O
        elif role == "sup":
            html = f"""<sup>{content}</sup>"""
        # MyST role for creating abbreviation, rendered to html5 <abbr>
        # {abbr}`HR (Human Resources)`
        elif role == "abbr":
            match = re.match(r"(\S+?)\s+\((.+)\)", content)
            if not match:
                return content
            abbreviation = match.group(1)
            description  = match.group(2)
            html = '<abbr title="%s">%s</abbr>' % (description, abbreviation)
            # TODO Finish later
        # MyST role for adding note/observation or explanation to some word, set words or sentence.
        # Syntax: {note}`[TERM] ([NOTE])`
        #  The python dictionary is {note}`hash table (This data structure is unordered.)`.
        elif role == "note":
            match = re.match(r"(.*)\((.*)\)", content)
            if not match:
                return content
            term = match.group(1).strip()
            note  = match.group(2).strip()
            html = '<span class="myst-note-role" data-note="%s">%s</span>' % (note, term)
        elif role == "big":
            html = f'<span class="text-big">{content}</span>'
        elif role == "big-bold":
            html = f'<span class="text-big-bold">{content}</span>'
        elif role.startswith("color") or role in ["blue", "red", "orange", "gray", "green"]:
            color = role[len("color:"):] if role.startswith("color:") else role
            html = f"""<span class="myst-color-role" style="color:{color};">{content}</span>"""
        elif role == "youtube" or role == "yt":
            video_id = get_yoututbe_video_id(content)
            html = """ <iframe class="youtube-player" 
                        src="https://www.youtube-nocookie.com/embed/%s?enablejsapi=1" > 
                      </iframe> 
                   """ %  video_id
        else:
            html = "{%s}`%s`" % (role, content)
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
        """
        Render fence code blocks delimited by three backticks (```). 

        Python Code Block:

        ```python
        import os 
        print(os.listdir("/"))
        ```

        Latex Formula (Rendered to a LaTeX, not a code block)

        ```{math}
        f(x) = \\frac{\\sqrt{x^2 + b^2 - c}}{ 2 a}
        ```

        Latex Macro code Block defines LaTeX macros used by 
        mathjax. This block is not rendered.

        ```{latex_macro}
        % Logical AND 
        \DeclareMathOperator{\\and}{ \\wedge }
        % Logical OR
        \DeclareMathOperator{\\or}{ \\vee }
        ```
        
        Quotation code block, rendered to <blockquote>

        ```{quote}
        Some quotation of somebody here.
        ```

        Solution of example or exercise:

        ```{solution}
        Consider an orthogonal matrix $Q \\in \mathbb{R}^{n \\times n}$
           ... ... 
           ... ... 
        Then, it can be shown that:
        $$
        (Q \\mathbf{u}) \\cdot (Q \\mathbf{v}) = \\mathbf{u} \\cdot \\mathbf{v}
        $$
        ```

        Proof of theorem:

        ```{proof}
        Let $Q$ be an orthogonal matrix such that $Q \\in \mathbb{R}^{n \\times n}$.
        It is possible to prove that the determinat of this matrix is always 1
        taking the determinat of $Q Q^{-1}$.

         ... ... 
         ... ...
         
        $$
        \\begin{split}
                   \\det (Q Q^{-1})     &= \\det \\mathbf{I}
             \\\\  \\det (Q Q^T)        &= 1
             \\\\  \\det (Q) \\det(Q^T) &= 1
             \\\\  \\det (Q) \\det(Q^T) &= 1 
             \\\\  \\det (Q) \\det(Q)   &= 1
             \\\\  \\det (Q) \\det(Q)   &= 1
             \\\\  \\det (Q)^2          &= 1 
             \\\\  \\det (Q)            &= 1 
        \\end{split}
        $$
        ```
        """
        assert node.tag == "code"
        ## breakpoint()
        info = (node.info if node.info != "" else "text").strip()
        if info == "{math}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = ""
            if self._render_math_svg:
                html = _latex_to_html(content, inline = False)
            else:
                self._needs_mathjax = True
                # Algorithm code block 
                if content.strip().startswith(r"\begin{algorithm}"):
                    content, directives = mparser.get_code_block_directives(node.content)
                    label = f'id="{u}"' if (u := directives.get("label")) else ""
                    #content_ = utils.escape_html(content)
                    html = f"""<pre {label} class="pseudocode" >\n{content}\n</pre>\n"""
                # MathJS/Latex Code Block 
                else:
                    html = f"""<div class="math-block anchor" {label} > \n$$\n""" \
                        + utils.escape_html(content) + "\n$$\n</div>"
        # Render multi-line comment blocks
        #
        # Example 1:
        #
        #  ```{comment}
        #  The content here is not rendered because it is just
        #  a comment or some markdown that is still not ready
        #  to be published yet.
        #  ```
        #
        # Exaple 2:
        #
        # ```{comment} on
        # The content here will be rendered due to the on
        # command in this code block.
        # ```
        #
        elif info.startswith("{comment}"):
            command = utils.strip_prefix("{comment}", info).strip()
            if command == "on":
                ast =  mparser.parse_source(node.content)
                html = self.render(ast)
            elif command == "off":
                html = ""
            else:
                html = ""
        ## Graphviz dot language
        elif info == "{dot}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = f"""<pre {label} class="graphviz-dot" >\n{content}\n</pre>\n"""                   
        ## Mermaid JS Diagram (Flowchart, Sequence Diagram and so on.)
        elif info == "{mermaid}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            #content_ = utils.escape_html(content)
            html = f"""<pre {label} class="mermaid" >\n{content}\n</pre>\n"""                   
        # Compatible with Obsidian's pseudo-code plugin
        elif info == "pseudo" or info == "{pseudo}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            #content_ = utils.escape_html(content)
            html = f"""<pre {label} class="pseudocode" >\n{content}\n</pre>\n"""
        elif info == "{quote}":
            content, directives = mparser.get_code_block_directives(node.content)
            label = f'id="{u}"' if (u := directives.get("label")) else ""
            html = f"""<blockquote {label} >\n{utils.escape_html(content)}\n</blockquote>"""
        elif info.startswith("{solution}") or info == "{proof}" or info.startswith("{foldable}") or info.startswith("{example}"):
            ## breakpoint()
            content, directives = mparser.get_code_block_directives(node.content)
            label      = f'id="{u}"' if (u := directives.get("label")) else ""
            background = f'background:{u};' if (u := directives.get("background")) else ""
            ## breakpoint()
            ast =  mparser.parse_source(content)
            title = ""
            tag = ""
            if (m :=  re.match(r"\{(.+?)\}\s(.+)", info)) is not None:
                tag, title = m.groups()
            else:
                tag = info.strip("{}")
                title = ""
            if info.startswith("{foldable}"):
                # Remove prefix
                title = "Foldable" if (x := info[len("{foldable}"):].strip().capitalize()) == "" \
                          else x
            tag = tag.capitalize()
            i18nTagsDB = {  "solution": "foldable-math-solution-block-label"
                          , "proof":    "foldable-math-proof-block-label"
                          , "example":  "foldable-math-example-block-label"
                         }
            i18nTag = i18nTagsDB.get(tag.lower())
            inner_html = self.render(ast)
            html = f"""<div class="foldabel-block-div"><details {label}>\n<summary><u class="solution-label"><label data-i18n="{i18nTag}">{tag}</label> {title}</u></summary>\n\n<div class="foldable-block" style="{background}">{inner_html}</div>\n</details></div>"""
        elif info == "{latex_macro}":
            html = f""" 
            <div class="hidden-mathjax-macros user-macros" style="display: none;">
              <div>
              $$
                {node.content}                
              $$
              </div>
              <pre>
              {node.content}
              </pre>
            </div>
            """
        # Render figure (pictures/images) with metadata including
        # height, width, alt text,
        elif info.startswith("{figure}"):
            image = utils.strip_prefix("{figure}", info).strip()
            if image.startswith("![[") and image.endswith("]]"):
                image =  "/wiki/" + image.strip("![]")
            content, directives = mparser.get_code_block_directives(node.content)
            # Image caption 
            caption = content.strip()
            caption_ast =  mparser.parse_source(caption)
            captiona_ast_inline = None
            if len(caption_ast.children) >= 1:
                if caption_ast.children[0].type == "paragraph":
                    captiona_ast_inline = caption_ast.children[0].children[0]
                else:
                    captiona_ast_inline = caption_ast.children[0]
            caption_html = caption if captiona_ast_inline is None else self.render(captiona_ast_inline)
            # Name is a label - unique identifier for cross referencing with hyperlinks.
            name = directives.get("name", "")
            # Alternative text for acessibility (Optional)
            alt = directives.get("alt", caption)
            # Image height (Optional)
            height = f"height={u}" if (u := directives.get("height")) else ""
            # Image width (Optional)
            width = f"height={u}" if (u := directives.get("width")) else ""
            ## Rendering of this node
            if not self._preview:
                html = ("""<div class="div-wiki-image" div-figure>""" 
                        """<img id="figure-%s" class="wiki-image lazy-load anchor" data-src="%s" alt="%s" %s %s>""" 
                        """<p class="figure-caption"><label data-i18n="figure-prefix-label">Figure</label> %d: %s</p>"""
                        """</div>""") %  (name, image, alt, height, width, self._figure_counter, caption_html)
            else:
                html = ("""<div class="div-wiki-image" div-figure>""" 
                        """<img id="figure-%s" class="wiki-image  anchor" src="%s" alt="%s" %s %s>""" 
                        """<p class="figure-caption"><label data-i18n="figure-prefix-label">Figure</label> %d: %s</p>"""
                        """</div>""") %  (name, image, alt, height, width, self._figure_counter, caption_html)
            self._figure_counter += 1
        elif info.startswith("{video}"):
            video = utils.strip_prefix("{video}", info).strip()
            x = video.split(".")
            video_extension = "" if len(x) == 0 else x[-1]
            if video.startswith("![[") and video.endswith("]]"):
                video =  "/wiki/" + video.strip("![]")
            content, directives = mparser.get_code_block_directives(node.content)
            # Image caption
            caption = content.strip()
            caption_ast =  mparser.parse_source(caption)
            captiona_ast_inline = None
            if len(caption_ast.children) >= 1:
                if caption_ast.children[0].type == "paragraph":
                    captiona_ast_inline = caption_ast.children[0].children[0]
                else:
                    captiona_ast_inline = caption_ast.children[0]
            caption_html = caption if captiona_ast_inline is None else self.render(captiona_ast_inline)
            # Name is a label - unique identifier for cross referencing with hyperlinks.
            name = directives.get("name", "")
            # Alternative text for acessibility (Optional)
            alt = directives.get("alt", caption)
            # Image height (Optional)
            height = f"height={u}" if (u := directives.get("height")) else ""
            # Image width (Optional)
            width = f"height={u}" if (u := directives.get("width")) else ""
            ## Rendering of this node
            if not self._preview:
                html =  """
                        <div class="div-wiki-image">
                            <div class="lazy-load-video" data-src="%s"  data-type="video/%s" data-alt="%s">
                            </div>
                            <p class="video-caption"><label data-i18n="video-prefix-label">Video</label> %d: %s</p>
                        </div>
                        """ % (video, video_extension, alt, self._video_counter, caption_html)
            else:
                html =  """
                <div class="divi-wiki-image">
                    <video controls width="80%">
                        <source src="%s" type="video/%s">
                        Download the <a href="%s">%s Video</a>
                    </video>
                    <p class="video-caption"><label data-i18n="video-prefix-label">Video</label> %d: %s</p>
                </div>
                        """ % (video, video_extension, video, video_extension
                               , self._video_counter, caption)
            self._video_counter += 1
        ## Render list of footnotes hyperlinks
        elif info == "{footnotes}":
            html = FOOTNOTES_DIV_FORWARD_REFERENCE
        # Disable flashcard if-else branch while the flashcard
        # feature is not ready yet.
        elif False and info == "{flashcard}":
            code = node.content 
            data = None 
            try:
                data = json.loads(node.content) 
                title = data.get("title", "")
                entries = data.get("entries", [])
                html = ""
                k = 0
                n = len(entries)
                for card in entries:
                    if len(card) < 1:
                        return "<b>Flashcard error: each entry must be an array of size 2</b>" 
                    front = card[0] # Contains the question 
                    back  = card[1] # Contains the response 
                    style = "hidden" if k != 0 else ""
                    html += ("""<div class="card-entry %s" data-index="%s">\n""" % (style , k)
                                + """<button class="btn-show-card">show</button>""" 
                                + """<label class="label-card-front">(%d/%d) %s</label>""" % (k+1, n, front) 
                                + """<p class="card-answer hidden">ANSWER: %s</p>""" % back 
                                + """</div>""")
                    k = k + 1
                html = (  """<div class="div-flashcard" onclick="onFlashcardClickHandler(event)" data-size="%s">""" % len(entries)
                        + """<div><b class="flashcard-title">%s</b></div>""" % title
                        + """<div class="div-flashcard-button-panel">""" 
                            + """<button class="btn-flashcard-view">View</button>""" 
                            + """<button class="btn-flashcard-prev">Prev</button>""" 
                            + """<button class="btn-flashcard-next">Next</button>""" 
                            + """<input type="checkbox" name="random" /><label for="random">Random</label>"""
                            + """</div>""" 
                            
                        + """<div class="flashcard-entries">\n""" +  html  + """\n</div>"""
                        + """</div>"""
                        )
            except json.decoder.JSONDecorderError as ex:
                html = "<b>Flash card error: bad json syntax</b>"
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
        html = """<div class="div-wiki-image"><img class="external-image anchor" src="%s" alt="%s"></div>""" % (src, inner)
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
        """Render html definition list <dl> tag."""
        assert node.type == "dl"
        inner = "\n".join([ self.render(n) for n in node.children ])
        html = f"""<dl class="anchor">\n{inner}\n</dl>"""
        return html 

    def render_dt(self, node: SyntaxTreeNode) -> str:
        """Render description term tag <dt> of definition list <dd>."""
        assert node.type == "dt"
        inner = "".join([ self.render(n) for n in node.children ])
        html = f"""<dt class="anchor">{inner}</dt>"""
        return html

    def render_dd(self, node: SyntaxTreeNode) -> str:
        """Render description details tag <dd> of definition list <dd>."""
        assert node.type == "dd"
        if len(node.children) == 1 and node.children[0].type == "paragraph":
            ## breakpoint()
            x =   node.children[0].children[0]
            inner = self.render(x)
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
        ## breakpoint()
        pagename = self._pagefile.split(".")[0]
        url =  f"/edit/{pagename}?start={node.map[0]}&end={node.map[1] + 1}&page={pagename}&timestamp={self._timestemap}"
        edit_link = f"""<a class="link-edit link-edit-admonition" style="display:none" href="{url}" title="Edit admonition"><img class="img-icon" src="/static/pencil.svg"></a>"""  
        metadata = {}
        if first:
            _, metadata  = mparser.get_code_block_directives(first) 
        ## print(" [TRACE] metadata = ", metadata)
        class_ = metadata.get("class") or ""
        # Background color override
        background = metadata.get("background") or ""
        is_dropdown = class_ == "dropdown"
        label = f'id="{x}"' if (x := metadata.get("label")) else ""
        ## css_class = x if (x := metadata.get("class")) else ""
        ##style = f'style="background: {x};"' if (x := metadata.get("background")) else ""
        admonition_type = utils.strip_prefix("container_", node.type).strip("{").strip("}")
        admonition_title = utils.strip_prefix("{" + admonition_type + "}", node.info).strip()
        _title = f"<strong>({admonition_title})</strong>" if admonition_title != "" else ""
        if admonition_type == "def":
            admonition_title = f'<label class="admonition-tag" data-i18n="admonition-math-defintion-label">DEFINITION</label>: {_title}'
        elif admonition_type == "theorem":
            admonition_title = f'<label class="admonition-tag" data-i18n="admonition-math-theorem-label">THEOREM</label> {self._theorem_counter}: {_title}'
            self._theorem_counter += 1
        elif admonition_type == "example":
            admonition_title = f'<strong class="admonition-tag" data-i18n="admonition-math-example-label">Example</strong>: {admonition_title}'
        elif admonition_type == "details":
            admonition_title = admonition_title.title()
        else:
            rest = "" if admonition_title == "" else ": " + admonition_title
            admonition_title = admonition_type.title() + rest 
        style = f"""style="background:{background};" """
        if admonition_type != "details":
            attrs =  f""" {label} class="{admonition_type} admonition anchor" {style}""".strip()
        else:
            attrs =  f""" {label} class="{admonition_type} anchor" """.strip()
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
        title = f"""\n<span class="admonition-title">{icon}{admonition_title}{edit_link}</span>\n""" \
                if admonition_title != "" else ""
        if admonition_type == "details":
            html = f"""<details {attrs}>\n<summary><strong>{title}</strong></summary>\n<div class="admonition" style="background:{background};" >\n{inner}\n</div>\n</details>"""
        elif admonition_type == "example":
            html = f"""<aside {attrs}  class="admonition example">\n<span class="admonition-title"><strong>{title}</strong></span>\n\n{inner}\n</aside>"""
        elif is_dropdown:
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
        counter = 0
        number_footnotes = len(node.children)
        block = '\n<div class="footnotes-div"><p>Number of footnotes: %d</p>' % number_footnotes
        for child in node.children:
            n = counter + 1
            #footnote = child.children[0]
            paragraph = child.children[0]
            assert paragraph.type == "paragraph"
            inline = paragraph[0]
            assert inline.type == "inline"
            inline_html = self.render(inline)
            self._footnotes.append(inline_html)
            block += '\n <p class="footnote-item"><a class="link-internal" href="#footnote-reference-link-%d">[%d]</a> %s</p>' % (n, n, inline_html)
            ## print(f" [DEBUG] Footnote{self._footnotes_counter} = {inline_html} ")
            counter += 1
        block += "\n</div>"
        self._footnotes_html_rendering = block
        return ""

    def render_footnote_ref(self, node: SyntaxTreeNode) -> str:
        ## breakpoint()
        html = """<a href="#" id="footnote-reference-link-%d" class="link-internal"><sup class="footnote-reference" data-counter="%d" data-footnote="{{{@FOOTNOTE-FORWARD-REFERENCE-%d}}}">[%d]</sup></a>""" \
            % (self._footnotes_counter
              , self._footnotes_counter, self._footnotes_counter
              , self._footnotes_counter
              )
        self._footnotes_counter += 1
        ## print(f" [DEBUG] footnote_ref = {html}")
        return html

    def render_frontmatter(self, node: SyntaxTreeNode) -> str:
        data = {}
        try:
            data = yaml.safe_load(node.content)
        except yaml.YAMLError as ex:
            print("[ERROR] Failed to parse frontmatter data => \nDetails:", ex)
        if data is None: 
            return "" 
        if not self._is_embedded_page:
            self._title = data.get("title", "")
            self._section_enumeration  = data.get("section_enumeration", False)
            enum_style = data.get("equation_enumeration", "section")   
            enum_style = enum_style if enum_style in ["none", "cont", "continuous", "section", "subsection"] else "section"
            self._equation_enumeration = enum_style
        abbrs =  data.get("abbreviations", {}) 
        wordlinks = data.get("wordlinks", {})
        ## Append abbreviation dictionary 
        for k, v in abbrs.items():
            self._abbreviations[k] = v
        for k, v in wordlinks.items():
            self._wordlinks[k] = v
        ### breakpoint()
        ### print(" [WARNING] Frontmatter not renderend to HTML")
        return "" 

    def render_horizontal_line_hr(self, node: SyntaxTreeNode) -> str:
        return "<hr>" 

    def render_myst_line_comment(self, node: SyntaxTreeNode) -> str:
        html = ""
        if self._myst_line_comment_enabled:
            ## html = f"<!-- {node.content} -->"
            html = ""
        else:
            html = utils.escape_html(node.content)       
        return html

    def render_wiki_tag_inline(self, node: SyntaxTreeNode) -> str:
        url = f"/pages?search={node.content}".replace("#", "%23")
        html = f"""<a href="{url}" class="link-internal">{node.content}</a> """ 
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
% \setmainfont[Ligatures=TeX]{TeX Gyre Pagella}
% \setmathfont{TeX Gyre Pagella Math}

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


RENDER_MATH_SVG = True 

def node_to_html(page_name: str, node: SyntaxTreeNode, base_path: str):
    __html_render = HtmlRenderer(page_name = page_name, render_math_svg = False, base_path = base_path)
    html = __html_render.render(node)
    return html

def pagefile_to_html(pagefile: str, base_path: str) -> Tuple[HtmlRenderer, str]:
    with open(pagefile) as fd:
        source: str = fd.read()
        ## source = re.sub(r"^$$", "\n$$", source) 
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        page_name = os.path.basename(pagefile)
        renderer = HtmlRenderer(  page_name = page_name
                            , render_math_svg = False
                            , base_path = base_path
                            )
        html = renderer.render(ast)
        return renderer, html

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
