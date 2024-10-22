#!/usr/bin/env python 
"""Script for starting the server without any command line arguments. 

This file is a loader script for starting the server without any command
line argument in order to make it easier to run the VSCode debugger
or any other GUI/IDE based debugger.

Abbreviations:
 
   + GUI - Graphical User Interface 
   + IDE - Integrated Development Environment

"""

import mwiki.server 


HOST = "0.0.0.0"
PORT = 8000

mwiki.server.run_app_server(  host = HOST
                             , port = PORT
                             , debug = True
                             , login = None
                             , wikipath = "pages"
                             , random_ssl = False 
                             )