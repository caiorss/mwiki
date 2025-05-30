"""Extends markdown_it_py parser for implementing hyperlinks to Mastodon handles.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Callable, Match, Sequence, TypedDict

from markdown_it import MarkdownIt
from markdown_it.common.utils import charCodeAt

if TYPE_CHECKING:
    from markdown_it.renderer import RendererProtocol
    from markdown_it.rules_block import StateBlock
    from markdown_it.rules_inline import StateInline
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict


### print(" [TRACE Loading Wikilinks Plugin]")

RULE_NAME = "mastodon_handle_link"
MAIN_DELIMITER = "at"

def mastodon_handle_plugin(
    md: MarkdownIt, delimiters: str = MAIN_DELIMITER, macros: Any = None
) -> None:
    """Turn mastodon handles into hyperlinks.

    Plugin for parsing mastodon handles and turning them into hyperlinks.
    For instance, the mastodon handle @kde@floss.social is turned into a hyperlink 
    to the URL https://floss.social/@kde.
    
    NOTE: A mastodon handle is equivalent to Twitter's user name @someUserName.

    """
    ## print(" [TRACE] Inside function WikiLink Plugin")
    macros = macros or {}
    ## breakpoint()

    if delimiters in rules:
        for rule_inline in rules[delimiters]["inline"]:
            md.inline.ruler.before(
                "escape", rule_inline["name"], make_inline_func(rule_inline)
            )

            def render_math_inline(
                self: RendererProtocol,
                tokens: Sequence[Token],
                idx: int,
                options: OptionsDict,
                env: EnvType,
            ) -> str:
                return rule_inline["tmpl"].format(  # noqa: B023
                    render(tokens[idx].content, False, macros)
                )

            ##print(" [TRACE] rule_inline = ", rule_inline)
            md.add_render_rule(rule_inline["name"], render_math_inline)

class _RuleDictReqType(TypedDict):
    name: str
    rex: re.Pattern[str]
    tmpl: str
    tag: str


class RuleDictType(_RuleDictReqType, total=False):
    # Note in Python 3.10+ could use Req annotation
    pre: Any
    post: Any


def applyRule(
    rule: RuleDictType, string: str, begin: int, inBlockquote: bool
) -> None | Match[str]:
    if not (
        string.startswith(rule["tag"], begin)
        and (rule["pre"](string, begin) if "pre" in rule else True)
    ):
        return None

    match = rule["rex"].match(string[begin:])

    if not match or match.start() != 0:
        return None

    lastIndex = match.end() + begin - 1
    if "post" in rule and not (
        rule["post"](string, lastIndex)  # valid post-condition
        # remove evil blockquote bug (https:#github.com/goessner/mdmath/issues/50)
        and (not inBlockquote or "\n" not in match.group(1))
    ):
        return None
    return match


def make_inline_func(rule: RuleDictType) -> Callable[[StateInline, bool], bool]:
    def _func(state: StateInline, silent: bool) -> bool:
        res = applyRule(rule, state.src, state.pos, False)
        if res:
            if not silent:
                token = state.push(rule["name"], RULE_NAME, 0)
                token.content = res[1]  # group 1 from regex ..
                token.info = res[2]     # group 2 from regex ...
                token.markup = rule["tag"]

            state.pos += res.end()

        return bool(res)

    return _func


def make_block_func(rule: RuleDictType) -> Callable[[StateBlock, int, int, bool], bool]:
    def _func(state: StateBlock, begLine: int, endLine: int, silent: bool) -> bool:
        begin = state.bMarks[begLine] + state.tShift[begLine]
        res = applyRule(rule, state.src, begin, state.parentType == "blockquote")
        if res:
            if not silent:
                token = state.push(rule["name"], RULE_NAME, 0)
                token.block = True
                token.content = res[1]
                token.info = res[len(res.groups())]
                token.markup = rule["tag"]

            line = begLine
            endpos = begin + res.end() - 1

            while line < endLine:
                if endpos >= state.bMarks[line] and endpos <= state.eMarks[line]:
                    # line for end of block math found ...
                    state.line = line + 1
                    break
                line += 1

        return bool(res)

    return _func



def render(tex: str, displayMode: bool, macros: Any) -> str:
    return tex
    # TODO better HTML renderer port for math
    # try:
    #     res = katex.renderToString(tex,{throwOnError:False,displayMode,macros})
    # except:
    #     res = tex+": "+err.message.replace("<","&lt;")
    # return res


def syntax_filter(src: str, beg: int) -> bool:
    """Function for regex desambiguation"""
    result = "(" not in src or "]" not in src
    return result

rules: dict[str, dict[str, list[RuleDictType]]] = {

    MAIN_DELIMITER: {
        "inline": [
           {
                #### "name": "math_inline",
                 "name": "mastodon_handle_inline"
                ##, "rex": re.compile(r"@(.+)@([\w\.]+)\s\n?", flags = re.M | re.)
               , "rex": re.compile(r"@(.+)@([\w\.]+)")
               , "tmpl": """<a href="https://{1}/@{2}" class="link-external" >@{1}@{2}</a>"""
               , "tag": "@"
               , "pre": syntax_filter
           }

        ]
    },
}
