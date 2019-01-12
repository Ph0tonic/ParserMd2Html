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

def t_IF(t):
	r'@if'
	return t

def t_ELIF(t):
	r'@else\ if'
	return t

def t_ELSE(t):
	r'@else'
	return t

def t_COMMENT(t):
	r'//.*'
	pass # No return value. Token discarded

def t_COMP_OP(t):
	r'(==|!=)'
	return t

def t_LGTE_OP(t):
	r'(<=|<|>=)'
	return t

def t_GT_OP(t):
	r'>'
	return t

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'
	return t

def t_NUMBER(t):
	r'\d+(\.\d+)?(px|%|em|rem|pt|cm|mm|in|pt|pc|ex|ch|vw|vh|vmin|vmax)?'
	return t

def t_VARIABLE(t):
	r'\$\w[A-Za-z-]*'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_SELECTOR_EXTEND(t):
	r'%{1}[\w\-\_]*'
	return t

def t_FILE_PATH(t):
	r'[\'\"]{1}[\w\_\-.]*[\'\"]{1}'
	return t

def t_STRING_VALUE(t):
	r'[#\.]*[\w\-\_\[\]=]*[\w\]]{1}'
	if t.value in reserved_words:
		t.type = t.value.upper()
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
