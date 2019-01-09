import ply.yacc as yacc

from lex import tokens
import AST

import re

extend_statement = {}

def p_programme_recursive(p):
    '''
    programme : programme statement
            |   statement
    '''
    pass

def p_statement(p):
    '''
    statement : STRING_VALUE section
            |   list_string section
            |   list_selector section
    '''
    #TODO Add code here
    pass

def p_section(p):
    '''
    section : '{' programme '}'
            | '{' '}'
    '''
    pass

def p_rule(p):
    '''
    statement : STRING_VALUE attribution
    '''
    pass

def p_assign(p):
    '''
    statement : variable attribution
    '''
    pass

def p_attribution(p):
    '''
    attribution : ':' STRING_VALUE ';'
                | ':' list_string ';'
                | ':' list_value ';'
                | ':' variable ';'
    '''
    pass

def p_mixin(p):
    '''
    statement : '@' MIXIN STRING_VALUE '(' list_variable ')' section
            |   '@' MIXIN STRING_VALUE '(' variable ')' section
            |   '@' MIXIN STRING_VALUE section
    '''
    pass

def p_include(p):
    '''
    statement : '@' INCLUDE STRING_VALUE '(' list_value ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' list_string ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' STRING_VALUE ')' ';'
            |   '@' INCLUDE STRING_VALUE ';'
    '''
    pass

def p_if(p):
    '''
    statement : '@' IF '(' expression ')' section
            |   '@' IF '(' expression ')' section '@' ELSE
            |   '@' INCLUDE STRING_VALUE '(' STRING_VALUE ')' ';'
            |   '@' INCLUDE STRING_VALUE ';'
    '''
    pass

def p_else(p):
    '''
    else_section : '@' ELSE section
                |  '@' ELIF '(' expression ')' section
    '''
    pass

def p_list_variables(p):
    '''
    list_variable : list_variable ',' variable
                |   variable ',' variable
    '''
    pass

def p_list_value_recursive(p):
    '''
    list_value : list_value STRING_VALUE
            |    list_value expression
            |    STRING_VALUE list_value
            |    list_string list_value %prec STRING_VALUE
    '''
    pass

def p_list_value(p):
    '''
    list_value : expression
    '''
    pass

def p_list_string(p):
    '''
    list_string : STRING_VALUE STRING_VALUE
                | list_string STRING_VALUE
    '''
    pass

def p_expression_operation(p):
    '''
    expression : expression ADD_OP expression
            |    expression MUL_OP expression
            |    expression ADD_OP variable
            |    expression MUL_OP variable
            |    variable ADD_OP expression
            |    variable MUL_OP expression
            |    variable ADD_OP variable
            |    variable MUL_OP variable
    '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression(p):
    '''
    expression : NUMBER
    '''
    prog = re.compile(r'(\d*)(\D*)')
    result = prog.match(p[1])
    groups = result.groups()

    typeNumber = int

    if groups[0].find('.') > -1:
        typeNumber = float

    if groups[1] == '':
        p[0] = AST.NumberNode(typeNumber(groups[0]))
    else:
        p[0] = AST.NumberNode(typeNumber(groups[0]), groups[1])

def p_variable(p):
    '''
    variable : VARIABLE
    '''
    p[0] = AST.VariableNode(p[1])

def p_selector_recursive(p):
    '''
    list_selector : list_selector SELECTOR
                |   list_selector SEPARATOR
                |   list_selector STRING_VALUE
    '''
    pass

def p_selector(p):
    '''
    list_selector : STRING_VALUE SELECTOR
                |   STRING_VALUE SEPARATOR
                |   list_string SELECTOR
                |   list_string SEPARATOR
                |   SEPARATOR
                |   SELECTOR
    '''
    pass

# def p_structure(p):
#     ''' structure : WHILE expression '{' programme '}' '''
#     p[0] = AST.WhileNode([p[2],p[4]])

# def p_minus(p):
#     ''' expression : ADD_OP expression %prec UMINUS'''
#     p[0] = AST.OpNode(p[1], [p[2]])

# def p_error(p):
#     if p:
#         print ("Syntax error in line %d" % p.lineno)
#         yacc.errok()
#     else:
#         print ("Sytax error: unexpected end of file!")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

precedence = (
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'MIXIN'),
    ('nonassoc', 'SELECTOR'),
    ('nonassoc', 'VARIABLE'),
    ('nonassoc', 'SEPARATOR'),
    ('nonassoc', 'STRING_VALUE'),
	('nonassoc', 'SELECTOR_EXTEND'),
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    # ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug = False)
    if result:
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
