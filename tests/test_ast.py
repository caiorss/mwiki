import mwiki.mparser as mparser 

AST_ROOT      = "root"
AST_PARAGRAPH = "paragraph"
AST_INILINE   = "inline"
AST_WIKILINK  = "wikilink_inline"
AST_WIKIEMBED = "wiki_embed"
AST_WIKI_FOOTNOTE = "wiki_footnote"
AST_WIKI_TEXT_HIGHLIGHT = "wiki_text_highlight_inline"


def test_parse_wikilink_ast():
    """
    Test AST of MWiki markdown code fragment containing a single wiki link.

    Expected ast:
    >>> print(ast.pretty())
    <root>
      <paragraph>
        <inline>
          <wikilink_inline>
      
    """
    wikicode = "[[Torque Equations of Motion]]"
    ast = mparser.parse_source(wikicode)
    root = ast
    paragraph = root[0]
    inline = paragraph[0]
    wikilink = inline[0]
    assert root.type == AST_ROOT \
                and paragraph.type == AST_PARAGRAPH \
                and inline.type    == AST_INILINE \
                and wikilink.type  == AST_WIKILINK 
                
def test_parse_wikilink_ast_value():
    """
    """
    expected = "Torque Equations of Motion"
    wikicode = "[[Torque Equations of Motion]]"
    ast = mparser.parse_source(wikicode)
    root = ast
    paragraph = root[0]
    inline = paragraph[0]
    wikilink = inline[0]
    assert wikilink.content == expected 
           
def test_wiki_embed_ast():
    """ Test AST of ![[embed_file]] syntax extension.
    """
    wikicode = "![[some_image_file.jpeg]]"
    ast        = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_embed = inline[0]
    ast_types  = [ root.type, paragraph.type, inline.type, wiki_embed.type ]
    expected_ast_types = [ AST_ROOT, AST_PARAGRAPH, AST_INILINE, AST_WIKIEMBED ]
    assert ast_types == expected_ast_types

def test_wiki_embed_value():
    """Test value ![[embedded_file.jpeg]] AST.
    """
    embedded_file = "some_image_file.jpeg"
    wikicode = "![[some_image_file.jpeg]]"
    ast        = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_embed = inline[0]
    assert wiki_embed.content == embedded_file 

def test_wiki_embed_page_value():
    """Test value ![[Embedded wiki page]] AST.
    """
    embedded_page = "Embedded wiki page"
    wikicode = "![[Embedded wiki page]]"
    ast        = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_embed = inline[0]
    assert wiki_embed.content == embedded_page 

def test_wiki_highlighted_text_ast():
    """Test AST of highlighted text syntax."""
    wikicode = "==Highlighted text here=="
    ast = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_text_highlight = inline[0]
    ast_types  = [ root.type, paragraph.type, inline.type, wiki_text_highlight.type ]
    expected_ast_types = [ AST_ROOT, AST_PARAGRAPH, AST_INILINE, AST_WIKI_TEXT_HIGHLIGHT ]
    assert ast_types == expected_ast_types

def test_wiki_highlighted_ast_value():
    """Test AST value of highlighted text syntax."""
    wikicode = "==Highlighted text here=="
    ast = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_text_highlight = inline[0]
    highlighted_text = wiki_text_highlight.content
    expected_highlighted_text = "Highlighted text here"
    assert highlighted_text == expected_highlighted_text 

def test_wiki_highlighted_ast_multiple():
    """Test AST value of highlighted text syntax in a wikicode with mutliple leaf nodes."""
    wikicode = "Hello ==Highlighted text here== wold"
    ast = mparser.parse_source(wikicode)
    root       = ast
    paragraph  = root[0]
    inline     = paragraph[0]
    wiki_text_highlight = inline[1]
    highlighted_text = wiki_text_highlight.content
    expected_highlighted_text = "Highlighted text here"
    assert highlighted_text == expected_highlighted_text 


def test_wiki_footnote_ast():
    """Test AST of MWiki footnote syntax."""
    wikicode = "word^{footnote about this term}"
    ast = mparser.parse_source(wikicode)
    root         = ast
    paragraph    = root[0]
    inline       = paragraph[0]
    footnote_ast = inline[1]
    ast_types    = [ root.type, paragraph.type, inline.type, footnote_ast.type ]
    expected_ast_types = [ AST_ROOT, AST_PARAGRAPH, AST_INILINE, AST_WIKI_FOOTNOTE ]
    assert ast_types == expected_ast_types

def test_wiki_footnote_ast_obsidian():
    """Test AST of MWiki footnote syntax (Obsidian compatility)."""
    wikicode     = "word^[footnote about this term]"
    ast          = mparser.parse_source(wikicode)
    root         = ast
    paragraph    = root[0]
    inline       = paragraph[0]
    footnote_ast = inline[1]
    ast_types    = [ root.type, paragraph.type, inline.type, footnote_ast.type ]
    expected_ast_types = [ AST_ROOT, AST_PARAGRAPH, AST_INILINE, AST_WIKI_FOOTNOTE ]
    assert ast_types == expected_ast_types

def test_wiki_footnote_ast_value():
    """Test AST value of MWiki footnote syntax."""
    wikicode     = "word^{footnote about this word}"
    ast          = mparser.parse_source(wikicode)
    root         = ast
    paragraph    = root[0]
    inline       = paragraph[0]
    footnote_ast = inline[1]
    footnote     = footnote_ast.content 
    expected_footnote = "footnote about this word"
    assert footnote == expected_footnote 

def test_wiki_footnote_ast_value_obsidian():
    """Test AST value of MWiki footnote syntax (Obsidian compatiblity format)."""
    wikicode     = "word^[footnote about this word]"
    ast          = mparser.parse_source(wikicode)
    root         = ast
    paragraph    = root[0]
    inline       = paragraph[0]
    footnote_ast = inline[1]
    footnote     = footnote_ast.content 
    expected_footnote = "footnote about this word"
    assert footnote == expected_footnote 

