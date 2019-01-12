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
            |   list section
            |   list_separator section
            |   GT_OP section
            |   STRING_VALUE GT_OP section
            |   GT_OP STRING_VALUE section
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[0] = AST.StatementNode([p[1]]+p[2].children)
    elif len(p) > 3:
        p[0] = AST.StatementNode([AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2])])]+p[3].children)
    else:
        p[0] = AST.StatementNode([AST.ValuesNode([AST.ValueNode(p[1])])]+p[2].children)

def p_extend_define(p):
    '''
    statement : SELECTOR_EXTEND section
    '''
    p[0] = AST.ExtendNodeDefine(p[1], [p[2]])

def p_extend(p):
    '''
    statement : '@' EXTEND SELECTOR_EXTEND ';'
    '''
    p[0] = AST.ExtendNode(p[3])

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
            |   variable ':' boolean ';'
    '''
    if len(p) > 3:
        p[0] = AST.AssignNode([p[1],p[3]])
    else:
        p[0] = AST.AssignNode([p[1],p[2]])

def p_attribution(p):
    '''
    attribution : ':' STRING_VALUE ';'
                | ':' list ';'
                | ':' variable ';'
                | ':' expression ';'
    '''
    if isinstance(p[2], AST.ValuesNode):
        p[0] = p[2]
    elif isinstance(p[2], AST.VariableNode):
        p[0] = AST.ValuesNode([p[2]])
    else:
        p[0] = AST.ValuesNode([AST.ValueNode(p[2])])

def p_import(p):
    '''
    statement : '@' IMPORT FILE_PATH ';'
    '''
    p[0] = AST.ImportNode(p[3].replace("'", ""))

def p_mixin(p):
    '''
    statement : '@' MIXIN STRING_VALUE '(' list_variable ')' section
            |   '@' MIXIN STRING_VALUE '(' variable ')' section
            |   '@' MIXIN STRING_VALUE '(' ')' section
            |   '@' MIXIN STRING_VALUE section
    '''
    #TODO
    if len(p) > 7:
        if isinstance(p[5], AST.ValuesNode):
            p[0] = AST.MixinNode(p[3],p[5],p[7])
        else:
            p[0] = AST.MixinNode(p[3],AST.ValuesNode([p[5]]),p[7])
    elif len(p) > 5:
        p[0] = AST.MixinNode(p[3],None,p[6])
    else:
        p[0] = AST.MixinNode(p[3],None,p[4])

def p_include(p):
    '''
    statement : '@' INCLUDE STRING_VALUE '(' list ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' STRING_VALUE ')' ';'
            |   '@' INCLUDE STRING_VALUE '(' ')' ';'
            |   '@' INCLUDE STRING_VALUE ';'
    '''

    if len(p) > 5:
        if isinstance(p[5], AST.ValuesNode):
            p[0] = AST.IncludeNode(p[3], p[5])
        else:
            p[0] = AST.IncludeNode(p[3], AST.ValuesNode([AST.ValueNode(p[5])]))
    else:
        p[0] = AST.IncludeNode(p[3])

def p_while(p):
    '''
    statement : '@' WHILE expression section
            |   '@' WHILE variable section
            |   '@' WHILE boolean section
    '''
    p[0] = AST.WhileNode([p[3], p[4]])

def p_if(p):
    '''
    statement : IF expression section
            |   IF variable section
            |   IF boolean section
            |   IF expression section else_if_block
            |   IF variable section else_if_block
            |   IF boolean section else_if_block
            |   IF expression section else_block
            |   IF variable section else_block
            |   IF boolean section else_block
    '''
    try:
        p[0] = AST.IfNode([p[2], p[3], p[4]])
    except:
        p[0] = AST.IfNode([p[2], p[3]])

def p_else_if_block(p):
    '''
    else_if_block : ELIF expression section
                |   ELIF variable section
                |   ELIF boolean section
                |   ELIF expression section else_if_block
                |   ELIF variable section else_if_block
                |   ELIF boolean section else_if_block
                |   ELIF expression section else_block
                |   ELIF variable section else_block
                |   ELIF boolean section else_block
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

def p_list_variable(p):
    '''
    list_variable : list_variable ',' variable
                |   variable ',' variable
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[1].children += [AST.ValueNode(p[2]), p[3]]
        p[0] = p[1]
    else:
        p[0] = AST.ValuesNode([p[1], AST.ValueNode(p[2]), p[3]])

def p_list_sep_rec(p):
    '''
    list : list ',' boolean
        |  list ',' variable
        |  list ',' expression
        |  list ',' STRING_VALUE
        |  list_variable ',' boolean
        |  list_variable ',' expression
        |  list_variable ',' STRING_VALUE
    '''
    p[0] = p[1]
    if not isinstance(p[3], AST.ValueNode):
        p[3] = AST.ValueNode(p[3])
    p[0].children += [AST.ValueNode(p[2]), p[3]]

def p_list_sep(p):
    '''
    list : boolean ',' boolean
        |  boolean ',' variable
        |  boolean ',' expression
        |  boolean ',' STRING_VALUE
        |  variable ',' boolean
        |  variable ',' expression
        |  variable ',' STRING_VALUE
        |  expression ',' boolean
        |  expression ',' variable
        |  expression ',' expression
        |  expression ',' STRING_VALUE
        |  STRING_VALUE ',' boolean
        |  STRING_VALUE ',' variable
        |  STRING_VALUE ',' expression
        |  STRING_VALUE ',' STRING_VALUE
    '''
    if not isinstance(p[1], AST.ValueNode):
        p[1] = AST.ValueNode(p[1])
    if not isinstance(p[3], AST.ValueNode):
        p[3] = AST.ValueNode(p[3])
    p[0] = AST.ValuesNode([p[1], AST.ValueNode(p[2]), p[3]])

def p_list_separator(p):
    '''
    list_separator : STRING_VALUE GT_OP STRING_VALUE
                |    list_separator GT_OP STRING_VALUE
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[0] = p[1]
        p[0].children += [AST.ValueNode(p[2]), AST.ValueNode(p[3])]
    else:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2]), AST.ValueNode(p[3])])

