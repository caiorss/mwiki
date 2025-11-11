import re 
import os
import os.path 
import json 
import pathlib
import hashlib
from typing import Optional, List, Tuple
import subprocess 
import multiprocessing
from markdown_it.tree import SyntaxTreeNode
import mwiki
import mwiki.utils as utils 
from mwiki.utils import Result
import mwiki.mparser as mparser 

# Module Exports 
__all__ = [ "LatexFormula" ]

def get_latex_macros_json(code: str):
    macros = get_latex_macros(code)
    out = json.dumps(macros)
    return out 

def get_latex_macros(code: str):
    pat_def1 = r"\\def(?P<d1>.+?)\{(?P<d2>.+?)\}\}"
    pat_cmd1 = r"\\newcommand\{(?P<c1>.+?)\}(\[.*?\])?\s*\{(?P<c2>.+?)\{(?P<c3>.+?)\}\s*\}" 
    pat_cmd2 = r"\\newcommand\{(?P<r1>.+?)\}(\[.*?\])?\{(?P<r2>.+?)\}"
    pat_opr  = r"\\DeclareMathOperator(?P<ostar>\*?)\{\s*(?P<o1>.+?)\}\{\s*(?P<o2>.+?)\s*\}"
    pat = f"{pat_def1}|{pat_cmd1}|{pat_cmd2}|{pat_opr}"
    # Initial position within the code to be parsed 
    text = code.strip()
    out = {}
    while text != "":
        if m := re.search(pat, text):
            start, end = m.span() 
            text = text[end:]
            #size = sum([1 if x is not None else 0 for x in m.groups()])
            #groups = [x for x in m.groups() if x is not None]
            dic = m.groupdict()
            if dic.get("o1"):
                lhs = dic["o1"]
                rhs = dic["o2"]
                ostar = dic.get("ostar", "")
                out[lhs.strip()] = r"\operatorname" + ostar + "{" + rhs.strip() + "}"
            elif dic.get("c1"):
                #lhs, rhs_, inner = groups
                lhs = dic["c1"]
                rhs = dic["c2"]
                inner = dic["c3"]
                out[lhs.strip()] = "%s{%s}" % (rhs.strip(), inner.strip())
            elif dic.get("r1"):
                lhs = dic["r1"]
                rhs = dic["r2"]
                out[lhs.strip()] = rhs.strip()
            elif dic.get("d1"):
                #lhs, rhs_, inner = groups
                lhs = dic["d1"]
                rhs = dic["d2"]
                out[lhs.strip()] = rhs.strip() + "}"
        else:
            break
    return out

