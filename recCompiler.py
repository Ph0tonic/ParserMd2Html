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

@addToClass(AST.ValueNode)
def compile(self):
    return str(self.value)

@addToClass(AST.NumberNode)
def compile(self):
    return str(self.value)

@addToClass(AST.SelectorNode)
def compile(self):
    return str(self.selectorStr)

@addToClass(AST.ValuesNode)
def compile(self):
    compiledString = " ".join([child.compile() for child in self.children])

    return compiledString

@addToClass(AST.RuleNode)
def compile(self):
    children = self.children

    return f'{children[0]} : {children[1].compile()}'


if __name__ == "__main__" :
	from parser import parse
	import sys
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	compiledString = ast.compile()
	with open('compiled.css', 'w') as f :
		f.write(compiledString)
