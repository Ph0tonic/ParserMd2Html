import AST
from AST import addToClass
from functools import reduce

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
	'>' : lambda x,y: x>y,
	'<' : lambda x,y: x<y,
	'>=' : lambda x,y: x>=y,
	'<=' : lambda x,y: x<=y,
}

vars = {}
lineSeperator = '\n'

def compileListToString(list, separator):
	compiledString = separator.join([element.compile() for element in list])

	return compiledString

@addToClass(AST.ValueNode)
def compile(self):
	return str(self.value)

# @addToClass(AST.NumberNode)
# def execute(self):
#     return (self.value, self.unit)

@addToClass(AST.NumberNode)
def compile(self):
	return f'{self.value}{self.unit}'

@addToClass(AST.ValuesNode)
def compile(self):
	return compileListToString(self.children, ' ')

@addToClass(AST.RuleNode)
def compile(self):
	children = self.children

	return f'{children[0].compile()} : {children[1].compile()};\n'

@addToClass(AST.SelectorsNode)
def compile(self):
	return compileListToString(self.children, ' ')

@addToClass(AST.OpNode)
def execute(self):
	args = [c.execute() for c in self.children]

	if args[0][1] != args[1][1] and args[1][1] != '' and args[0][1] != '':
		raise Exception('unit is different')

	if len(args) == 1:
		args.insert(0,0)

	unit = ''

	if args[0][1] != '':
		unit = args[0][1]
	elif args[1][1] != '' :
		unit = args[1][1]

	value = reduce(operations[self.op], map(lambda t: t[0], args))

	return AST.NumberNode(value, unit).execute()

@addToClass(AST.OpNode)
def compile(self):
	result = self.execute()
	return f'{result[0]}{result[1]}'

@addToClass(AST.StatementNode)
def compile(self, selectors = ''):
	selector = self.children[0]
	selectorString = f"{selectors}{selector.compile()} "

	compiledNested = ""
	compiledContent = ""
	compiledString = ""

	for child in self.children[1:]:
		if isinstance(child, AST.StatementNode):
			compiledNested += f"{child.compile(selectorString)}"
		else:
			compiledContent += child.compile()

	if compiledContent == "":
		compiledString = f"{compiledNested}\n"
	else:
		compiledString = f"{selectorString}  {{ \n{compiledContent}}}\n{compiledNested}\n"

	return compiledString

@addToClass(AST.ProgramNode)
def compile(self):
	return compileListToString(self.children, '\n')

@addToClass(AST.VariableNode)
def compile(self):
	return ""

@addToClass(AST.AssignNode)
def compile(self):
	vars[self.children[0].value] = self.children[1].compile()
	return ""

@addToClass(AST.VariableNode)
def compile(self):
	try:
		return vars[self.value]
	except KeyError:
		raise Exception(f"Variable {self.value} doesn't exist") from None

@addToClass(AST.MixinNode)
def compile(self):
	return ""

@addToClass(AST.IncludeNode)
def compile(self):
	return ""

@addToClass(AST.IfNode)
def compile(self):
	return ""

@addToClass(AST.BoolNode)
def compile(self):
	return ""

@addToClass(AST.BoolOpNode)
def compile(self):
	return ""

@addToClass(AST.WhileNode)
def compile(self):
	return ""

def getFileName(path):
	return path.split("/")[-1].split('.')[0]

if __name__ == "__main__" :
	from parser import parse
	import sys
	prog = open(sys.argv[1]).read()
	ast = parse(prog)
	compiledString = ast.compile()
	pathCompiled = f'compiled/{getFileName(sys.argv[1])}.css'

	with open(pathCompiled, 'w') as f :
		f.write(compiledString)
