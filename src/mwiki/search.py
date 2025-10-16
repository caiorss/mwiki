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
    """Remove accents, such as ú or ç for making searching easier.

    Example: The word 'Citroën' (French Car brand) is stored in
    the search index database as 'Citroen' instead of 'Citroën'
    due to be easier to write "Citroen" with an English keyboard layout
    or any non french keyboard layout. Therefore, searching for
    'Citroën' or 'Citroen' yields the same search results.

    See:
    + https://en.wikipedia.org/wiki/Diacritic
    + https://en.wikipedia.org/wiki/Spanish_orthography
    + https://en.wikipedia.org/wiki/Portuguese_orthography
    + https://portuguesepedia.com/portuguese-alphabet

    """
    # Turn the whole text to lower case
    out = text.lower()
    # Normalize escaped characters
    out = out.replace(r"\.", ".") \
             .replace(r"\:", ":")
    # Those accents or diactricts are common in
    # Spanish, French and Portuguese
    out = (out
                .replace("ñ", "n") # Spanish letter
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
                ## German Umlaut
                .replace("ü", "u")
                .replace("ö", "o")
                .replace("ß", "ss"))
    # Normalize letters, diactricts and Ligatures of old English and old Norse latin alphabet to Modern English alphabet.
    #
    # See:
    # + https://en.wikipedia.org/wiki/Old_English_Latin_alphabet
    # + https://en.wikipedia.org/wiki/Old_Norse_orthography
    # + https://en.wikipedia.org/wiki/Old_Norse#Old_Icelandic
    out = (out
            .replace("Æ", "ae")
            .replace("æ", "ae")
            .replace("Ƿ", "p")
            .replace("Ð", "D")
            .replace("ð", "d")
            .replace("ø", "o")
            .replace("ǫ", "o")
            .replace("þ", "th")
            .replace("ý", "y")
            .replace("í", "i")
            .replace("ö", "o")
            .replace("ſ", "s")
            .replace("ꝩ", "v")
            .replace("n͛", "n")
            .replace("h̅", "h")
            .replace("ꝛ", "r")
            # DO NOT Confuse this old norse letter with the greek letter tau.
            .replace("ꞇ", "t")
           )
    # Normalize Sweedish alphabet and its diactricts to english alphabet
    #
    # See:
    # + https://en.wikipedia.org/wiki/Swedish_alphabet
    out = (out
           .replace("å", "a")
           .replace("Å", "a")
           .replace("Ä", "a")
           .replace("Ö", "o")
           .replace("ö", "o")
           )
    # Normalize Ligatures and Diactricts of the French Latin Alphabet
    # to letter sof the English Alphabet.
    #
    # See:
    # + https://en.wikipedia.org/wiki/French_orthography
    # + https://en.wikipedia.org/wiki/Circumflex_in_French
    out = (out
            .replace("æ", "ae")
            .replace("œ", "oe")
            .replace("Æ", "AE")
            .replace("Œ", "OE")
            .replace("ç", "c")
            .replace("à", "a")
            .replace("â", "a")
            .replace("î", "i")
            .replace("ï", "i")
            .replace("û", "u")
            .replace("ô", "o")
            .replace("ê", "e")
            .replace("è", "e")
            .replace("ë", "e")
            .replace("ÿ", "y")
            .replace("É", "E")

           )
    # Normalize Vietnamese latin Alphabet to English Alphabet.
    # Note the Vietnamese latin Alphabet is based on the French Latin alphabet.
    #
    # See:
    # +  https://en.wikipedia.org/wiki/Vietnamese_alphabet
    # + https://en.wikipedia.org/wiki/Vietnamese_punctuation
    #
    # Example: The vietnamese word "người" is stored in the search index
    # database as "nguoi".
    out = (out
            .replace("à", "a")
            .replace("á", "a")
            .replace("ă", "a")
            .replace("â", "a")
            .replace("ả", "a")
            .replace("ã", "a")
            .replace("ằ", "a")
            .replace("ằ", "a")
            .replace("ặ", "a")
            .replace("ạ", "a")
            .replace("ắ", "a")
            .replace("ê", "e")
            .replace("ế", "e")
            .replace("ệ", "e")
            .replace("ô", "o")
            .replace("ơ", "o")
            .replace("ờ", "o")
            .replace("ò", "o")
            .replace("ổ", "o")
            .replace("ư", "u")
            .replace("ủ", "u")
            .replace("ữ", "u")
            .replace("đ", "d")
            .replace("ý", "y")
            .replace("ỳ", "y")
            .replace("ỹ", "y")
            .replace("ỷ", "y")
            .replace("ỵ", "y")
            .replace("ị", "i")
            .replace("ì", "i")
            .replace("ĩ", "i")
           )
    # Normalize Danish and Norwegian alphabets to English Alphabet
    # See:
    #  + https://en.wikipedia.org/wiki/Danish_and_Norwegian_alphabet
    out = (out
            .replace("Å", "A")
            .replace("å", "a")
            .replace("Æ", "AE")
            .replace("æ", "ae")
            .replace("Ø", "O")
            .replace("ø", "o"))
    # Normalize letters of Polish Latin Alphabet to
    # Letters of English Alphabet in order to make the
    # search more comprehensive. This normalization allows
    # searching polish text or Polish names without typing
    # any letter of Polish alphabet using only letters of
    # English alphabet without any diactrict or special punctuation marks.
    # See:
    #  + https://en.wikipedia.org/wiki/Polish_alphabet
    #  + https://simple.wikipedia.org/wiki/Polish_alphabet
    out = (out
                .replace("ą", "a")
                .replace("ć", "c")
                .replace("ę", "e")
                .replace("ó", "o")
                .replace("ź", "z")
                .replace("ż", "z")
                .replace("ł", "l")
                .replace("ń", "n")
                .replace("ś", "s")
                .replace("Ą", "A")
                .replace("Ć", "C")
                .replace("Ę", "E")
                .replace("Ł", "L")
                .replace("Ń", "N")
                .replace("Ó", "O")
                .replace("Ś", "S")
                .replace("Ź", "Z"))
    # Normalization of Turkish Latin alphabet to English Latin Alphabet
    # See:
    #  + https://en.wikipedia.org/wiki/Turkish_alphabet
    #  + https://en.wikipedia.org/wiki/Common_Turkic_alphabet
    out = (out
                .replace("ç", "c")
                .replace("ğ", "g")
                .replace("i", "i")
                .replace("ı", "i")
                .replace("ö", "o")
                .replace("ü", "u")
                .replace("I", "I")
                .replace("Ç", "C")
                .replace("Ğ", "G")
                .replace("Ö", "O")
                .replace("Ü", "U")
                .replace("Ū", "U")
                .replace("ū", "u")
                .replace("ş", "s")
                .replace("Ş", "S")
                .replace("Ə", "E")
                .replace("ə", "e")
                .replace("Ñ", "N")
                .replace("ñ", "n"))
    # Normalize letters of Serbo-Croatian Alphabet to English Latin Alphabet
    # See:
    #  + https://en.wikipedia.org/wiki/Gaj%27s_Latin_alphabet
    out = (out
                .replace("č", "c")
                .replace("ć", "c")
                .replace("Č", "C")
                .replace("Ć", "C")
                .replace("ž", "Z")
                .replace("ž", "Z")
                .replace("Đ", "D")
                .replace("đ", "d")
                .replace("š", "s")
                .replace("Š", "S")
           )
    # Normalize letters of the Czesh Alphabet to English Latin Alphabet
    # See:
    # - https://en.wikipedia.org/wiki/Czech_orthography
    out = (out
                .replace("á", "a")
                .replace("č", "c")
                .replace("ď", "d")
                .replace("é", "e")
                .replace("ě", "e")
                .replace("ň", "n")
                .replace("ř", "r")
                .replace("š", "s")
                .replace("ť", "t")
                .replace("ú", "u")
                .replace("ů", "u")
                .replace("ý", "y")
                .replace("ž", "z")
                .replace("í", "i")
           )
    # Normalize Maltese Alphabet letters to English alphabet.
    # See:
    # - https://en.wikipedia.org/wiki/Maltese_alphabet
    out = (out
                .replace("ċ", "c")
                .replace("č", "c")
                .replace("ġ", "g")
                .replace("ħ", "h")
                .replace("ż", "z")
           )
    # Normalize Romanian and Istro-Romanian alphabets letters to English alphabet
    # See:
    # - https://en.wikipedia.org/wiki/Romanian_alphabet
    # - https://en.wikipedia.org/wiki/Istro-Romanian_alphabet
    out = (out
            .replace("ș", "s")
            .replace("î", "i")
            .replace("â", "a")
            .replace("å", "a")
            .replace("ă", "a")
            .replace("ț", "t")
            .replace("ĭ", "i")
            .replace("ğ", "g")
            .replace("č", "c")
            .replace("ń", "n")
            .replace("ǔ", "u")
            .replace("ę", "e")
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

## storage = RamStorage()
## index = storage.create_index(schema)


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
    print(" [TRACE] Updating search index for document " + str(afile))
    writer.update_document(  title = title
                        , description = data.get("description", "")
                        , content = normalize_text(content)
                        , path = path
                        )


def update_index_page(base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    """Update a search index metadata of MWiki markdown page file."""
    index_dir = base_path / _SEARCH_INDEX_PATH
    ## breakpoint()
    ix = open_dir(str(index_dir))
    writer = ix.writer()
    update_index_page_(writer, base_path, mwiki_page_file)
    writer.commit()

def add_index_page(base_path: pathlib.Path, mwiki_page_file: pathlib.Path):
    """Add MWiki page to search index."""
    afile = mwiki_page_file
    index_dir = base_path / _SEARCH_INDEX_PATH
    ix = open_dir(str(index_dir))
    writer = ix.writer()
    index_page_(writer, base_path, afile)
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
        data_dir = base_path / ".data"
        data_dir.mkdir(exist_ok = True)
        index_dir.mkdir(exist_ok = True)
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



