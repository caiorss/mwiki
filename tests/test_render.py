from markdown_it.tree import SyntaxTreeNode
from parsel import Selector
import mwiki.utils as utils 
import mwiki.mparser as mparser 
from mwiki.render import HtmlRenderer


def render_markdown(markdown_code: str, renderer = "mathjax") -> str:
    ast = mparser.parse_source(markdown_code)
    rnd = HtmlRenderer(latex_renderer = renderer)
    out = rnd.render(ast)
    return out   
    
def render_markdown_ast(ast: SyntaxTreeNode, renderer = "mathjax") -> str:
    rnd = HtmlRenderer(latex_renderer = renderer)
    out = rnd.render(ast)
    return out

def test_render_external_link():
    input_ = '[Lexer hack](https://en.wikipedia.org/wiki/Lexer_hack)'
    expected_label = 'Lexer hack'
    expected_url = 'https://en.wikipedia.org/wiki/Lexer_hack'
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    link      = inline.children[0]
    html      = render_markdown_ast(link)
    sel       = Selector(text = html)
    node      = sel.css("a")
    label     = node.css("::text").get() 
    klass     = node.attrib.get("class", "")
    href      = node.attrib.get("href", "")
    assert label == expected_label and href == expected_url and klass == "link-external"

def test_render_special_link_cve():
    input_ = '<cve:CVE-2024-50264>'
    expected_label = 'CVE-2024-50264'
    expected_url   = 'https://www.cve.org/CVERecord?id=CVE-2024-50264'
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    link      = inline.children[0]
    html      = render_markdown_ast(link)
    sel       = Selector(text = html)
    node      = sel.css("a")
    label     = node.css("::text").get() 
    klass     = node.attrib.get("class", "")
    href      = node.attrib.get("href", "")
    assert label == expected_label and href == expected_url and klass == "link-external"


def test_render_special_link_patent():
    input_ = '<patent:7,020,850>'
    expected_label = 'Patent US7020850'
    expected_url   = 'https://patents.google.com/patent/US7020850'
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    link      = inline.children[0]
    html      = render_markdown_ast(link)
    sel       = Selector(text = html)
    node      = sel.css("a")
    label     = node.css("::text").get() 
    klass     = node.attrib.get("class", "")
    href      = node.attrib.get("href", "")
    assert label == expected_label and href == expected_url and klass == "link-external"

def test_render_wiki_link():
    """Test the HTML rendering of MWiki hyperlinks"""
    input_    = '[[MWiki hyperlink to internal page]]'
    expected  = 'MWiki hyperlink to internal page'
    expected_url = "/wiki/MWiki_hyperlink_to_internal_page"
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    link      = inline.children[0]
    html      = render_markdown_ast(link)
    sel       = Selector(text = html)
    node      = sel.css(".wiki-link")
    text      = node.css("::text").get() 
    href      = node.attrib.get("href", "")
    assert text == expected and href == expected_url 

def test_render_internal_link_to_file():
    input_          = '[[link-to-stored-file.pdf|(Download)]]'
    expected_label  = '(Download)'
    expected_url    = "/wiki/link-to-stored-file.pdf"
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    link      = inline.children[0]
    html      = render_markdown_ast(link)
    sel       = Selector(text = html)
    node      = sel.css(".link-internal")
    text      = node.css("::text").get() 
    href      = node.attrib.get("href", "")
    targ      = node.attrib.get("target", "")
    assert text == expected_label and href == expected_url and targ == "_blank"

def test_render_heading_h2():
    input_          = '## Feedback Control Theory'
    expected_label  = 'Feedback Control Theory'
    html      = render_markdown(input_)
    sel       = Selector(text = html)
    label     = sel.css("h2::text").get().strip()
    # CSS classes 
    classes   = sel.css("h2").attrib.get("class", "").split()
    assert label == expected_label \
            and "document-heading" in classes \
            and "anchor" in classes

def test_render_multiple_headings_h2():
    input_ = r"""
## Feedback Control

Feedback control theory ... 
    
## Forward Dynamics

Forward dynamics for robotics and mechanism simulation ... 

## Inverse Dynamics

Inverse dynamics is the dynamic analysis of forces, torques
or forces necessary to control a robot or mechanism. 

## Kinematic Analysis  

Study of motion of mechanisms and robotics systems.
   """
    html = render_markdown(input_)
    sel  = Selector(text = html)
    res  = [x.strip() for x in sel.css("h2::text").getall()]
    expected_headings = [
          "Feedback Control"
        , "Forward Dynamics"
        , "Inverse Dynamics"
        , "Kinematic Analysis"
    ]
    assert res == expected_headings
    

def test_render_math_inline_mathjax():
    input_    = r'$s = \sum_{i = 1}^n x_i^2$'
    expected  = utils.escape_html(r'\(s = \sum_{i = 1}^n x_i^2\)')
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    span      = inline.children[0]
    html      = render_markdown_ast(span)
    sel       = Selector(text = html)
    node      = sel.css(".math-inline")
    result    = node.css("::text").get() 
    assert result == expected

def test_render_math_inline_katex():
    input_    = r'$s = \sum_{i = 1}^n x_i^2$'
    expected  = utils.escape_html(r's = \sum_{i = 1}^n x_i^2')
    ast       = mparser.parse_source(input_)
    paragraph = ast.children[0]
    inline    = paragraph.children[0]
    span      = inline.children[0]
    html      = render_markdown_ast(span, renderer = "katex")
    sel       = Selector(text = html)
    node      = sel.css(".math-inline")
    result    = node.css("::text").get() 
    assert result == expected


def test_render_math_inline_mathjax_():
    input_    = r'The expected result of $s = \sum_{i = 1}^n x_i^2$ should be ...'
    expected  = r'\(' + utils.escape_html(r's = \sum_{i = 1}^n x_i^2') + r'\)'
    html      = render_markdown(input_, renderer = "mathjax")
    sel       = Selector(text = html)
    node      = sel.css(".math-inline")
    result    = node.css("::text").get() 
    assert result == expected

def test_render_math_inline_katex_():
    input_    = r'The expected result of $s = \sum_{i = 1}^n x_i^2$ should be ...'
    expected  = utils.escape_html(r"s = \sum_{i = 1}^n x_i^2") 
    html      = render_markdown(input_, renderer = "katex")
    sel       = Selector(text = html)
    node      = sel.css(".math-inline")
    result    = node.css("::text").get() 
    assert result == expected

def test_render_embed_image():
    input_ = r"""
Syntax for embedding a picture in a MWiki page.

![[pasted-image-1747264831284.jpg]] 
    """
    html      = render_markdown(input_, renderer = "katex")
    expected  = "/wiki/pasted-image-1747264831284.jpg"
    sel       = Selector(text = html)
    dom       = sel.css("img")
    classes   = dom.attrib.get("class", "").split()
    data_src  = dom.attrib.get("data-src", "")
    src       = dom.attrib.get("src", "")
    assert "wiki-image" in classes \
            and "anchor" in classes \
            and src == "" \
            and data_src == expected