def p_list_separator_advance(p):
    '''
    list : variable list_separator
        |  expression list_separator
        |  STRING_VALUE list_separator
    '''
    p[0] = p[2]
    if not isinstance(p[1], AST.ValueNode):
        p[1] = AST.ValueNode(p[1])
    p[0].children.insert(0, p[1])

def p_list_rec(p):
    '''
    list : list variable
        |  list expression
        |  list STRING_VALUE
        |  list list_separator
    '''
    p[0] = p[1]
    if isinstance(p[2], AST.ValuesNode):
        p[2] = p[2].children[0]
    elif not isinstance(p[2], AST.ValueNode):
        p[2] = AST.ValueNode(p[2])
    p[0].children += [p[2]]

def p_list(p):
    '''
    list : STRING_VALUE STRING_VALUE
        |  STRING_VALUE variable
        |  STRING_VALUE expression
        |  variable STRING_VALUE
        |  variable variable
        |  variable expression
        |  expression STRING_VALUE
        |  expression variable
        |  expression expression
    '''
    if not isinstance(p[1], AST.ValueNode):
        p[1] = AST.ValueNode(p[1])
    if not isinstance(p[2], AST.ValueNode):
        p[2] = AST.ValueNode(p[2])
    p[0] = AST.ValuesNode([p[1], p[2]])

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

def p_expression_comparison_LGTE(p):
    '''
    boolean : expression GT_OP expression
            | expression LGTE_OP expression
            | expression GT_OP variable
            | expression LGTE_OP variable
            | variable GT_OP expression
            | variable LGTE_OP expression
            | variable GT_OP variable
            | variable LGTE_OP variable
    '''
    p[0] = AST.BoolOpNode(p[2], [p[1], p[3]])

def p_expression_comparison(p):
    '''
    boolean : expression COMP_OP expression
            | expression COMP_OP variable
            | expression COMP_OP boolean
            | expression COMP_OP STRING_VALUE
            | variable COMP_OP expression
            | variable COMP_OP variable
            | variable COMP_OP boolean
            | variable COMP_OP STRING_VALUE
            | boolean COMP_OP expression
            | boolean COMP_OP variable
            | boolean COMP_OP boolean
            | boolean COMP_OP STRING_VALUE
            | STRING_VALUE COMP_OP expression
            | STRING_VALUE COMP_OP variable
            | STRING_VALUE COMP_OP boolean
            | STRING_VALUE COMP_OP STRING_VALUE
    '''
    if not isinstance(p[1], AST.ValueNode):
        p[1] = AST.ValueNode(p[1])
    if not isinstance(p[3], AST.ValueNode):
        p[3] = AST.ValueNode(p[3])
    p[0] = AST.BoolOpNode(p[2], [p[1], p[3]])

def p_boolean_operation(p):
    '''
    boolean : boolean OR boolean
            | boolean AND boolean
            | NOT boolean
    '''
    if isinstance(p[1], str):
        p[0] = AST.BoolOpNode(p[1],[p[2]])
    else:
        p[0] = AST.BoolOpNode(p[2],[p[1], p[3]])

def p_boolean_simplify(p):
    '''
    boolean : '(' boolean ')'
    '''
    p[0] = p[2]

def p_boolean_value(p):
    '''
    boolean : FALSE
            | TRUE
    '''
    p[0] = AST.BoolNode(p[1] == "true")

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

# def p_minus(p):
#     ''' expression : ADD_OP expression %prec UMINUS'''
#     p[0] = AST.OpNode(p[1], [p[2]])

# def p_error(p):
#     if p:
#         print ("Syntax error in line %d" % p.lineno)
#         yacc.errok()
#     else:
#         print ("Sytax error: unexpected end of file!")

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")

precedence = (
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'VARIABLE'),
    ('nonassoc', 'STRING_VALUE'),
	('nonassoc', 'SELECTOR_EXTEND'),
    ('nonassoc', 'FILE_PATH'),
    ('nonassoc', 'TRUE'),
	('nonassoc', 'FALSE'),
    ('left', 'AND'),
    ('left', 'OR'),
    ('left', 'LGTE_OP'),
    ('left', 'GT_OP'),
    ('left', 'COMP_OP'),
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'NOT'),
    ('left', 'IF'),
    ('left', 'ELIF'),
    ('left', 'ELSE'),
    ('right', 'MIXIN'),
    ('right', 'INCLUDE'),
	('right', '@'),
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
