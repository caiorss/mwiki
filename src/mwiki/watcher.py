import os
import json 
import pathlib
from typing import Dict, List 
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog.events as events
import mwiki as mw
import mwiki.utils as utils
from .mparser import parse_file, SyntaxTreeNode
from mwiki.app import MWIKI_REPOSITORY_PATH


mwiki_path = MWIKI_REPOSITORY_PATH 
HASHTAG_NODE_TYPE = "wiki_tag_inline"

root = pathlib.Path(mwiki_path)
cache_directory = root.joinpath(".data")
tags_cache_file = cache_directory.joinpath("tags_cache.json")
utils.mkdir(cache_directory)

print(" [TRACE] mwiki_path = ", mwiki_path)

class Event(LoggingEventHandler):
    ## def on_modified(self, event):
    ##     if event.event_type == "modified" and event.src_path.endswith(".md"):
    ##         print(" [TRACE] Updating tags.")
    ##         update_tags_index()
        
    def dispatch(self, event):
        if event.event_type == "modified" and event.src_path.endswith(".md"):
            print(" [TRACE] Updating tags.")
            update_tags_index()

def observe_wiki(wikipath: str):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Event() #LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, wikipath, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def get_hashtags(document: str, ast: SyntaxTreeNode) -> Dict[str, Dict[str, int]]:
    """Get all hashtags from the AST of a wiki page.
    For instance if a wiki page has the tags 
    #ai, #llm, #ai and #math, this function returns
    a inverted index, where each tag points to the 
    current document and contains a count of a each 
    tag. 
    """
    gen = ast.walk()
    #tags_set = set()
    # Inverted index 
    index = {}
    while True:
        node = next(gen , None)
        if node is None: 
            break
        elif node.type != HASHTAG_NODE_TYPE: 
            continue
        else:
            tag = node.content[1:] if node.content != "" else ""
            if tag[0].isdigit() or '(' in tag \
                                or ')' in tag \
                                or ']' in tag \
                                or '[' in tag \
                                or '#' in tag \
                                or '!' in tag \
                                or '?' in tag \
                                or '/' in tag \
                                or '*' in tag \
                                or '+' in tag \
                                or '=' in tag \
                                or ',' in tag \
                                or '"' in tag \
                                or ':' in tag \
                                or '.' in tag:
                  continue
            #tags_set.add(tag)
            if tag not in index:
                index[tag] = { document:  1 }
            else: 
                index[tag][document] += 1
    ##print(" [*] tags = ", tags_set)
    return index

def update_tags_index():
    root = pathlib.Path(mwiki_path)
    pages = root.rglob("*.md")
    ## Inverted index data structure
    index = {}
    tags_list = set()
    documents = []
    out = {}
    if tags_cache_file.exists():
        with open(tags_cache_file, "r") as fd:
            out = json.load(fd)
            index = dict(out.get("index", []))
            tags_list = set(out.get("tags", []))
            documents = out.get("documents", [])
    while True:
        p = next(pages, None)
        if p is None: break
        if tags_cache_file.exists() and \
            os.path.getmtime(p) < os.path.getmtime(tags_cache_file):
            continue
        print(f" [TRACE] Processing file {p}")
        doc = str(p.relative_to(root))
        if doc not in doc:
            documents.append(doc)
        ast = parse_file(p)
        tags = get_hashtags(doc, ast)
        #out = out.union(tags)
        ## breakpoint()
        for tag, data in tags.items():
            tags_list.add(tag)
            if tag not in index:
                index[tag] = data 
            else:
                for doc, count in data.items():
                    index[tag][doc] = count
        ## for x in tags_list:
        ##     if x not in index.keys():
        ##         tags_list.remove(x)
    out["index"] = list(index.items())
    out["tags"] = sorted(list(tags_list), key = str.casefold)
    out["documents"] = list(documents)
    ## breakpoint()
    with open(tags_cache_file, "w") as fd:
        json.dump(out, fd)
    ##return out 

if __name__ == "__main__":
    print(" [TRACE] Monitoring Wikipath. Extracting tags.")
    update_tags_index()
    print(" [TRACE] Extracting tags terminated ok.")
    observe_wiki(MWIKI_REPOSITORY_PATH)