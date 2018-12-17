import AST
from AST import addToClass
from functools import reduce

operations = {
	'+': lambda x,y : f"{x}{y}ADD\n",
    '-': lambda x,y : f"{x}{y}SUB\n",
    '*': lambda x,y : f"{x}{y}MUL\n",
    '/': lambda x,y : f"{x}{y}DIV\n",
}

vars = {}
lineSeperator = '\n'

if __name__ == "__main__" :
	from parser import parse
	import sys
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	compiledString = ast.compile()
	with open('compiled.css', 'w') as f :
		f.write(compiledString)
