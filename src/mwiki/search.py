import re 
from typing import List, Dict 
import pathlib
import os.path
import yaml
import frontmatter
import whoosh.qparser as qparser
from whoosh import scoring
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.filedb.filestore import RamStorage
from whoosh.qparser import QueryParser, MultifieldParser


_ENGLISH_STOP_WORDS = [ 
                "and", "or", "any", "of", "some"
             , "in", "at", "on", "off", "our"
             , "your", "we", "yours", "yourself"
             , "his", "he", "himself", "her", "hers"
             , "it", "its", "itself", "they", "them"
             , "what", "which", "whom", "that", "these"
             , "those", "a", "an" 
             ]

def normalize_text(text: str) -> str:
    """Remove accents, such as ú or ç for making searching easier."""
    out = (text
                .replace("ã", "a")
                .replace("õ", "o")
                .replace("á", "a")
                .replace("à", "a")
                .replace("â", "a")
                .replace("ó", "o")
                .replace("ô", "o")
                .replace("í", "i")
                .replace("é", "e")
                .replace("ê", "e")
                .replace("ú", "u")
                .replace("ç", "c")
                .replace("ä", "a")
                .replace("Ä", "A")
                .replace("û", "u")
                .replace("ü", "u")
                .replace("ö", "o")
                .replace("ß", "ss")
            )
    return out


def file_contains(fileName: str, query: str, opt = "and_all", flag_normalize_words = False) -> bool:
    """Check whether a file (full path) contains a queyr string.
    Returns true if file contains a query string.
    NOTE: This function is case-indepedent.
    """
    with open(fileName) as fd:
        ### result = False
        basename = normalize_text(os.path.basename(fileName).lower())
        ## print(f" [TRACE] fileName = {fileName} ; basename = {basename}")
        query = normalize_text(query.lower())
        # Split whitespace
        ## queries = query.split()
        queries = []
        if flag_normalize_words:
            queries = [ _NORMALIZATION_DATABASE.get(x, x) for q in query.split() 
                        if (x := normalize_text(q))  not in _ENGLISH_STOP_WORDS  ]
        else:
            queries = [ x for q in query.split() 
                        if (x := normalize_text(q))  not in _ENGLISH_STOP_WORDS  ]
        ## queries_ = queries.copy()
        score = 0
        contail_all = True
        register = dict( (q, False) for q in queries )
        # WARNING: Never read the whole file to memory, becasue
        # if the file is 1 GB, then 1 GB memory will be consumed,
        # what can case OOM (Out-Of-Memory) issues and slow down
        # the server.
        while line := fd.readline():
            line_ = normalize_text(line.lower())
            ## line_ = normalize_words(line_) if flag_normalize_words else line_
            # Ignore case
            if opt == "exact" and query in line_ :
                result = True
                break
            # (OR) Returns true if is the file contains at
            # at least one word of the query.
            elif opt == "or_all":
                for q in queries:
                    if q in line_: 
                        score += 1
                        result = True
                        ##break
            # (AND) Returns treu if the file contains all words
            # from the input query
            elif opt == "and_all":
                for q in queries:
                    cond1 = re.findall(r"\b%s\b" % q if "#" not in q else q, line_) != []
                    cond2 = re.findall(r"\b%s\b" % q if "#" not in q else q, basename) != []
                    register[q] = register[q] or (cond1 or cond2)
                    if cond1: score += 1
                    if cond2: score += 3
                        ## queries_.remove(q)
                    ##break
        ## if score != 0:
        ##     print(f" [DEBUG] score = {score} ; file =  {fileName} ")
        if not all(register.values()):
            score = 0 
        return score

def grep_file(fileName: str, query: str) -> List[str]:
    """Return lines of a file that contains a given query string."""
    query = normalize_text(query.lower())
    queries = [normalize_text(q) for q in query.split()]
    lines = []
    n = 1
    with open(fileName) as fd:
        while line := fd.readline():
            line_ = normalize_text(line.lower())
            for q in queries:
                if q in line_: 
                    next_line = fd.readline()
                    lines.append((n, line + "\n" + next_line))
            n += 1
            # if query in normalize_text(line.lower()):
            #     lines.append((n, line))
            n += 1
    return lines  

