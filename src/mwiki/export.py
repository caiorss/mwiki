import pathlib
import shutil 
from typing import Optional, Callable, Any, Dict, Optional
import jinja2 
import mwiki  
from . import render
import mwiki.utils as utils  
from mwiki.latex import LatexFormula 
import mwiki.mparser as mparser 

__all__ = [   "export"
            , "fonts_database"
            , "fonts_database_by_name"
          ]

def export(   wikipath:              Optional[str]
            , output:                Optional[str]
            , page:                  Optional[str]
            , website_name:          str
            , root_url:              str 
            , locale:                str
            , content_language:      str
            , icon:                  Optional[str]
            , main_font:             str 
            , code_font:             str 
            , title_font:            str 
            , unicode_emoji_favicon: Optional[str]
            , list_fonts:            bool 
            , allow_language_switch: bool
            , self_contained:        bool 
            , embed_latex_renderer:  bool
            , latex_renderer:        str 
            , compile_latex:         bool 
            , verbose:               bool 
            , author:                str 
            , export_source:         bool = True
            ):
    """Export a MWiki repository or a markdown files repository to a static website."""
    bool_to_on_off = lambda x: "on" if x else "off"
    if list_fonts:
        print("%30s%30s"  % ("KEY", "FONT FAMILY"))            
        for fdata in fonts_database:
            key = fdata.get("key", "")
            family = fdata.get("family", "")
            print("%30s%30s" % (key, family))
        exit(0)
    if not latex_renderer == "mathjax" and not latex_renderer == "katex":
        print("Error: expected --latex-renderer=mathjax or --latex-renderer=katex")
        exit(1)        
    if compile_latex:
        latex_renderer = "katex"
    if not wikipath and not page:
        print("Error expected --wikipath or --page command line switches.")
        exit(1)
    def favicon() -> str:
        base_path = pathlib.Path(wikipath)
        g = base_path.glob("favicon.*")
        ico = next(g, None)
        out = ""
        if ico:
            out = str(ico.name)
        return out

    def favicon_mimetype() -> str:
        _extension_mimetypes = {
              "png":  "image/png"
            , "apng": "image/apng"
            , "svg":  "image/svg+xml"
            , "webp": "image/webp"
            , "jpg":  "image/jpeg"
            , "ico":  "imag/x-icon"
        }
        ico = favicon()
        xs = ico.split(".")
        if len(xs) != 2:
            return ""
        mimetype = _extension_mimetypes.get(xs[1], "")
        return mimetype
    out = pathlib.Path(output) if output else pathlib.Path("./out")
    out.mkdir(exist_ok = True)
    root = pathlib.Path(wikipath)
    if not root.exists():
        print(f"Error not found {root.resolve()}")
        exit(1)
    if root_url != "/" and root_url.endswith("/"):
        root_url = "/" + root_url.strip("/")
    # mwiki.models.MwikiConfig.set_path(wikipath)
    base_path = str(wikipath)
    # secret_key = mwiki.models.get_secret_key()
    # app.config["SECRET_KEY"] = secret_key
    print("Root URL\n - ", root_url)
    print("Compiling wiki repository\n - ", root.resolve())
    print("Generating static website at\n - ", out.resolve())
    print()
    root_url = "" if root_url == "/" else root_url
    pages = []
    if page:
        page_path = pathlib.Path(page)
        if not page_path.exists():
            print(f"Error file {page_path} not found.")
            exit(1)
        pages = [ page_path ]
    else:
        pages = root.rglob("*.md")
    static = out / "static"
    if not self_contained:
        static.mkdir(exist_ok = True)
        mwiki.utils.copy_resource_files_ext(mwiki, "static/*.svg", static)
        mwiki.utils.copy_resource_file(mwiki, "static/main.js", static )
        mwiki.utils.copy_resource_file(mwiki, "static/static_style.css", static )
    main_js = mwiki.utils.get_path_to_resource_file(mwiki, "static/main.js")
    style_css = mwiki.utils.get_path_to_resource_file(mwiki, "static/static_style.css")
    main_code = main_js.read_text()
    style_code = style_css.read_text()
    if embed_latex_renderer and latex_renderer == "mathjax":
        mwiki.utils.copy_resource_directory(mwiki, "static/mathjax", static / "mathjax" )
    if embed_latex_renderer and latex_renderer == "katex":
        mwiki.utils.copy_resource_directory(mwiki, "static/katex", static / "katex" )
    icon_mimetypes_database = {
          "ico":   "image/x-icon"
        , "png":   "image/png"
        , "jpg":   "image/jpeg"
        , "jpgeg": "image/jpeg"
        , "svg":   "image/svg+xml"
    }
    icon_mimetype = "image/x-icon"
    icon_path = ""
    if icon is not None:
        p = pathlib.Path(icon)
        if not p.is_file():
            print(f"Error not found icon file: {p} ")
            exit(1)
        print(" [*] Using favicon ", icon)
        shutil.copy(p, out)
        icon_path = str(p.name)
        extension = str(p.name).split(".")[0].strip(".")
        icon_mimetype = icon_mimetypes_database.get(extension) or icon_mimetype
    # template  = utils.read_resource(mwiki, "templates/static.html")
    # tpl = jinja2.Template(template)
    static_html_renderer = make_template_renderer(mwiki, "templates/static.html")
    ## source_html_renderer = make_template_renderer(mwiki, "templates/source_static.html")
    root_path = mwiki.utils.get_module_path(mwiki)
    ### print(" [TRACE] root_path => (718) = " + str(root_path))
    font_face_main_font =  render_font_data(main_font
                                            , root_url = root_url
                                            , root_path = root_path
                                            , self_contained = self_contained)
    font_face_title_font = render_font_data(title_font
                                            , root_url = root_url
                                            , root_path = root_path
                                            , self_contained = self_contained)
    font_face_code_font = render_font_data(code_font
                                           , root_url = root_url
                                           , root_path = root_path
                                           , self_contained = self_contained)
    if not self_contained:
        fonts = out / "static/fonts"
        fonts.mkdir(exist_ok = True)
        copy_font_files(main_font, fonts)
        copy_font_files(title_font, fonts)
        copy_font_files(code_font, fonts)
        base_path = pathlib.Path(wikipath)
        g = pathlib.Path(wikipath).glob("favicon.*")
        ico = next(g, None)
        if ico:
            shutil.copy(ico, out)
    main_font_family  = (get_font_data(main_font) or {}).get("family") 
    title_font_family = (get_font_data(title_font) or {}).get("family")  
    code_font_family  = (get_font_data(code_font) or {}).get("family")  
    unfold_icon_url = f"{root_url}/static/dots-vertical.svg"
    menu_icon_url   = f"{root_url}/static/hamburger-menu.svg"
    home_icon_url   = f"{root_url}/static/icon-home.svg"
    if self_contained:
        unfold_icon_url = mwiki.utils.file_to_base64_data_uri(root_path / "static/dots-vertical.svg")
        menu_icon_url   = mwiki.utils.file_to_base64_data_uri(root_path / "static/hamburger-menu.svg")
        home_icon_url   = mwiki.utils.file_to_base64_data_uri(root_path / "static/icon-home.svg")
    print()
    print("Export Settings")
    print()
    print(" [*]                              Author: ", author or "")
    print(" [*]                        Website Name: ", website_name)
    print(" [*]                            Root URL: ", "/" if root_url == "" else root_url)
    print(" [*]               Content Language Code: ", content_language)
    print(" [*]  Default User Interface (UI) Locale: ", locale)
    print(" [*]               Allow language switch: ", bool_to_on_off(allow_language_switch))
    print(" [*]             Self Contained Document: ", bool_to_on_off(self_contained))
    print(" [*]       Compile LaTeX to HTML (KaTeX): ", bool_to_on_off(compile_latex))
    print(" [*]                      LaTeX renderer: ", latex_renderer.capitalize())
    print(" [*]        Load LaTeX renderer from CDN: ", bool_to_on_off(not compile_latex and not embed_latex_renderer))
    print(" [*]                Embed LaTeX Renderer: ", bool_to_on_off(not compile_latex and embed_latex_renderer))
    print(" [*]                    Main font family: ", main_font_family)
    print(" [*]                   Title Font Family: ", title_font_family)
    print(" [*]                    Code Font Family: ", code_font_family)
    print(" [*]               Unicode/emoji favicon: ", unicode_emoji_favicon)
    print()
    print("Status:")
    print()
    for p in pages:
        basename = str(p.relative_to(root))\
                .replace("Index", "index")\
                .replace(".md", ".html")\
                .replace(" ", "_")
        outfile = out / basename
        print(f" [*] Compiling {p} to {outfile}")
        pagefile = str(p)
        if compile_latex:
            ##LatexFormula.compile_document(p, root, verbose = verbose)
            LatexFormula.compile_document_parallel(p, root, verbose = verbose)
        renderer, content = render.pagefile_to_html(  pagefile
                                                    , base_path
                                                    , static_compilation  = True
                                                    , self_contained      = self_contained
                                                    , root_url            = root_url
                                                    , render_math_svg     = compile_latex 
                                                    , embed_math_svg      = self_contained 
                                                    , latex_renderer      = latex_renderer 
                                                    ) 
                                                    
        files = renderer.files
        if not self_contained:
            for file  in files:
                f = file.relative_to(root)
                dest = out / f.parent
                dest.mkdir( exist_ok = True)
                shutil.copy(file, dest)
        title = renderer.title if renderer.title != "" else str(p.name ).split(".")[0]
        # Generate table of contents 
        page_source = p.read_text()
        headings    = mparser.get_headings(page_source)
        root_       = mparser.make_headings_hierarchy(headings)
        toc         = mparser.headings_to_html(root_)
        env_ = {
              "content": utils.highlight_code(page_source, "markdown")
            , "title":    title 
            , "pagename": title
            , "page_title_i18n_tag": "source-page-title"
            , "config_sitename":     lambda: website_name
            , "config_main_font":    lambda: main_font_family
            , "config_code_font":    lambda: code_font_family
            , "config_title_font":   lambda: title_font_family
            , "default_locale":      lambda: locale
            , "use_default_locale":  lambda: True
            , "root_url":             root_url
            , "allow_language_switch": allow_language_switch
            , "main_font":            main_font_family  
            , "title_font":           title_font_family
            , "font_face_main":       font_face_main_font
            , "font_face_code":       font_face_code_font
            , "font_face_title":      font_face_title_font
            , "favicon":              icon_path 
            , "favicon_mimetype":     icon_mimetype
            , "page_description":     renderer.description
            , "page_author":          renderer.author or author 
            , "toc":                  toc 
            , "page_type":            "src_page"
        }
        src_page_html = ""
        src_page_html_url = ""
        if export_source:
            ##src_page_html = utils.base64_encode( static_html_renderer(env_) )
            src_page_html =  static_html_renderer(env_)
            src_dest = out / "src_pages"
            src_dest.mkdir( exist_ok = True )
            src_out = src_dest / basename
            src_out.write_text(src_page_html)
            src_page_html_url = f"{root_url}/src_pages/{basename}"
        # print(" [TRACE] needs pseudocode_js ", renderer.needs_latex_algorithm)
        env = {
                 "title":                title.replace("about", "About")
               , "page":                 title
               , "page_link":            title.replace(" ", "_")
               , "root_url":             root_url
               , "pagename":             title
               , "allow_language_switch": allow_language_switch
               , "main_font":            main_font_family  
               , "title_font":           title_font_family
               , "font_face_main":       font_face_main_font
               , "font_face_code":       font_face_code_font
               , "font_face_title":      font_face_title_font
               # , "favicon":              icon_path 
               # , "favicon_mimetype":     icon_mimetype
               , "page_description":     renderer.description
               , "page_author":          renderer.author or author 
               , "toc":                  toc 
               , "content":              content               
               , "latex_renderer":       renderer.latex_renderer
               , "compile_latex":        compile_latex 
               , "mathjax_enabled":      not compile_latex & renderer.needs_mathjax
               , "graphviz_enabled":     renderer.needs_graphviz 
               , "latex_algorithm":      not compile_latex & renderer.needs_latex_algorithm
               , "equation_enumeration": renderer.equation_enumeration_style
               , "config_sitename":      lambda: website_name 
               , "config_main_font":     lambda: main_font_family
               , "config_code_font":     lambda: code_font_family
               , "config_title_font":    lambda: title_font_family
               , "default_locale":       lambda: locale
               , "use_default_locale":   lambda: True
               , "embed_latex_renderer": not compile_latex and embed_latex_renderer 
               , "self_contained":       self_contained
               , "main_script_code":     main_code
               , "style_sheet_code":     style_code
               , "menu_icon_url":        menu_icon_url 
               , "unfold_icon_url":      unfold_icon_url 
               , "home_icon_url":        home_icon_url
               ##, "src_page_html":        src_page_html             
               , "export_source":        export_source 
               , "src_page_html_url":    src_page_html_url 
               , "page_type":           "main"
               , "katex_macros":         utils.base64_encode( renderer.katex_macros )
               , "unicode_emoji_favicon": unicode_emoji_favicon
               , "favicon":               favicon
               , "favicon_mimetype":      favicon_mimetype
               , "content_language":      renderer.language or content_language 
              }
        ## html = tpl.render(env)
        html = static_html_renderer(env)
        outfile.write_text(html)
    print(" [*] Compilation terminated successfully ok.")
    # math_svg_cache_folder = root / ".data/svgcache"
    # if not self_contained and compile_latex and math_svg_cache_folder.is_dir():
    #    utils.copy_folder(math_svg_cache_folder, out / "svgcache")
    # exit(0)



