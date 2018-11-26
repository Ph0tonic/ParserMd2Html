import ply.lex as lex

reserved_words = (
	'@while',
	'@if',
	'@else if',
	'@else',
	'@mixin',
	'@import',
	'@include',
	'@extend'
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MUL_OP',
	'IDENTIFIER',
) + tuple(map(lambda s:s.upper(),reserved_words))

literals = '();=:{},'

def t_ADD_OP(t):
	r'[+-]'
	return t

def t_MUL_OP(t):
	r'[*/]'
	return t

def t_NUMBER(t): # 5px*10px
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t

t_UNIT = r'px|%|em|rem|pt|cm|mm|in|pt|pc|ex|ch|vw|vh|vmin|vmax'

t_STR_CSS = r'[\w#]+'

t_FUNC_CSSV(t) = ''

def t_IDENTIFIER(t):
	r'\$\w[A-Za-z-]+'
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