class LatexFormula:
    """
    """
    
    def __init__(self, code: str, mwiki_path: pathlib.Path, inline: bool = False, inline_single = False):
        """
        Parameters:
         - mwiki_path: Path to the wiki directory.
         - code:       Latex code or formula to be compiled  
         - inline:     Flag that indicates whether the LaTeX formula is iniline
                       between single dollar signs `$<FORMULA>$` or non-iline
                       between double dollar signs `$$<FORMULA>$$`.
        """
        self._root = mwiki_path
        self._code = code
        self._inline = inline
        self._inline_single = inline_single
        data = code.encode("utf-8")
        self._hash = hashlib.sha1(data).hexdigest()
        self._file = self._hash + "_katex.html"
        cache = self._root / ".data/svgcache" 
        # Ensure that the SVG cache folder exists 
        cache.mkdir(exist_ok=True)
        self._path = cache / self._file

    @property
    def path(self) -> pathlib.Path:
        """Return path to cached SVG file"""
        return self._path

    @property
    def hash(self) -> str:
        return self._hash 

    @property
    def inline(self) -> bool:
        r"""
        Evaluates to true if the LaTeX formula is inline.

        A inline LaTeX formula has code between a pair of single
        dollar signs, such as `$f(x) = \sqrt{x^2}$` a non line
        LaTeX formula (display mode) written between a pair of
        double dollar signs, example

        ```latex 
        f(x) = \frac{\sqrt{x^2 - 10x}{x^3 + 3}}
        ```
        """
        return self._inline 
        
    @property
    def image(self) -> str:
        """Return name of corresponding SVG image file name."""
        return self._file

    @property
    def formula(self) -> str:
        return self._code
    
    @property 
    def cached(self) -> bool:
        """Return true if the corresponding SVG image file exists."""  
        return self._path.exists()

    def svg(self) -> Optional[str]:
        """Returns cached SVG image of compiled LaTeX code.
        NOTE: SVG stands for Scalable Vector Graphics. A XML
              vector graphics image file. 
        """
        if not self.cached:
            return None
        else:
            content = self.path.read_text() 
            return content 


    def html(self, embed: bool = False, export: bool = False, root_url = "/") -> str:
        """Return <img> html code for the current LaTeX formula (code). 

        Returns a html code containing img DOM element for the
        corresponding SVG image of the current math formula.

        Parameters:
          - embed => If this flag is set to true, the SVG image is embedded as
                     base64 SVG image in the <img> html code. This option is useful
                     for creating self-contained documents such as PDFs that are easy
                     to copy, send as attachment and view offline.
          - export => When this flag is set to true, a MWiki page is being exported
                      as a static website that can be served just by copying files
                      without any web/http server.  
        """
        ##if not self.cached:
        ##     self.compile()
        out = ""
        if self.path.is_file():
            out = self.path.read_text()
        else:
            out = f"""<div><p>Fail to compile Latex hash = {self.hash}</p> <pre>{utils.escape_html(self.formula)}</pre></div> """
        if not self.inline: 
            out = f"""<div class="math-container div-wiki-image">\n{out}\n</div>"""
        return out

    def compile(self, verbose = False):
        if self.cached:
            return
        out = compile_latex_to_html_katex(self._code, self.inline, verbose)
        if out.success:
            self.path.write_text(out.value)

    def html_(self, embed: bool = False, export: bool = False, root_url = "/") -> str:
        """Return <img> html code for the current LaTeX formula (code). 

        Returns a html code containing img DOM element for the
        corresponding SVG image of the current math formula.

        Parameters:
          - embed => If this flag is set to true, the SVG image is embedded as
                     base64 SVG image in the <img> html code. This option is useful
                     for creating self-contained documents such as PDFs that are easy
                     to copy, send as attachment and view offline.
          - export => When this flag is set to true, a MWiki page is being exported
                      as a static website that can be served just by copying files
                      without any web/http server.  
        """
        html = ""
        klass = "inline-math" if self.inline else "math"
        if self._inline_single:
            klass = "inline-math-single"
        root_url = root_url.strip("/") if root_url.endswith("/") else root_url 
        alt = utils.escape_html(self._code)
        src = f"/wiki/math/{self.image}" if not export else f"{root_url}/svgcache/{self.image}"
        if embed and self.cached:
            src = utils.file_to_base64_data_uri(self.path)
        html = f"""<a href="#equation-{self.hash}">
                    <img id="equation-{self.hash}" class="{klass}"
                    src="{src}" alt="{alt}" loading="lazy" ></a>"""
        if not self.inline: 
            html = f"""<div class="math-container div-wiki-image">\n{html}\n</div>"""
        ## print(" [DEBUG] math html = ", html)
        return html 

    def compile_(self, verbose = False): 
        eqtext = self._code 
        # svg = self.svg() if self.cached or "" 
        svg = self.svg() if self.cached else ""
        if svg != "":
            return 
        if not self.cached or svg == "": 
            if verbose:
                print(f"\n[TRACE] Compiling equation to {self.path}")
                print("Equation = \n", eqtext)
            svg = compile_latex_to_svg(eqtext, self.inline)
            if svg != "":
                self.path.write_text(svg)
            ## print("\n\n--------------------------------------")

    @classmethod
    def compile_document(cls, pagefile: pathlib.Path, mwiki_path: pathlib.Path, verbose = False):
        """
        Compile all LaTeX formulas from a particular MWiki page to SVG files. 
        """
        source = pagefile.read_text()
        tokens = mparser.MdParser.parse(source)
        ast    = SyntaxTreeNode(tokens)
        ## print(" [*] Compiling File: ", pagefile)
        # Get generator object to iterate over the AST
        # (Abstract Syntax Tree nods)
        gen = ast.walk()
        while True:
            node = next(gen, None)
            tex = None 
            if node is None: break
            if node.type == "math_block":
                tex = LatexFormula(node.content, mwiki_path, inline = False)
            elif node.type == "math_inline" \
                or node.type == "math_single":
                tex = LatexFormula(node.content, mwiki_path, inline = True)
            # Code block ```{math} ... ```
            elif node.type == "fence":
                assert node.tag == "code"
                info = node.info if node.info != "" else "text" 
                if info == "{math}":
                    content, directives = mparser.get_code_block_directives(node.content)
                    #label = f'id="{u}"' if (u := directives.get("label")) else ""
                    tex = LatexFormula(content, mwiki_path, inline = False)
            if tex is not None:
                tex.compile(verbose = verbose)

    @classmethod
    def compile_document_parallel(cls, pagefile: pathlib.Path
                                  , mwiki_path: pathlib.Path, verbose = False, size = 6):
        
        equations = get_latex_expressions(pagefile, mwiki_path)
        with multiprocessing.Pool(size) as p:
            p.map(compile_, equations) 
            p.close()
            # Wait for all tasks termination
            p.join()


