#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Programe which use our compiler and compile all scss file located in the folder data, the final generated files are in the folder "generated".

:returns: Nothing, but all css file are generated in the folder "generated" with the same name but the .css extension

Correct syntax:
python3 test-all.py filename

Concrete example :
python3 test-all.py "./data/_test-main.scss"

Requirements:
- Python3
- Ply
- Graphviz
- pydot
- yacc
- AST.py
- lex.py
- recCompiler.py

Authors:
- Lucas Bulloni - https://github.com/bull0n
- Bastien Wermeille - https://github.com/Ph0tonic

Code source of the project:
- https://github.com/Ph0tonic/SassCompiler
"""

import os
import re
from recCompiler import compile_file

FOLDER = "./data/"

if __name__ == "__main__":
    p = re.compile('[\w\-\_]*\.(scss){1}')

    files = os.listdir(FOLDER)
    files = list(filter(lambda file: p.match(file) != None, files))

    for file_name in files:
        print("Compile "+file_name)
        compile_file(FOLDER+file_name)
