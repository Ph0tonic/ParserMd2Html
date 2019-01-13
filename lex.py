#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Programe which allow a user to make a lexical analyse on a scss file

:param argv[1]: Scss file
:returns: Nothing but a file containing the lexems is generated in th same folder as the sources

Correct syntax:
python3 lex.py filename

Concrete example :
python3 lex.py "./data/_test-main.scss"

Requirements:
	Python3
	Ply

Authors:
	Lucas Bulloni - https://github.com/bull0n
	Bastien Wermeille - https://github.com/Ph0tonic

Date:
	13.01.2019

Code source of the project:
	https://github.com/Ph0tonic/SassCompiler
"""

import ply.lex as lex

reserved_words = {
	'while' : 'WHILE',
	'mixin' : 'MIXIN',
	'import' : 'IMPORT',
	'include' : 'INCLUDE',
	'extend' : 'EXTEND',
	'true' : 'TRUE',
	'false' : 'FALSE',
	'or' : 'OR',
	'and' : 'AND',
	'not' : 'NOT',
}

tokens = [
	'IF',
	'ELIF',
	'ELSE',
	'GT_OP',
	'FILE_PATH',
	'LGTE_OP',
	'COMP_OP',
	'ADD_OP',
	'MUL_OP',
	'NUMBER',
	'VARIABLE',
	'STRING_VALUE',
	'SELECTOR_EXTEND',
 ] + list(reserved_words.values())

literals = '@();:{},\''

def t_COMMENT(t):
	r'//.*'
	"""
	Detect single line comments

	:param t: token detected
	:return: nothing because this comment token is discarded
	"""
	pass # No return value. Token discarded

def t_IF(t):
	r'@if'
	"""
	Detect an if reserved keywords

	:param t: token detected
	:return: token
	"""
	return t

def t_ELIF(t):
	r'@else\ if'
	"""
	Detect an else if reserved keywords

	:param t: token detected
	:return: token
	"""
	return t

def t_ELSE(t):
	r'@else'
	"""
	Detect an else reserved keywords

	:param t: token detected
	:return: token
	"""
	return t

def t_COMP_OP(t):
	r'(==|!=)'
	"""
	Detect a comparator

	:param t: token detected
	:return: token
	"""
	return t

def t_LGTE_OP(t):
	r'(<=|<|>=)'
	"""
	Detect all integer comparators, except GreaterThan(>) 

	:param t: token detected
	:return: token
	"""
	return t

def t_GT_OP(t):
	r'>'
	"""
	Detect GreaterThan symbole

	:param t: token detected
	:return: token
	"""
	return t

def t_ADD_OP(t):
	r'[+-]'
	"""
	Detect Integer operator + and -

	:param t: token detected
	:return: token
	"""
	return t

def t_MUL_OP(t):
	r'[*/]'
	"""
	Detect Integer operator * and /

	:param t: token detected
	:return: token
	"""
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?(px|%|em|rem|pt|cm|mm|in|pt|pc|ex|ch|vw|vh|vmin|vmax)?'
	"""
	Detect Integer value with their unit

	:param t: token detected
	:return: token
	"""
	return t

def t_VARIABLE(t):
	r'\$\w[A-Za-z-]*'
	"""
	Detect variables (start with $)

	:param t: token detected
	:return: token
	"""
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_SELECTOR_EXTEND(t):
	r'%{1}[\w\-\_]*'
	"""
	Detect special extend keywords (start with %)

	:param t: token detected
	:return: token
	"""
	return t

def t_FILE_PATH(t):
	r'[\'\"]{1}[\w\_\-.]*[\'\"]{1}'
	"""
	Detect Filename

	:param t: token detected
	:return: token
	"""
	return t

def t_STRING_VALUE(t):
	r'[#\.]*[\w\-\_\[\]=]*[\w\]]{1}'
	"""
	Detect String value which are not poart of the reserved words

	:param t: token detected
	:return: token
	"""
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	"""
	Detect a new line

	:param t: token detected
	:return: token
	"""
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	"""
	Manage case when a token isn't detected

	:param t: token detected
	:return: token
	"""
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	
	filename = sys.argv[1]
	try:
		prog = open(filename).read()
	except FileNotFoundError:
		print(f"Error File not found {filename}")
		exit()

	lex.input(prog)

	result = ""
	while 1:
		tok = lex.token()
		if not tok: break
		result += "line %d: %s(%s)\n" % (tok.lineno, tok.type, tok.value)
	
	print(result)
	
	#Store lexem in file
	if result:
		import os

		name = os.path.splitext(sys.argv[1])[0] + '-lex.txt'
		with open(name, 'w') as f:
			f.writelines(result)
		print("wrote ast to", name)
	else:
		print("Lex returned no result!")
	