def compile_(x):
    code, inline, mwiki_path, verbose = x 
    tex = LatexFormula(code, mwiki_path, inline = inline)
    svg = tex.svg() if tex.cached else ""
    if not tex.cached or svg == "":
        tex.compile(verbose = verbose)

def get_latex_expressions(pagefile: pathlib.Path
                        , mwiki_path: pathlib.Path
                        , verbose = False) -> List[Tuple[str, bool, pathlib.Path, bool]]:
    source: str = pagefile.read_text()
    ## source = re.sub(r"^$$", "\n$$", source) 
    tokens = mparser.MdParser.parse(source)
    ast    = SyntaxTreeNode(tokens)
    out    = get_latex_expressions_ast(ast, mwiki_path, verbose)            #label = f'id="{u}"' if (u := directives.get("label")) else ""
    return out

def get_latex_expressions_ast(ast
                        , mwiki_path: pathlib.Path
                        , verbose = False) -> List[Tuple[str, bool, pathlib.Path, bool]]:
 
    # Get generator object to iterate over the AST
    # (Abstract Syntax Tree nods)
    gen = ast.walk()
    mathblocks = []
    while True:
        node = next(gen, None)
        if node is None: break
        if node.type == "math_block":
            x = (node.content, False, mwiki_path, verbose)
            mathblocks.append(x)
        elif node.type == "math_inline" \
            or node.type == "math_single":
            x =  (node.content, "inline", mwiki_path, verbose)
            mathblocks.append(x)
        # Code block ```{math} ... ```
        elif node.type == "fence":
            assert node.tag == "code"
            info = node.info if node.info != "" else "text" 
            content, directives = mparser.get_code_block_directives(node.content)
            if info == "{math}":
                x = (content, False, mwiki_path, verbose)
                mathblocks.append(x)
            elif info.startswith("{derivation}") \
                or info.startswith("{proof}") \
                or info.startswith("{foldable}") \
                or info.startswith("{example}") \
                or info.startswith("{solution}"):
                    tokens = mparser.MdParser.parse(content)
                    ast_    = SyntaxTreeNode(tokens)
                    xs     = get_latex_expressions_ast(ast_, mwiki_path, verbose) 
                    mathblocks += xs
    return mathblocks

def compile_latex_to_html_katex(latex: str, inline: bool, verbose = False) -> Result:
    """Compile LaTeX code or fomula to html using KaTeX.
    NOTE: This feature requires NodeJS installed and the parent directory
    of the node command line application listed in the $PATH environment variable. 
    """
    # Remove latex \label{someLabel} and \eqref{someRefeence to a label constructs}
    # that are not supported by KaTeX.
    latex = re.sub(r"\\notag|\\(label|eqref)\{.*?\}", "", latex)
    latex = latex.strip()
    if latex == "":
        return Result.error("")
    katex_path = utils.get_path_to_resource_file(mwiki, "static/katex/node_modules/katex/cli.js")
    if not katex_path.is_file():
        raise RuntimeError("Path KaTex cli 'cli.js' file not found.")
    node_executable = os.getenv("MWIKI_NODE_PATH", "node") 
    args = [node_executable, katex_path]
    if not inline:
        args.append("--display-mode")
    ## verbose = True
    if verbose:
        print(" [TRACE] --------------------------------------- ")
        print(" [TRACE] Compiling formula: \n ", latex)
    proc = subprocess.Popen(args
                            , stdout = subprocess.PIPE
                            , stderr =subprocess.PIPE
                            , stdin = subprocess.PIPE
                        )
    stdout, stderr = proc.communicate( input = latex.encode("utf-8"))
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")
    if proc.returncode == 0 and verbose:
        print(" [TRACE] output = \n", stdout)
    if proc.returncode != 0 and verbose:
        print(" ------ ERROR ----------------------------------- ")
        print(" [TRACE] KaTeX compiled formula:\n ", latex)
        print(" [TRACE} Return Code = ", proc.returncode)
        print(" [TRACE] otuput = \n", stdout)
        print(" [TRACE] stderr = \n", stderr)
    out = Result.result(stdout) \
        if proc.returncode == 0 else Result.error(stderr)
    return out
    