def make_template_renderer(module, template_file: str):
    template  = utils.read_resource(module, template_file)
    tpl = jinja2.Template(template)
    def render(environment: Optional[Dict], **kawargs) -> str:
        out = tpl.render(environment, **kawargs)
        return out
    return render
    

def get_font_data(font_key: str):
    for x in fonts_database:
        key = x.get("key", "")
        ## print(" [TRACE] key = ", key)
        if key == font_key:
            return x 
    return None


def copy_font_files(font_key: str, dest: pathlib.Path):
    data = get_font_data(font_key)
    if not data:
        return
    regular = data.get("regular")
    italic = data.get("italic")
    bold = data.get("bold")
    bold_italic = data.get("bold-italic")
    if regular:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + regular) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if italic:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + italic) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if bold:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + bold) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)
    if bold_italic:
       f = utils.get_path_to_resource_file(mwiki, "static/fonts/" + bold_italic) 
       if not f.exists():
           raise RuntimeError(f"File {f} not found")
       shutil.copy(f, dest)


def render_font_data_by_family( family: str
                              , root_url: str
                              , self_contained: bool = False
                              , root_path: Optional[pathlib.Path] = None) -> str:
    font_data = fonts_database_by_name.get(family) or {} 
    font_key  =  font_data.get("key") or ""
    out       = render_font_data(font_key, root_url, self_contained, root_path)
    return out 
       

