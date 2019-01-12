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
