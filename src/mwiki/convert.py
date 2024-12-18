"""Conversion from other markdown/markup formast to MWiki's markup language.

"""
import sys 
import re 
import pathlib 
from typing import Optional
import click 

def replace_underline(line: str) -> str:
    n = len(line)
    k = 0
    def peek():
        if k < n: return line[k]
        return ""
    def nextch():
        if k <= n: k = k + 1
    disable = False
    output = "" 
    while True:
        ch = peek()
        if ch == "": break
        output += ch 
        if not disable and ch == "_":
            pass 


def convert_source(content: str) -> str:
    link_pat = re.compile(r"\[\[(.+)\]\[(.+)\]\]")
    # Covert-org-mode link to markdown likns
    out = re.sub(link_pat, r"[\2](<\1>)", content)
    def replace_heading(m: re.Match) -> str:
        n = len(m.group(1)) - 1
        out = "\n" + "##" * n  + " " if n != 0 else ""
        return out
    ##out = temp.strip()
    # Turn '#+BEGIN_SRC sh' into '```sh` markdown code block`
    out = re.sub(r"#\+BEGIN_SRC[ \t]*(\S+)?", r"```\1\n", out)
    out = out.replace("#+END_SRC", "```")
    # Replace =inline code block= by `inline code block`
    out = re.sub("=(.*?)=", r"\1", out)
    # Replace blocks #+BEGIN_QUOTE and #+END_QUOTE 
    def replace_quote(m: re.Match) -> str:
        text: str = m.group(1)
        out  = "> " + " ".join([lin.strip() for lin in text.splitlines() ])
        return out
    out = re.sub(r"#\+BEGIN_QUOTE((\n|.)+)#\+END_QUOTE", replace_quote, out)   

    # Reoplace _underlin text_ by <u>underline text</u>
    temp = ""
    flag = False
    lines = []
    for lin in out.splitlines():
        _lin = lin
        if lin.startswith("```"):
            flag = not flag 
        if not flag:
            # Repalce underline text 
            _lin = re.sub(r"\s_(.*?)_",   r" <u>\1</u>", _lin)
            # Remove Org-mode directives
            if _lin.startswith("#+") or lin.startswith("#"):
                _lin = ""
            if _lin.startswith("*"):
                # Replace section heading ** by ##, * by # and so on.
                _lin = re.sub(r"(\*+)[ \t]+", replace_heading, _lin)   
            # Replace bold text 
            _lin = re.sub(r"\*(.*)\*", r"**\1**", _lin)
            # Replace Italic 
            _lin = re.sub("\\s\/(.*?)\/\\s?",   r" *\1* ", _lin)
            # Transform Latex Equations/Expressions
            _lin = (_lin.replace(r"\begin{equation}",   "$$")
                        .replace(r"\end{equation}",     "$$")
                        .replace(r"\begin{equation*}",  "$$")
                        .replace(r"\end{equation*}",    "$$")
                        .replace(r"\begin{eqnarray}",   "$$\n\\begin{split}")
                        .replace(r"\end{eqnarray}",     "\n\\end{split}\n$$")
                        .replace(r"\begin{eqnarray*}",  "$$\n\\begin{split}\n")
                        .replace(r"\end{eqnarray*}",    "\\end{split}\n$$")
                        .replace(r"\begin{align}",      "$$\n\\begin{split}\n")
                        .replace(r"\begin{align*}",     "$$\n\\begin{split}\n")
                        .replace(r"\end{align*}",       "\\end{split}\n$$")                       
                        .replace(r"\end{align}",        "\\end{split}\n$$")
                       )       
        ###_lin = _lin if not (_lin.endswith(" ") or _lin.endswith("\t")) else _lin + " "
        ## temp = temp + "\n" + _lin
        lines.append(_lin)
    ## print("\n".join(lines))
    ## return 
    gen = iter(lines)
    temp = ""
    flag = False
    state_start = 0 
    state_join_lines  = 1
    state =  state_start
    while True:
        line_: Optional[str] = next(gen, None) 
        if line_ is None: break
        line: str = line_ or ""
        line = "\n" if line.strip() == "" else line
        if line.startswith("```") or line.startswith("$$"):
            flag = not flag
        if state == state_start:
            if not flag and not line.startswith(" ") \
                and not line.strip() == "" \
                and not line.startswith("$$") \
                and not line.startswith("```")\
                and not line.startswith("|"):
                state = state_join_lines
                temp = temp + line 
                ## print(" [TRACE] join lines start => line = ", line)
                ## print(" [TRACE] join lines start => temp = ", temp)
            else:
                ## print(" [TRACE] join lines else => line = ", line)
                ## print(" [TRACE] join lines else => temp = ", temp)
                temp = temp + "\n" + line
        elif state == state_join_lines:
            if not line.startswith(" ") and not line.strip() == "" \
                and not line.startswith("$$") \
                and not line.startswith("```")\
                and not line.startswith("|"):
                temp = temp + " "  + line
            else:
                if line.startswith("$$") or line.startswith("```") or line.startswith("|"):
                    temp = temp + "\n" + line 
                    print(" [line] = ", line)
                    state = state_start
                else:
                    state = state_start
                    temp = temp + "\n" + line 
    return temp  

def convert_file(file: Optional[str], output: Optional[str]):
    """Convert from org-mode markup to markdown 
    """
    if file is None:
        print("Error expected --file, but none given")
        exit(1)
    pfile = pathlib.Path(file).resolve()
    if not pfile.is_file():
        print(f"Error {pfile} does not exist.")
        exit(1)
    content = pfile.read_text()
    out = convert_source(content)
    print(out)

@click.command()
@click.option("-f", "--file", default = None, 
                help = ( "Input markdown file to be converted." )
                )
@click.option("-o", "--output", default = None, 
                help = ( "Output file." )
                )
def main(file: Optional[str], output: Optional[str]):
    convert_file(file, output)


if __name__ == "__main__":
   main()
   ## convert("test.org", "")