def render_font_data(  key: str 
                     , root_url: str                = ""
                     , self_contained: bool         = False
                     , root_path: Optional[pathlib.Path] = None
                     ) -> str:
    data = get_font_data(key)
    if not data:
        return ""
    ## print(" [TRACE] root_path = " + str(root_path))
    family = data.get("family")
    has_italic = "italic" in data
    has_bold   = "bold" in data
    has_bold_italic = "bold-italic" in data
    root = "" if root_url == "/" else root_url
    code = """
@font-face {
    font-family: '{{family}}';
    {% if has_italic %}
    font-style: {{font_style}};
    {% endif %}
    {% if has_bold %}
    font-weight: {{font_weight}};
    {% endif %}
    {%if not self_contained %}
    src: url('{{root}}/static/fonts/{{file}}');
    {% else %}
    src: url({{font_data_b64}});
    {% endif %}
}
    """
    tpl = jinja2.Template(code)
    font_face_regular_b64 = ""
    font_face_regular_file: pathlib.Path = root_path / ("static/fonts/" + data.get("regular", ""))
    ## 0print("font_file = ", font_face_regular_file)
    if self_contained and font_face_regular_file.is_file():
        font_face_regular_b64 = mwiki.utils.file_to_base64_data_uri(font_face_regular_file)
        ### print(f" regular font = {key} => " + font_face_regular_b64)
    font_face_regular = tpl.render(  family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("regular")
                                   , font_style = "normal"
                                   , font_weight = "normal"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_regular_b64 
                               )
    font_face_italic = ""
    font_face_italic_b64 = ""
    font_face_italic_file = root_path / ("static/fonts" + data.get("italic", ""))
    if self_contained and font_face_italic_file.is_file():
        font_face_regular_b64 = mwiki.utils.file_to_base64_data_uri(font_face_italic_file)
    if has_italic:
        font_face_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("italic")
                                   , font_style = "italic"
                                   , font_weight = "normal"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_italic_b64 
                               )
    
    font_face_bold = ""
    font_face_bold_b64 = ""
    font_face_bold_file = root_path / ("static/fonts/" + data.get("bold", ""))
    if self_contained and font_face_bold_file.is_file():
        font_face_bold_b64 = mwiki.utils.file_to_base64_data_uri(font_face_bold_file)
    if has_bold:
        font_face_bold = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold")
                                   , font_style = "normal"
                                   , font_weight = "bold"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_bold_b64 
                               )
    font_face_bold_italic = ""
    font_face_bold_italic_b64 = ""
    font_face_bold_italic_file = root_path / ("static/fonts/" + data.get("bold-italic", ""))
    if self_contained and font_face_bold_file.is_file():
        font_face_bold_italic_b64 = mwiki.utils.file_to_base64_data_uri(font_face_bold_italic_file)
    if has_bold_italic:
        font_face_bold_italic = tpl.render(
                                     family = family
                                   , has_italic = has_italic
                                   , has_bold = has_bold
                                   , has_bold_italic = has_bold_italic
                                   , file = data.get("bold-italic", "")
                                   , font_style = "italic"
                                   , font_weight = "bold"
                                   , root = root
                                   , self_contained = self_contained 
                                   , font_data_b64 = font_face_bold_italic_b64 
                               )
    out = font_face_regular 
    out = out + "\n\n" + font_face_italic if font_face_italic != "" else out
    out = out + "\n\n" + font_face_bold   if font_face_bold   != "" else out
    out = out + "\n\n" + font_face_bold_italic   if font_face_bold_italic != "" else out
    return out 

