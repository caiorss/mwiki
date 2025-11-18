"""Module for watching file system changes in the Wiki repository.
"""
import os
import json 
import pathlib
from typing import Dict, List 
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
import watchdog.events as events
import mwiki as mw
import pathlib
import mwiki.utils as utils
import mwiki.search as search
from   mwiki.models import MwikiConfig
from .mparser import parse_file, SyntaxTreeNode
##from mwiki.app import MWIKI_REPOSITORY_PATH


## mwiki_path = MwikiConfig.path ## MWIKI_REPOSITORY_PATH
##mwiki_path = utils.expand_path(os.getenv("MWIKI_PATH", os.getcwd()))
HASHTAG_NODE_TYPE = "wiki_tag_inline"

# print(" [WATCHER] Start Watcher Process mwiki_path = ", mwiki_path)

##class Event(LoggingEventHandler):

    #def on_modified(self, event):
    #    print(f" [WATCHER] modified event = {event}")
    #    if event.event_type == "modified" and event.src_path.endswith(".md"):
    #        print(f" [TRACE] Modified = {event}")
    #         ## print(" [TRACE] Updating tags.")
     #        ##update_tags_index()

    #def __init__(self):
    #    super().__init__()
    #    print(f" [WATCHER] Created Event object for watching #{MwikiConfig.path}")


class Event(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        print(f" [TRACE] on_any_event => {event}")

    def on_created(self, event):
        print(f"Created event => {event}")

    def on_deleted(self, event):
        print(f"Deleted event => {event}")

    def dispatch(self, event):
        print(f" [WATCHER] dispatch Event = {event}")
        mwiki_path = MwikiConfig.path
        if event.event_type == "modified" and event.src_path.endswith(".md"):
            print(f" [WATCHER] Updating searching index of {event.src_path}")
            search.update_index_page(pathlib.Path(mwiki_path), pathlib.Path(event.src_path))
            print(" [WATCHER] Updating tags.")
            update_tags_index()

def observe_wiki(wikipath: str):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Event() #LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path = wikipath, recursive=True)
    observer.start()
    print("Block this thread")
    ## observer.join()
    print("Start try/except block")
    try:
        while True:
            time.sleep(1)
            ## observer.join()
        #while observer.is_alive():
        #    observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        ##observer.stop()
        observer.join()
        observer.stop()
    #try:
    #    while True:
    #        time.sleep(1)
    #observer.join()


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
    mwiki_path = MwikiConfig.path
    root = pathlib.Path(mwiki_path)
    cache_directory = root.joinpath(".data")
    tags_cache_file = cache_directory.joinpath("tags_cache.json")
    utils.mkdir(cache_directory)
    pages = root.rglob("*.md")
    ## Inverted index data structure
    index = {}
    tags_list = set()
    documents = []
    out = {}
    if tags_cache_file.exists():
        with open(tags_cache_file, "r") as fd:
            try:
                out = json.load(fd)
                index = dict(out.get("index", []))
                tags_list = set(out.get("tags", []))
                documents = out.get("documents", [])
            except json.JSONDecodeError as ex:
                print(" [ERROR] Line 157 => ", ex)
    while True:
        p = next(pages, None)
        if p is None: break
        if tags_cache_file.exists() and \
            os.path.getmtime(p) < os.path.getmtime(tags_cache_file):
            continue
        print(f" [WATCHER] Processing file {p}")
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

def index_wiki_repository():
    root = pathlib.Path(MwikiConfig.path)
    cache_dir = root / ".data/search_index_tags"
    utils.mkdir(cache_dir)
    pages = root.rglob("*.md")
    print(" [INFO] Updating Search Index")
    while (p := next(pages, None)) is not None:
        # Remove .md suffix
        mtime = p.stat().st_mtime
        name = p.name.split(".")[0] + ".txt"
        search_index_tag_file = cache_dir / p.parent.relative_to(root) / name
        if search_index_tag_file.exists() and \
            mtime < search_index_tag_file.stat().st_mtime:
            continue
        if not search_index_tag_file.parent.exists():
            search_index_tag_file.parent.mkdir(exist_ok=True)
        print(f" [INFO] Indexing wiki page {p}")
        search.update_index_page(root, p)
        search_index_tag_file.write_text(f"{mtime}")
        print(f" [INFO] Finished indexing wiki page {p} Ok.")
    print(" [INFO] Search index updated OK.")

def watch():
    print(" [TRACE] Starting scanning ", MwikiConfig.path)
    while True:
        index_wiki_repository()
        update_tags_index()
        time.sleep(5)


## Entry Point of this module
def watch_():
    print(f" [WATCHER] Start indexing directory: '{MwikiConfig.path}'")
    print(" [WATCHER] Monitoring Wikipath. Extracting tags.")
    update_tags_index()
    print(" [WATCHER] Extracting tags terminated ok.")
    observe_wiki(MwikiConfig.path)





if __name__ == "__main__":
    watch()

