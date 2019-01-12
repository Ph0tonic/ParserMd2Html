import AST
from AST import addToClass
from parser import parse

from functools import reduce
import os

operations = {
	'+' : lambda x,y: x+y,
	'-' : lambda x,y: x-y,
	'*' : lambda x,y: x*y,
	'/' : lambda x,y: x/y,
	'>' : lambda x,y: x>y,
	'<' : lambda x,y: x<y,
	'>=' : lambda x,y: x>=y,
	'<=' : lambda x,y: x<=y,
	'==' : lambda x,y: x==y,
	'!=' : lambda x,y: x!=y,
	'or' : lambda x,y: x|y,
	 'and' : lambda x,y: x&y
	}

vars = {}
extendsRules = {}
mixins = {}
lineSeperator = '\n'

def compileListToString(list, separator = ''):
	compiledString = separator.join([element.compile() for element in list])

	return compiledString

@addToClass(AST.ValueNode)
def compile(self):
	if isinstance(self.value, AST.NumberNode):
		return self.value.compile()
	elif isinstance(self.value, AST.OpNode):
		return self.value.compile()
	elif isinstance(self.value, AST.VariableNode):
		return self.value.compile()
	else:
		return str(self.value)

@addToClass(AST.NumberNode)
def compile(self):
	compiledStr = f'{self.value}{self.unit}'
	return compiledStr

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

	def opToNumber(value):
		if isinstance(value, AST.OpNode):
			return value.execute()
		else:
			return value

	args = list(map(opToNumber, self.children))

	if len(args) > 1 and args[0].unit != args[1].unit and args[1].unit != '' and args[0].unit != '':
		raise Exception('unit is different')

	if len(args) == 1:
		args.insert(0,0)

	unit = ''

	if args[0].unit != '':
		unit = args[0].unit
	elif args[1][1] != '' :
		unit = args[1].unit

	value = reduce(operations[self.op], map(lambda t: t[0], args))

	return AST.NumberNode(value, unit)

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
	return compileListToString(self.children, '')


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

@addToClass(AST.VariableNode)
def execute(self):
	return self.compile()

@addToClass(AST.MixinNode)
def compile(self):
	mixins[self.identifier] = self
	return ""

@addToClass(AST.MixinNode)
def execute(self):
	return compileListToString(self.children)

@addToClass(AST.IncludeNode)
def compile(self):
	global vars
	savedVarsState = vars

	try:
		mixin = mixins[self.identifier]
	except KeyError:
		raise Exception(f"Variable {self.value} doesn't exist") from None

	mappedIdentifier = map(lambda val: val.value, mixin.parameters.children)
	listIdentifier = deleteComaFromList(mappedIdentifier)


	mappedValue = map(lambda val: val.compile(), self.children[0].children)
	listValue = deleteComaFromList(mappedValue)

	if len(listIdentifier) != len(listValue):
		raise Exception(f"parameters for mixin {self.identifier} not valid")

	mixinVars = dict(zip(listIdentifier, listValue))
	vars = {**vars, **mixinVars}

	compiledMixin = mixin.execute()
	vars = savedVarsState

	return compiledMixin

@addToClass(AST.IfNode)
def compile(self):
	if self.children[0].compile():
		return self.children[1].compile()
	else:
		return ""

@addToClass(AST.BoolNode)
def compile(self):
	return self.value

@addToClass(AST.BoolOpNode)
def compile(self):
	args = [c.compile() for c in self.children]

	if len(args) == 1:
		return not args

	value = reduce(operations[self.op], args)

	return AST.BoolNode(value).compile()

@addToClass(AST.WhileNode)
def compile(self):
	compiledStr = ""

	while self.children[0].compile():
		compiledStr += self.children[1].compile()

	return compiledStr

@addToClass(AST.ImportNode)
def compile(self):
	prog = open(f"data/{self.value}.scss").read()

	return compile(prog)

@addToClass(AST.ExtendNodeDefine)
def compile(self):
	extendsRules[self.identifier] = self.children[0].compile()
	return ""

@addToClass(AST.ExtendNode)
def compile(self):
	try:
		return extendsRules[self.identifier]
	except KeyError:
		raise Exception(f"extend {self.identifier} does not exist") from None

def deleteComaFromList(listToFilter):
	return list(filter(lambda val: val != ",", listToFilter))

def getFileName(path):
	return path.split("/")[-1].split('.')[0]

def compile(stringToCompile):
	ast = parse(stringToCompile)
	compiledString = ast.compile()

	return compiledString


if __name__ == "__main__" :
	import sys
	prog = open(sys.argv[1]).read()

	compiledString = compile(prog)
	pathCompiled = f'compiled/{getFileName(sys.argv[1])}.css'

	with open(pathCompiled, 'w') as f :
		f.write(compiledString)