def compile_latex_to_svg(latex, inline: bool, verbose = False) -> Optional[str]:
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

    On Fedora Linux based distributions, the LaTeX dependencies
    can be installed with

    ```sh
    $ sudo dnf install -y texlive-texlive-en.noarch
    $ sudo dnf install -y texlive-texlive-en.noarch texlive-pdfcprot.noarch
    ```
   
    """
    # Replace tabs by 4 spaces 
    code = latex
    code = code.replace("\t", "   ")
    # Remove empty lines
    code = "\n".join([x for x in code.splitlines() if x.strip() != '']).strip()
    code = ( code
                .replace(r"\begin{equation}", r"") 
                .replace(r"\end{equation}", r"") 
                .replace(r"\begin{equation*}", r"") 
                .replace(r"\end{equation*}", r"") 
                .replace(r"\begin{eqnarray}", r"\begin{align*}") 
                .replace(r"\end{eqnarray}", r"\end{align*}") 
                .replace(r"\begin{eqnarray*}", r"\begin{align*}") 
                .replace(r"\end{eqnarray*}", r"\end{align*}") 
                # Remove MathJax \require{cancel}
                .replace(r"\require{cancel}", "")
                .replace(r"\notag", "")
                .replace(r"\begin{split}", r"\begin{align*}")
                .replace(r"\end{split}",   r"\end{align*}")
                .replace(r"\begin{cases}", r"\begin{align*}")
                .replace(r"\end{cases}",   r"\end{align*}")
                # .replace(r"\begin{equation}", r"\[") 
                # .replace(r"\end{equation}", r"\]") 
                # .replace(r"\begin{equation*}", r"\[") 
                # .replace(r"\end{equation*}", r"\]") 
                .strip()
            )
    # Remove empty lines
    code = "\n".join([x for x in code.splitlines() if x.strip() != '']).strip()
    ## print(" [TRACE] code = \n", code)
    if inline:
        code = code.strip("$").replace("\\displaystyle", "")
        if code != r"\LaTeX": 
            code = f"$\\displaystyle {code}$"
    else:
        if not code.startswith(r"\begin{align}") \
           and not code.startswith(r"\begin{align*}")\
           and not code.startswith(r"\begin{algorithm}"):
            # and not code.startswith(r"\begin{split}"):
            code = "$$\n" + code + "\n$$"
    tex  = _latex_template.replace("{{math}}", code)
    # breakpoint()
    BASEFILE = "input"
    TEXFILE  = BASEFILE + ".tex"
    PDFFILE  = BASEFILE + ".pdf"
    CROP_PDFILE = BASEFILE + "-crop.pdf"
    SVGFILE     = BASEFILE + ".svg"
    svg = ""
    with utils.TempDirectory() as d:
        ## breakpoint()
        ## print(" [TRACE] within directory ", d.name())
        with open(TEXFILE, "w") as fd:
            fd.write(tex)
        ## print(" [INFO] Compiling with xelatex")
        proc = subprocess.run([  "xelatex"
                               , "-output-directory=."
                               , "-interaction=batchmode"
                              # , "-no-console"
                               , TEXFILE]
                               , capture_output=True , text=True)
        ##print(" [TRACE] proc = ", proc)
        ## breakpoint()
        if proc.returncode != 0:
            print(" [ERROR] Failed to compile latex formula ", code)
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
        ##print(" [INFO] Croping PDF .... ")
        if proc.returncode != 0:
            print(f" [ERROR] Failed to crop pdf of latex formula:\n{latex}")
            return ""
        assert os.path.isfile(CROP_PDFILE)
        if verbose:
            print(" [TRACE] Compiling LatTeX formula: \n", latex)
        ##print(" [INFO] Turnin PDF into SVG .... ")
        proc = subprocess.run([ "pdf2svg" , CROP_PDFILE, SVGFILE ]
                               , capture_output=True , text=True)
        if proc.returncode != 0:
            print("\n\n [ERROR] ---------------------------------------- ")
            print(f" [ERROR] Failed to turn pdf of latex formula into SVG. => \n{latex}")
            print( " [TRACE] tex = ", tex)
            print( " [TRACE] texfile = \n", tex)
            err = f"STDOUT: \n {proc.stdout} \nSTDERR: \n {proc.stderr}"
            print(err)
            ## out = Result(err = err)
            ##return out 
        with open(SVGFILE, "r") as fd:
            svg = fd.read()
        ##breakpoint()
    ##print(" [TRACE] Current directory after exit = ", os.getcwd())
    print(" --------------------------------------------------- ")
    print(" [TRACE] Compiled successfully\n", latex)
    print("\n [TRACE] Modified formula\n", code)
    if svg == "": 
        print(" [ERROR] failed to compile latex = ", latex)
        ## breakpoint()
    return svg
    #return Result(value = svg)
        
_latex_template = r"""
\documentclass[14pt]{article}
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

\begin{document}
{{math}}
\end{document}
"""