# Fields: 
#    key: unique name for the font without whitespace (replaced by dash '-')
#    family:       font family name
#    regular:      regular font file
#    italic:       italic  font file
#    bold:         bold font file
#    bold-italic:  bold italic font file
#    info:         font description 
#    role:         "title", "code"  (optional)
#    latex:        True or False => If true indicates that the font is LaTeX derived font
# 
fonts_database  = [
    {
          "key":     "computer-modern"
        , "family":  "Computer Modern"
        , "regular": "computer-modern-normal.ttf"
        , "italic":  "computer-modern-italic.ttf"
        , "bold":    "computer-modern-bold.ttf"
        , "info":    "Standard LaTeX font created by emeritus professor Donald Knuth."
        , "latex":   True
    }
   ,{
          "key":          "ibm-plex-mono"
        , "family":       "IBM Plex Mono"
        , "regular":      "IBM-Plex-Mono-normal.ttf"
        , "italic":       "IBM-Plex-Mono-italic.ttf"
        , "bold":         "IBM-Plex-Mono-bold.ttf"
        , "bold-italic":  "IBM-Plex-Mono-bold-italic.ttf"
        , "info":         "Old school nostalgia font that mimics type writers."
    }
   ,{
          "key":     "chicago"
        , "family":  "Chicago MacOS"
        , "regular": "ChicagoFLF.ttf"
        , "info":    "Recrefation of the nostagia Susan Kare's font/typeface used by Apple's Mac OS System 7."
    }
   ,{
        "key":     "neo-euler"
      , "family":  "Neo Euler"
      , "regular": "neo-euler.otf"
      , "info":    "Latex font that attempts to mimic a mathematician handwriting in blackboard."
   }
   ,{
          "key":     "news-reader"
        , "family":  "NewsReader"
        , "regular":  "NewsReader.woff2"
    }
   ,{
          "key":          "literata"
        , "family":       "Literata"
        , "regular":      "Literata-Regular.ttf"
        , "italic":       "Literata-Italic.ttf"
        , "bold":         "Literata-Bold.ttf"
        , "info":         "Serif Typeface designed for Google Play books."
    }
   ,{
          "key":         "literata-variable"
        , "family":      "Literata-Regular" 
        , "regular":     "literata-variable-font-opsz.ttf" 
        , "italic":      "literata-variable-font-italic-opsz.ttf" 
        , "info":         "Serif Typeface designed for Google Play books."
    }
   ,{
         "key":          "commint-mono"
       , "family":       "Commit Mono"
       , "regular":      "CommitMono-400-Regular.otf"
       , "italic":       "CommitMono-400-Italic.otf"
       , "bold":         "CommitMono-700-Regular.otf"
       , "bold-italic":  "CommitMono-700-Italic.otf"
    }
    ,{
         "key":    "logic-monospace-regular"
       , "family":  "Logic Monospace Regular"
       , "regular": "LogicMonospace-Regular.woff2"
    }
    ,{
          "key":          "go-mono"
        , "family":       "Go Mono"
        , "regular":      "Go-Mono.ttf"
        , "italic":       "Go-Mono-Bold.ttf"
        , "bold":         "Go-Mono-Bold.ttf"
        , "bold-italic":  "Go-Mono-Bold-Italic.ttf"
    }
   ,{
         "key":    "logic-monospace-medium"
       , "family": "Logic Monospace Medium"
       , "regular": "LogicMonospace-Medium.woff2"
    }
   ,{
         "key":   "libertinus-mono"
       , "family": "Libertinus Mono"
       , "regular": "LibertinusMono-Regular.woff2"
    }
   ,{
           "key": "julia-mono"
         , "family":  "Julia Mono"
         , "regular": "JuliaMono-Regular.woff2"  
         , "italic":  "JuliaMono-RegularItalic.woff2"  
         , "bold":    "JuliaMono-Bold.woff2"  
    }
    ,{
          "key":    "jetbrains-mono"
        , "family": "JetBrains Mono"
        , "regular": "JetBrainsMono-400-Normal.woff2"
        , "bold":    "JetBrainsMono-700-Normal.woff2"
    }
   ,{
         "key": "julia-mono-light"
       , "familiy": "Julia Mono Light"
       , "regular": "JuliaMono-Light.woff2"
       , "italic":  "JuliaMono-LightItalic.woff2"
       , "bold":    "JuliaMono-Bold.woff2"  
   }
   ,{
          "key":          "libertinus-sans"
        , "family":       "Libertinus Sans"
        , "regular":      "LibertinusSans-Regular.woff2"
        , "italic":       "LibertinusSans-Italic.woff2"
        , "bold":         "LibertinusSanas-Bold.woff2"
    }
    ,{
          "key":          "libertinus-serif"
        , "family":       "Libertinus Serif"
        , "regular":      "LibertinusSerif-Regular.woff2"
        , "italic":       "LibertinusSerif-Italic.woff2"
        , "bold":         "LibertinusSerif-Bold.woff2"
        , "bold-italic":  "LibertinusSerif-BoldItalic.woff2"
    }    
   ,{
         "key":     "libertinus-serif-display"
       , "family":  "Libertinus Serif Display"
       , "regular": "LibertinusSerifDisplay-Regular.woff2"
   }
   ,{
        "key":         "commint-mono"
      , "family":      "Commint Mono"
      , "regular":     "CommitMono-400-Regular.otf"
      , "italic":      "CommitMono-400-Italic.otf"
      , "bold":        "CommitMono-700-Regular.otf"
      , "bold-italic": "CommitMono-700-Italic.otf"
    
    }
    ,{
          "key":      "DMMono Regular"
        , "family":   "DMMono Regular"
        , "regular":  "DMMono-Regular.woff2"
    }
    ,{
          "key":     "DMMono Medium"
        , "family":  "DMMono Medium"
        , "regular": 'DMMono-Medium.woff2'
    }
   ,{
          "key":      "range-mono"
        , "family":   "Range Mono"
        , "regular":  "range-mono-medium-webfont.woff"
    }
    ,{
          "key":         "ia-writer-quattro-s"
        , "family":      "iA Writer Quatro S"
        , "regular":     "iA-Writer-Quattro-S-regular.woff2"
        , "italic":      "iA-Writer-Quattro-S-italic.woff2"
        , "bold":        "iA-Writer-Quattro-S-bold.woff2"
        , "bold-itliac": "iA-Writer-Quattro-S-bold-italic.woff2"
    }
   ,{
          "key":      "range"
        , "family":   "Range"
        , "regular":  "range-regular-webfont.woff"
    }    
   ,{
         "key":     "rokkit-semibold"
       , "family":  "Rokkit Semibold"
       , "regular": "rokkit-semibold.woff2"
   }
   ,{
         "key":           "epson-dotmatrix"
       , "family":        "Epson DotMatrix"
       , "regular":       "DotMatrix-Regular.otf"
       , "italic":        "DotMatrix-Italic.otf"
       , "bold":          "DotMatrix-Bold.otf"
       , "bold-italic":   "DotMatrix-BoldItalic.otf"
       , "info": ("Font that mimics Epson's dot-matrix font used in"
                 " the 1980's for * printing code in computer magazines.")
   }
   ,{
         "key":           "epson-dotmatrixduo"
       , "family":        "Epson DotMatrixDuo"
       , "regular":       "DotMatrixDuo-CondensedRegular.otf"
       , "italic":        "DotMatrixDuo-CondensedItalic.otf"
       , "bold":          "DotMatrixDuo-CondensedBold.otf"
       , "bold-italic":   "DotMatrixDuo-CondensedBoldItalic.otf"
       , "info": ("Font that mimics Epson's dot-matrix font used in"
                 " the 1980's for * printing code in computer magazines.")
   }
   
   ,{
         "key":           "epson-dotmatrixvarduo"
       , "family":        "Epson DotMatrixVarDuo"
       , "regular":       "DotMatrixVarDuo-Regular.otf"
       , "italic":        "DotMatrixVarDuo-Italic.otf"
       , "bold":          "DotMatrixVarDuo-Bold.otf"
       , "bold-italic":   "DotMatrixVarDuo-BoldItalic.otf"
       , "info": ("Font that mimics Epson's dot-matrix font used in"
                 " the 1980's for * printing code in computer magazines.")
   }
   ,{
        "key":     "comorant-light"
      , "family":  "Comorant Light"
      , "regular": "Comorant-Light.woff2"
   }
   ,{
        "key":     "crimson"
      , "family":  "Crimson"
      , "regular": "crimson-roman.woff"
      , "italic":  "crimson-italic.woff"
      , "bold":    "crimson-bold.woff"
        
    }
    ,{
          "key":     "linux-libertine"
        , "family":  "Linux Libertine"
        , "regular": "LinuxLibertine-Regular.woff"
        , "italic":  "LinuxLibertine-Italic.woff"
        , "bold":    "LinuxLibertine-Bold.woff"
    }
    ,{
          "family":  "EBGaramond"
        , "key":     "ebgaramond"
        , "regular": "EBGaramond-400-Normal.woff2"
        , "italic":  "EBGaramond-400-Italic.woff2"
    }
   ,{
        "key":     "munson"
      , "family":  "Munson"
      , "regular": "munson-roman.woff2"
      , "italic":  "munson-italic.woff2"
      , "bold":    "munson-bold.woff2"
    }
   ,{
        "key":     "jackwrite"
      , "family":  "Jackwrite"
      , "regular": "Jackwrite.woff2"
      , "info":    "Nostalgic noir font/typeface that mimics typewriter ink leaked on old paper."
   }

   ,{
        "key":     "jackwrite-bold"
      , "family":  "Jackwrite Bold"
      , "regular": "JackwriteBold.woff2"
      , "info":    "Nostalgic noir font/typeface that mimics typewriter ink leaked on old paper."
   }
   ,{
         "key":     "essays1743"
       , "family":  "Essays1743"
       , "regular": "Essays1743.woff"
       , "info":    "Nostalgia noir font\typeface that looks like typewriter font with leaked ink."
   }
   ,{
       "key":    "cmu-concrete"
      ,"family": "CMU Concrete"
      ,"regular": "cmu-concrete-regular.woff"
      ,"italic": "cmu-concrete-italic.woff"
   }

   ,{
       "key":    "cmu-sans-serif"
      ,"family": "CMU Sans Serif"
      ,"regular": "cmu-sans-serif-regular.woff"
      ,"italic":  "cmu-sans-serif-bold.woff"
   }
   ,{
        "key":    "peachi-medium"
      , "family": "Peachi Medium"   
      , "regular": "peachi-medium.woff2"
      , "role":   "title"
    }
   ,{
        "key":     "fondamento"
      , "family":  "Fondamento"   
      , "regular": "fondamento-regular.woff2"
      , "role":   "title"
   }   
   ,{
         "key":     "bricolage-grotesque"
       , "family":  "Bricolage Grotesque"
       , "regular": "bricolage-grotesque-latin-normal.woff2"
   }
   ,{
          "key":    "saira-thin-normal"
        , "family": "Saira Thin Normal"
        , "regular": "saira-latin-thin.woff2"
        , "role":   "title"
    }

    ,{
          "key":    "saira-thin-bold"
        , "family": "Saira Thin Bold"
        , "regular": "saira-latin-thin-bold.woff2"
        , "role":   "title"
    }
    ,{
         "key":     "dinweb-light"
       , "family":  "DINWeb-Light"
       , "regular": "DINWeb-Light.woff"
       , "role":    "title"
    }
    ,{
         "key":      "dinweb-medium"
       , "family":   "DINWeb-Medium"
       , "regular":  "DINWeb-Medium.woff"
       , "role":   "title"
        
    }
    ,{
        "key":     "dinweb-black"
      , "family":  "DINWeb-Black"
      , "regular": "DINWeb-Black.woff"
      , "role":   "title"
        
    }
    ,{
        "key":     "graphik-regular"
      , "family":  "Graphik Regular"
      , "regular": "Graphik-Regular-Web.woff"
      , "role":   "title"
        
    },
    {
          "key":     "space-grotesk"
        , "family":  "Space Grotesk"
        , "regular": "space-grotesk-light.woff2"
        , "bold":    "space-grotesk-v16-latin-700.woff2"
    }
    ,{
         "key":         "averia"
       , "family":      "Averia"
       , "regular":     "Averia-Regular.woff2"
       , "italic":      "Averia-Italic.woff2"
       , "bold":        "Averia-Bold.woff2"
       , "bold-italic": "Averia-Bold-Italic.woff2"

    }
   ,{
         "key":         "averia-sans"
       , "family":      "AveriaSans"
       , "regular":     "AveriaSans-Regular.woff2"
       , "italic":      "AveriaSans-Italic.woff2"
       , "bold":        "AveriaSans-Bold.woff2"
       , "bold-italic": "AveriaSans-Bold-Italic.woff2"
    }
   ,{
         "key":         "averia-gruesa"
       , "family":      "Averia Gruesa"
       , "regular":     "Averia-Gruesa.woff2"
    }
    ,{
         "key":         "notosans"
       , "family":      "NotoSans"
       , "regular":     "NotoSans-Regular.woff2"
       , "italic":      "NotoSans-Italic.woff2"
       , "bold":        "NotoSans-BoldBold.woff2"
       , "bold-italic": "NotoSans-BoldItalic.woff2"

    }
    ,{
          "key":    "textura-modern"
        , "family": "Textura Modern"
        , "regular": "TexturaModern.ttf"
        , "info":    "Modieval goth-like font."
        , "role":    "title"
    }
    ,{
          "key":    "bastarda"
        , "family": "Bastarda"
        , "regular": "Bastarda.otf"
        , "info":    "Modieval goth-like font used in framce."
        , "role":    "title"
    }
    ,{
          "key":    "orbitron-bold"
        , "family": "Orbitron Bold"
        , "regular": "Orbitron-Bold.woff2"
    }
   ,{
         "key":     "roboto"
       , "family":  "Roboto"
       , "regular": "roboto-regular.woff2"
       , "bold":    "roboto-medium.woff2"
   }
]

fonts_database_by_name = dict([(x.get("family"), x) for x in fonts_database])

monospace_fonts = [
      "Commit Mono"
    , "IBM Plex Mono"
    , "Libertinus Mono"
    , "JetBrains Mono"
    , "Julia Mono"
    , "Julia Mono Light"
    , "Range Mono"
    , "DMMono Regular"
    , "DMMono Medium"
    , "Epson DotMatrix"
    , "Epson DotMatrixDuo"
    , "Epson DotMatrixVarDuo"
]

