"""Plugins for extending the syntax of markdown_it_py parser. 
"""
from ._wiki_link_plugin import wiki_link_plugin
from ._wiki_embed_plugin import wiki_embed_plugin
from ._wiki_text_highlight_plugin import wiki_text_highlight_plugin
from ._wiki_tag_plugin import wiki_tag_plugin
from ._wiki_mastodon_handle import mastodon_handle_plugin

__all__ = (  "wiki_link_plugin"
           , "wiki_embed_plugin"
           , "wiki_text_highlight_plugin" 
           , "wiki_tag_plugin"
           , "mastodon_handle_plugin"
          )