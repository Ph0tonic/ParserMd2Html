import ply.yacc as yacc

from lex import tokens
import AST

import re

extend_statement = {}

def p_program_recursive(p):
    '''
    program : program statement
            | statement
    '''
    try:
        p[1].children.append(p[2])
        p[0] = p[1]
    except:
        p[0] = AST.ProgramNode([p[1]])

def p_statement(p):
    '''
    statement : STRING_VALUE section
            |   list_string section
            |   list_selector section
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[0] = AST.StatementNode([p[1]]+p[2].children)
    else:
        p[0] = AST.StatementNode([AST.ValuesNode([AST.ValueNode(p[1])])]+p[2].children)

def p_extend_define(p):
    '''
    statement : SELECTOR_EXTEND section
    '''
    p[0] = AST.ExtendNodeDefine([AST.ValueNode(p[1]), p[2]])

def p_section(p):
    '''
    section : '{' program '}'
            | '{' '}'
    '''
    if len(p) > 3:
        p[0] = p[2]
    else:
        p[0] = AST.ProgramNode([])

def p_rule(p):
    '''
    statement : STRING_VALUE attribution
    '''
    p[0] = AST.RuleNode([AST.ValueNode(p[1]),p[2]])

def p_assign(p):
    '''
    statement : variable attribution
    '''
    p[0] = AST.AssignNode([p[1],p[2]])

def p_attribution(p):
    '''
    attribution : ':' STRING_VALUE ';'
                | ':' list_string ';'
                | ':' list_value ';'
                | ':' variable ';'
    '''
    if isinstance(p[2], AST.ValuesNode):
        p[0] = p[2]
    elif isinstance(p[2], AST.VariableNode):
        p[0] = AST.ValuesNode([p[2]])
    else:
        p[0] = AST.ValuesNode([AST.ValueNode(p[2])])

def p_extend(p):
    '''
    statement : '@' EXTEND SELECTOR_EXTEND ';'
    '''
    p[0] = AST.ExtendNode(p[3])

def p_mixin(p):
    '''
    statement : '@' MIXIN STRING_VALUE '(' list_variable ')' section
            |   '@' MIXIN STRING_VALUE '(' variable ')' section
            |   '@' MIXIN STRING_VALUE section
    '''
    if len(p) > 5:
        if isinstance(p[5], AST.ValuesNode):
            p[0] = AST.MixinNode(p[3],p[5],p[7])
        else:
            p[0] = AST.MixinNode(p[3],AST.ValuesNode([p[5]]),p[7])
    else:
        p[0] = AST.MixinNode(p[3],None,p[4])

def p_include(p):
    '''
    statement : '@' INCLUDE STRING_VALUE '(' list_value ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' list_string ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' STRING_VALUE ')' ';'
            |   '@' INCLUDE STRING_VALUE ';'
    '''
    if len(p) > 5:
        if isinstance(p[5], AST.ValuesNode):
            p[0] = AST.IncludeNode(p[3], p[5])
        else:
            p[0] = AST.IncludeNode(p[3], AST.ValuesNode([p[5]]))
    else:
        p[0] = AST.IncludeNode(p[3], None)

def p_while(p):
    '''
    statement : '@' WHILE expression section
            |   '@' WHILE variable section
    '''
    p[0] = AST.WhileNode([p[3], p[4]])

def p_if(p):
    '''
    statement : IF expression section
            |   IF variable section
            |   IF expression section else_if_block
            |   IF variable section else_if_block
            |   IF expression section else_block
            |   IF variable section else_block
    '''
    try:
        p[0] = AST.IfNode([p[2], p[3], p[4]])
    except:
        p[0] = AST.IfNode([p[2], p[3]])

def p_else_if_block(p):
    '''
    else_if_block : ELIF expression section
                |   ELIF variable section
                |   ELIF expression section else_if_block
                |   ELIF variable section else_if_block
                |   ELIF expression section else_block
                |   ELIF variable section else_block
    '''
    if len(p) == 4:
        p[0] = AST.IfNode([p[2], p[3]])
    else:
        p[0] = AST.IfNode([p[2], p[3], p[4]])

def p_else_block(p):
    '''
    else_block : ELSE section
    '''
    p[0] = p[2]

def p_list_variables(p):
    '''
    list_variable : list_variable ',' variable
                |   variable ',' variable
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[1].children.append(p[3])
        p[0] = p[1]
    else:
        p[0] = AST.ValuesNode([p[1], p[3]])

def p_list_value_recursive(p):
    '''
    list_value : list_value STRING_VALUE
            |    list_value expression
            |    STRING_VALUE list_value
            |    list_string list_value %prec STRING_VALUE
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[0] = p[1]
        if isinstance(p[2], AST.ValuesNode):
            p[1].children += p[2].children
        elif isinstance(p[2], AST.ValueNode) or isinstance(p[2], AST.NumberNode):
            p[0].children.append(p[2])
        else:
            p[0].children.append(AST.ValueNode(p[2]))
    else:
        p[2].children.insert(0, ASt.ValueNode(p[1]))

def p_list_value(p):
    '''
    list_value : expression
    '''
    p[0] = AST.ValuesNode([p[1]])

def p_list_string(p):
    '''
    list_string : STRING_VALUE STRING_VALUE
                | list_string STRING_VALUE
    '''
    try:
        p[1].children.append(AST.ValueNode(p[2]))
        p[0] = p[1]
    except:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2])])

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

def p_expression_comparison(p):
    '''
    expression : expression EQU_OP expression
            |    expression NEQU_OP expression
            |    expression EQU_OP variable
            |    expression NEQU_OP variable
            |    variable EQU_OP expression
            |    variable NEQU_OP expression
            |    variable EQU_OP variable
            |    variable NEQU_OP variable
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
                |   list_string SELECTOR
                |   list_string SEPARATOR
                |   list_selector ',' SELECTOR
                |   list_selector ',' STRING_VALUE
                |   list_string ',' SELECTOR
    '''
    p[1].children.append(AST.ValueNode(p[2]))
    if len(p) == 4:
        p[1].children.append(AST.ValueNode(p[3]))
    p[0] = p[1]

def p_selector(p):
    '''
    list_selector : STRING_VALUE SELECTOR
                |   STRING_VALUE SEPARATOR
                |   SEPARATOR
                |   SELECTOR
                |   STRING_VALUE ',' SELECTOR
                |   STRING_VALUE ',' STRING_VALUE
    '''
    if len(p) == 4:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2]), AST.ValueNode(p[3])])
    elif len(p) == 3:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2])])
    else:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1])])

# def p_structure(p):
#     ''' structure : WHILE expression '{' program '}' '''
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
    ('nonassoc', 'SELECTOR'),
    ('nonassoc', 'VARIABLE'),
    ('nonassoc', 'SEPARATOR'),
    ('nonassoc', 'STRING_VALUE'),
	('nonassoc', 'SELECTOR_EXTEND'),
    ('left', 'EQU_OP'),
    ('left', 'NEQU_OP'),
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('left', 'IF'),
    ('left', 'ELIF'),
    ('left', 'ELSE'),
    ('right', 'MIXIN'),
    ('right', 'INCLUDE'),
	('right', '@'),
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
