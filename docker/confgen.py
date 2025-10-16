#!/usr/bin/env -S uv run --script 
#-*- coding:utf-8 -*-
# /// script
# requires-python = ">=3.8"
# dependencies = [
#       "jinja2"
#     , "dotenv"
# ]
# [tool.uv]
# exclude-newer = "2025-04-01T00:00:00Z"
# ///


# Script for generating configuration files with 
# if-else statement using Jinja2 Python template engine

import os
import sys 
import pathlib
import jinja2

def main():
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: ")
        print(f"  $ {argv[0]}  <template-file>")
        exit(1)
    file = pathlib.Path(argv[1])
    if not file.exists():
        print(f"ERROR: Template file {file} not found.")
        exit(1)
    src = file.read_text()
    env = os.environ
    tpl = jinja2.Template(src)
    out = tpl.render(env)
    print(out)
    exit(0)

if __name__ == "__main__":
    main()