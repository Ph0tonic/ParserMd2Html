import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_programme_statement(p):
    ''' programme : statement '''
    # p[0] = AST.ProgramNode(p[1])
    pass

def p_programme_recursive(p):
    ''' programme : statement programme '''
    # p[0] = AST.ProgramNode([p[1]]+p[3].children)
    pass

def p_statement(p):
    '''
    statement : selectors '{' rules '}'
            |   STRING_VALUE '{' rules '}'
            |   string_values '{' rules '}'
    '''
    pass

def p_selectors_without_sep(p):
    '''
    selectors : SELECTOR
            |   SELECTOR selectors
            |   STRING_VALUE selectors
            |   selectors STRING_VALUE
            |   string_values selectors
            |   selectors string_values
    '''
    pass

def p_selectors_with_sep(p):
    '''
    selectors : SELECTOR SEPARATOR selectors
            |   STRING_VALUE SEPARATOR selectors
            |   STRING_VALUE SEPARATOR STRING_VALUE
            |   selectors SEPARATOR STRING_VALUE
            |   string_values SEPARATOR selectors
            |   selectors SEPARATOR string_values
    '''
    pass

def p_rules(p):
    '''
    rules : rule rules
            | rule
    '''
    pass

def p_rule(p):
    '''
    rule : STRING_VALUE ':' values ';'
        |   STRING_VALUE ':' STRING_VALUE ';'
        |   STRING_VALUE ':' string_values ';'
    '''
    pass

def p_string_values(p):
    '''
    string_values : STRING_VALUE string_values
                |   STRING_VALUE STRING_VALUE
    '''

def p_values(p):
    '''
    values : NUMBER values
             | NUMBER
             | STRING_VALUE values
             | string_values values
             | values STRING_VALUE
             | values string_values
    '''
    pass

# def p_structure(p):
#     ''' structure : WHILE expression '{' programme '}' '''
#     p[0] = AST.WhileNode([p[2],p[4]])

# def p_expression_op(p):
#     '''expression : expression ADD_OP expression
#             | expression MUL_OP expression'''
#     p[0] = AST.OpNode(p[2], [p[1], p[3]])


# def p_identifier(p):
#     '''
#     STRING_VALUE SEPARATOR_IDENTIFIER
#     '''

# def p_minus(p):
#     ''' expression : ADD_OP expression %prec UMINUS'''
#     p[0] = AST.OpNode(p[1], [p[2]])

# def p_assign(p):
#     ''' assignation : VARIABLE ':' expression ';' '''
#     p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
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
    result = yacc.parse(prog, debug = True)
    # if result:
    #     print (result)
    #
    #     import os
    #     graph = result.makegraphicaltree()
    #     name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    #     graph.write_pdf(name)
    #     print ("wrote ast to", name)
    # else:
    #     print ("Parsing returned no result!")
