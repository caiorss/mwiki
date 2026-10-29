---
title:       Technical Details
label:       
description: Tehcnical details about MWiki and comparison to other software and wiki engines.
keywords:    
abbreviations:
  STEM:  Science, Technology, Engineering, and Mathematics
  CSS:   Cascade Style Sheet
  HTML5: Hypertext Markup Language (Version 5)
  ORM:   Object Relational Mapping
---

## Overview

MWiki is a [wiki](https://en.wikipedia.org/wiki/Wiki) engine and note taking web application software geared towards STEM and designed for scientific and technical communication. This wiki engine software has semantic-rich lightweight markup language inspired by MyST markdown, Obsidian markdown, and Mediawiki engine markup language. The application also works as a static websiste generator, that can export MWiki notes or pages to a static website or self-contained html files for offline reading, similar to PDF files.
## Inspiration

MWiki was inspired by many other Wiki engines and applications, inclunding:

[Mediawiki](https://en.wikipedia.org/wiki/MediaWiki) (PHP)
  : PHP Wiki engine used by Wikipedia. Although Mediawiki is mature, this engine is hard to self-host and does not uses markdown as markup language. The style of MWiki URLs was heavily inspired by Mediawiki and the schema of Wikipedia URLs.

[Dokuwiki](https://en.wikipedia.org/wiki/DokuWiki) (PHP)
  : File-based wiki, but does not uses markdown as its markup language. Dokuwiki also requires many plugins to achieve to obtain the same number of features that MWiki has by default.  

[MoinMoin](https://en.wikipedia.org/wiki/MoinMoin) (Python 2)
  : File-based wiki engine. Pages are stored as a single file instead of being stored in a database. MoinMoin also does not use markdown as its markup language. Other issue is the usage of Python 2, which makes the code hard to modify and the lack of support for Python 2.

[Obsidian](https://en.wikipedia.org/wiki/Obsidian_(software)) 
  : Desktop note taking application and personal wiki, which uses markdown. As Obsidian is a desktop application, it is harder to access notes from other devices due to the need for file synchronization. MWiki borrowed many concepts from Obsidian, such as the syntax for embedding files and for internal hyperlinks. As a result, since MWiki syntax is a superset of Obsidian syntax, it is possible to export existing Obsidian pages to static website or as wiki repository.  
  
MyST Markdown (Jupyter Book project)
  : Markdown language from Jupyter book project. MWiki uses the same parser as Jupyter book, which is a static website generator, but not a wiki.
## Technologies Used

Backend (Main Web Server)
  : Python [flask](https://flask.palletsprojects.com/) web server with SQLite as database^[Note that that all wiki pages or notes are text files, while the database is only used for administrative tasks, including session storage], however it is possible to use any other database compatible with SQL Alchemy ORM.

Backend (Reverse proxy and static files server)
  : Caddy web server

Frontend
  : HTML5 + CSS + hand-rolled JavaScript without any framework, such as React, VueJS, NextJS and so on.
 
ORM (Object Relational Mappping)
  : SQL [Alchemy](https://www.sqlalchemy.org/)

Search Engine
  : [whoosh](https://github.com/mchaput/whoosh)^[2011 - Matt Chaput] - Pure Python search engine, which makes MWiki easier to self-host.
