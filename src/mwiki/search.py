import re 
from typing import List, Dict 
import os.path


_ENGLISH_STOP_WORDS = [ 
                "and", "or", "any", "of", "some"
             , "in", "at", "on", "off", "our"
             , "your", "we", "yours", "yourself"
             , "his", "he", "himself", "her", "hers"
             , "it", "its", "itself", "they", "them"
             , "what", "which", "whom", "that", "these"
             , "those", "a", "an" 
             ]

## Database for normalization of English words  
_NORMALIZATION_DATABASE = {
       "scripts":  "script"
    ,  "sources":  "source"
     , "networks": "network"
     , "networking": "network"
     , "identifiers": "identifiers"
     , "objects": "object"
     , "countries":  "country"
     , "people":  "person"
     , "men":  "man"
     , "women": "woman"
     , "guys":   "guy"
     , "girls":  "girl"
     , "gurls":  "girl"
     , "children": "child"
     , "leaves": "leaf"
     , "choices": "choice"
     , "ports":  "port"
     , "gateway": "gate"
     , "mathematics": "math"
     , "arrays": "array"
     , "matrices": "matrix"
     , "vectors":  "vector"
     , "formulas": "formula"
     , "formulae": "formula"
     , "engines":  "engine"
     , "systems":  "system"
     , "services":  "service"
     , "projects": "project"
     , "packages": "package"
     , "features": "feature"
     , "functions": "function"
     , "methods":   "method"
     , "protocols":  "protocol"
     , "classes":      "class"
     , "dependencies": "dependency"
     , "IDs":          "id"
     , "ids":          "id"
     , "APIs":         "api"
     , "apps":         "app"
     , "jobs":         "job"
     , "tasks":        "task"
     , "listing":       "list"
     ,  "lists":        "list"
     , "debugging":    "debug"
     , "logging":      "log"
     , "libraries":    "library"
     , "libs":         "library"
     , "lib":          "library"
     , "diseases":     "disease"
     , "employees":    "employee"
     , "universities": "university"
     , "schools":      "school"
     , "U.K.":         "UK"
     , "U.K":          "UK"
     , "U.S.":         "US"
     , "U.S":          "US"
}

def normalize_text(text: str) -> str:
    """Remove accents, such as ú or ç for making searching easier."""
    out = (text 
                .replace("ã", "a")
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
            )
    return out

def normalize_words(text: str) -> str:
    out = text 
    for word in _NORMALIZATION_DATABASE.keys():
        out = re.sub(r"\b%s\b" % word, _NORMALIZATION_DATABASE[word], out)
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
            line_ = normalize_words(line_) if flag_normalize_words else line_
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
                    cond1 = re.findall(r"\b%s\b" % q, line_) != []
                    cond2 = re.findall(r"\b%s\b" % q, basename) != []
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
