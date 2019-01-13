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
from recCompiler import compile_write

FOLDER = "./tests/"

if __name__ == "__main__":
    p = re.compile('[\w\-\_]*\.(scss){1}')

    files = os.listdir(FOLDER)
    files = list(filter(lambda file: p.match(file) != None, files))
    nb_test = len(files)
    nb_error = 0
    for file_name in files:
        print(f"Start compiling {file_name}")
        try:
            compile_write(FOLDER+file_name)
        except:
            print(f"\t ! ERROR while compiling {file_name} !")
            nb_error += 1
    
    print(f"\nCompiling ended, {nb_test-nb_error}/{nb_test} tests sucessfuls")
