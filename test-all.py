import os
import re
from recCompiler import compile_file


if __name__ == "__main__":
    p = re.compile('[\w\-\_]*\.(scss){1}')

    files = os.listdir("./data/")
    files = list(filter(lambda file: p.match(file) != None, files))

    for file_name in files:
        print("Compile "+file_name)
        compile_file("./data/"+file_name)
