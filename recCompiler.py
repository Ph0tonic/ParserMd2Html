#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Programe which allow a user to compile a scss file into a css file

:param argv[1]: Scss file
:returns: Nothing, but a css file is generated in the folder "generated" with the same name but the .css extension

Correct syntax:
python3 recCompiler.py filename

Concrete example :
python3 recCompiler.py "./data/_test-main.scss"

Requirements:
- Python3
- Ply
- Graphviz
- pydot
- yacc
- AST.py
- lex.py
- parser.py

Authors:
- Lucas Bulloni - https://github.com/bull0n
- Bastien Wermeille - https://github.com/Ph0tonic

Date:
	13.01.2019

Code source of the project:
- https://github.com/Ph0tonic/SassCompiler
"""

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
extends_rules = {}
mixins = {}
LINE_SEPARATOR = '\n'
current_path = ''

def compileListToString(list, separator = ''):
	compiled_string = separator.join([element.compile() for element in list])

	return compiled_string

@addToClass(AST.ValueNode)
def compile(self):
	# if the node can be compiled, compile it
	if isinstance(self.value, AST.NumberNode) or isinstance(self.value, AST.OpNode) or isinstance(self.value, AST.VariableNode):
		return self.value.compile()
	else:
		return str(self.value)

@addToClass(AST.NumberNode)
def compile(self):
	compiled_string = f'{self.value}{self.unit}'
	return compiled_string

@addToClass(AST.ValuesNode)
def compile(self):
	return compileListToString(self.children, ' ')

@addToClass(AST.RuleNode)
def compile(self):
	children = self.children

	return f'\t{children[0].compile()} : {children[1].compile()};\n'

@addToClass(AST.SelectorsNode)
def compile(self):
	return compileListToString(self.children, ' ')

@addToClass(AST.OpNode)
def execute(self):

	# the two values
	args = list(map(opToResultNode, self.children))

	# EXCEPTIONS HANDLING
	if len(args) > 1 and args[0].unit != args[1].unit and args[1].unit != '' and args[0].unit != '':
		raise Exception('unit is different')

	if not isinstance(args[0], AST.NumberNode) or len(args) > 1 and not isinstance(args[1], AST.NumberNode):
		raise Exception('Operation with a non-number')

	if len(args) > 1 and self.op == '/' and args[1].value == 0:
		raise Exception('Dividing by zero')

	if len(args) == 1:
		args.insert(0, AST.NumberNode(0))

	unit = ''

	# give the right unit
	if args[0].unit != '':
		unit = args[0].unit
	elif args[1].unit != '' :
		unit = args[1].unit

	value = reduce(operations[self.op], map(lambda t: t.value, args))

	return AST.NumberNode(value, unit)

@addToClass(AST.OpNode)
def compile(self):
	result = self.execute()
	return f'{result.value}{result.unit}'

@addToClass(AST.StatementNode)
def compile(self, selectors = ''):
	selector = self.children[0]
	selectorString = f'{selectors}{selector.compile()} '

	# preparation for the nested statement ode
	compiled_nested = ''
	compiled_content = ''
	compiled_string = ''

	# compile the statement and the nested statement in 2 different strings
	for child in self.children[1:]:
		if isinstance(child, AST.StatementNode):
			compiled_nested += f'{child.compile(selectorString)}'
		else:
			compiled_content += child.compile()

	# if there is no rule, only add nested statement
	if compiled_content == '':
		compiled_string = f'{compiled_nested}\n'
	else:
		compiled_string = f'{selectorString}  {{ \n{compiled_content}}}\n{compiled_nested}\n'

	return compiled_string

@addToClass(AST.ProgramNode)
def compile(self):
	return compileListToString(self.children, '')


@addToClass(AST.AssignNode)
def compile(self):
	data = self.children[1]

	# check if we can reduce the hierarchy of the nodes
	if isinstance(data, AST.ValuesNode) and len(data.children) == 1:
		data = data.children[0].value
	if isinstance(data, AST.OpNode):
		data = data.execute()

	vars[self.children[0].value] = data
	return ""

@addToClass(AST.VariableNode)
def compile(self):
	try:
		if isinstance(vars[self.value], AST.Node):
			return vars[self.value].compile()
		else:
			return vars[self.value]
	except KeyError:
		raise Exception(f'Variable {self.value} doesn\'t exist') from None

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
	saved_vars_state = vars # save the vars to restore it when exiting the mixin

	# get the mixin if it exists
	try:
		mixin = mixins[self.identifier]
	except KeyError:
		raise Exception(f'Variable {self.value} doesn\'t exist') from None

	# if there is some parameters handle it
	if mixin.parameters != None:
		# merge the vars of the file + the parameter of the mixin
		mapped_identifier = map(lambda val: val.value, mixin.parameters.children)
		list_identifier = deleteComaFromList(mapped_identifier)

		mapped_value = map(lambda val: val.compile(), self.children[0].children)
		listValue = deleteComaFromList(mapped_value)

		# if parameters aren't good, too many, not enough
		if len(list_identifier) != len(listValue):
			raise Exception(f'parameters for mixin {self.identifier} not valid')

		mixin_vars = dict(zip(list_identifier, listValue))
		vars = {**vars, **mixin_vars}


	compiled_mixin = mixin.execute()
	vars = saved_vars_state

	return compiled_mixin

@addToClass(AST.IfNode)
def compile(self):
	if self.children[0].compile():
		return self.children[1].compile()
	else:
		# check if a else statement is there
		if len(self.children) > 2:
			return self.children[2].compile()

		return ''

@addToClass(AST.BoolNode)
def compile(self):
	return self.value

@addToClass(AST.BoolOpNode)
def compile(self):
	# the two values
	args = [c.compile() for c in self.children]

	if len(args) == 1:
		print(args[0])
		return not args[0]

	value = reduce(operations[self.op], args)

	return AST.BoolNode(value).compile()

@addToClass(AST.WhileNode)
def compile(self):
	compiled_string = ''
	i = 0

	while self.children[0].compile():
		compiled_string += self.children[1].compile()

	return compiled_string

@addToClass(AST.ImportNode)
def compile(self):
	return compile_file(f'{current_path}{os.sep}{self.value}.scss')

@addToClass(AST.ExtendNodeDefine)
def compile(self):
	extends_rules[self.identifier] = self.children[0].compile()
	return ''

@addToClass(AST.ExtendNode)
def compile(self):
	try:
		return extends_rules[self.identifier]
	except KeyError:
		raise Exception(f'extend {self.identifier} does not exist') from None

def deleteComaFromList(list_to_filter):
	'''
	delete all string coma from a list
	'''
	return list(filter(lambda val: val != ',', list_to_filter))

def getFileName(path):
	'''
	get the name of the file
	'''
	return path.split(os.sep)[-1].split('.')[0]

def compile(string_to_compile):
	'''
	main function for compilation
	'''
	ast = parse(string_to_compile)
	compiled_string = ast.compile()

	return compiled_string

def compile_file(filename):
	'''
	Function allowing to compile a file
	'''
	prog = open(filename).read()
	return compile(prog)

def write_into_compiled_file(filename, str_to_write):
	'''
	write a string into a File
	'''

	# check the string isn't empty
	if str == '':
		return

	# if folder doesn't exist, create it
	try:
		os.mkdir('./compiled/')
	except FileExistsError:
		pass

	path_compiled = f'compiled/{getFileName(filename)}.css'

	try:
		with open(path_compiled, 'w') as f :
			f.write(str_to_write)
	except FileNotFoundError:
		raise Exception(f'File {path_compiled} doesn\'t exist')

def compile_write(filename):
	'''
	compile a file and write it into his corresponding file
	'''
	global current_path
	current_path = os.sep.join(filename.split(os.sep)[:-1])
	write_into_compiled_file(filename, compile_file(filename))

def opToResultNode(value):
	'''
	execute an operation to transform it into his result node
	'''
	if isinstance(value, AST.OpNode):
		return value.execute()
	elif isinstance(value, AST.VariableNode):
		return vars[value.value]
	else:
		return value

if __name__ == "__main__" :
	import sys
	try:
		compile_write(sys.argv[1])
	except FileNotFoundError:
		print(f"Error File not found {sys.argv[1]}")