def _get_frontmatter(path: pathlib.Path) -> Dict[str, str]:
    """Return wikipage metadata"""
    out = {  "title":   ""
           , "subject": ""
           , "keywords": ""
           , "uuid": ""
           , "label": ""
           }
    parser = frontmatter.Frontmatter()
    try:
        data = parser.read_file(str(path))
        data = data.get("attributes")
    except yaml.scanner.ScannerError as err:
        pass
    return out


_SEARCH_INDEX_PATH = ".data/search_index"

schema = Schema(  title       = TEXT(stored=True, field_boost = 4.0)
                , description = TEXT(stored=True, field_boost = 2.0)
                , content     = TEXT(stored=True)
                , path        = ID(stored=True, unique = True)
                )

storage = RamStorage()
index = storage.create_index(schema)


def search_index_exists(base_path: pathlib.Path) -> bool:
    folder = base_path / _SEARCH_INDEX_PATH
    out = folder.exists()
    return out

def index_page_(writer, base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    # Path to mwiki page file (markdown file) with .md extension
    afile = mwiki_page_file
    data    = _get_frontmatter(afile)
    title   =  data.get("title") or afile.name.split(".")[0]
    path    = str(afile.relative_to(base_path))
    content = afile.read_text()
    writer.add_document(  title = title
                        , description = data.get("description", "")
                        , content = normalize_text(content)
                        , path = path
                        )

def update_index_page_(writer, base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    # Path to mwiki page file (markdown file) with .md extension
    afile = mwiki_page_file
    data    = _get_frontmatter(afile)
    title   =  data.get("title") or afile.name.split(".")[0]
    path    = str(afile.relative_to(base_path))
    content = afile.read_text()
    print(" [TRACE] Updateing document " + str(afile))
    writer.update_document(  title = title
                        , description = data.get("description", "")
                        , content = normalize_text(content)
                        , path = path
                        )


def update_index_page(base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    """Update a search index metadata of MWiki markdown page file."""
    index_dir = base_path / _SEARCH_INDEX_PATH
    ix = open_dir(str(index_dir))
    writer = ix.writer()
    update_index_page_(writer, base_path, mwiki_page_file)
    writer.commit()

def add_index_page(base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    """Add MWiki page to search index."""
    afile = mwiki_page_file
    index_dir = base_path / _SEARCH_INDEX_PATH
    ix = open_dir(str(index_dir), schema)
    writer = ix.writer()
    data    = _get_frontmatter(afile)
    title   =  data.get("title") or afile.name.split(".")[0]
    path    = str(afile.relative_to(base_path))
    content = afile.read_text()
    writer.add_document(  title = title
                           , description = data.get("description", "")
                           , content = normalize_text(content)
                           , path = path
                          )
    writer.commit()

def index_delete_page(base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    afile = mwiki_page_file
    path    = str(afile.relative_to(base_path))
    index_dir = base_path / _SEARCH_INDEX_PATH
    ix = open_dir(str(index_dir))
    writer = ix.writer()
    writer.delete_by_term("path", path)
    writer.commit()


def index_markdown_files(base_path: pathlib.Path):
    markdown_file_list = base_path.rglob("*.md")
    index_dir = base_path / _SEARCH_INDEX_PATH
    if not index_dir.exists():
        index_dir.mkdir()
    ix = create_in(str(index_dir), schema)
    writer = ix.writer()
    for afile in markdown_file_list:
        print(" [TRACE] Indexing file " + str(afile))
        index_page_(writer, base_path, afile)
    writer.commit()
    print(" [TRACE] All markdown files indexed. Ok.")

_fileds = ["title", "description", "content"]

def search_text(base_path: pathlib.Path, query: str):
    "Return list of markdown files that matches the input query."
    index_dir = base_path / _SEARCH_INDEX_PATH
    ix = open_dir(str(index_dir))
    out = []
    with ix.searcher() as searcher:
        ##query_parser = QueryParser("content", ix.schema)
        query_parser = MultifieldParser(_fileds, schema = ix.schema, group = qparser.OrGroup)
        query_parser.add_plugin(qparser.FuzzyTermPlugin())
        _query = normalize_text(query)
        aquery = query_parser.parse(_query)
        results_ = searcher.search(aquery, limit = 20)
        results = list(results_)
        for r in results:
            path = r['path']
            p = base_path / path
            if p.exists():
                out.append(p)
        return out
        #for r in results:
            #title = r['title']
           # path = r['path']
            ##score = r['score']
            #print(f"Title: {title}, Path: {path} ")



