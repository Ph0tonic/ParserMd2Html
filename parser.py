import ply.yacc as yacc

from lex import tokens
import AST

import re

extend_statement = {}

def p_programme_recursive(p):
    '''
    programme : programme programme
    '''
    p[0] = AST.ProgramNode(p[1].children+p[2].children)

def p_programme_statement(p):
    '''
    programme : statement
    '''
    p[0] = AST.ProgramNode([p[1]])

def p_extend_statement(p):
    '''
    statement : SELECTOR_EXTEND '{' rules '}'
            | SELECTOR_EXTEND '{' nested_statement '}'
            | SELECTOR_EXTEND '{' programme '}'
    '''
    p[0] = AST.ExtendStatementNode(p[1], p[3].children)

def p_nested_statement_rules(p):
    '''
    nested_statement : programme rules
                    | rules programme
    '''
    p[0] = AST.NestedStatementNode(p[1].children + p[2].children)

def p_nested_statement_rules_combined(p):
    '''
    nested_statement : rules nested_statement
                    |   programme nested_statement
    '''
    p[2].children = p[1].children + p[2].children
    p[0] = p[2]

def p_rules(p):
    '''
    rules : rules rules
    '''
    p[0] = AST.RulesNode(p[1].children+p[2].children)

def p_rules_simple(p):
    '''
    rules : rule
    '''
    p[0] = AST.RulesNode([p[1]])

def p_rule(p):
    '''
    rule : STRING_VALUE ':' values ';'
        |   STRING_VALUE ':' variable ';'
        |   STRING_VALUE ':' string_values ';'
        |   STRING_VALUE ':' STRING_VALUE ';'
    '''
    if not isinstance(p[3], AST.ValuesNode) and not isinstance(p[3], AST.VariableNode):
        # TODO improve
        p[3] = AST.ValueNode(p[3])
    p[0] = AST.RuleNode([AST.ValueNode(p[1]),p[3]])

def p_statement(p):
    '''
    statement : selectors '{' rules '}'
            |   selectors '{' programme '}'
            |   selectors '{' nested_statement '}'
    '''
    p[0] = AST.StatementNode([AST.SelectorsNode(p[1].children)]+p[3].children)

def p_statement_string_value(p):
    '''
    statement : STRING_VALUE '{' rules '}'
            |   STRING_VALUE '{' programme '}'
            |   STRING_VALUE '{' nested_statement '}'
    '''
    p[0] = AST.StatementNode([AST.SelectorNode(p[1])]+p[3].children)

def p_statement_string_values(p):
    '''
    statement : string_values '{' rules '}'
            |   string_values '{' nested_statement '}'
            |   string_values '{' programme '}'
    '''
    p[0] = AST.StatementNode([AST.SelectorsNode(p[1].children)]+p[3].children)

def p_assign(p):
    '''
    statement : variable ':' string_values ';'
            |   variable ':' values ';'
            |   variable ':' STRING_VALUE ';'
    '''
    p[0] = AST.AssignNode([p[1]])
    if isinstance(p[3], AST.ValuesNode):
        p[0].children.append(p[3])
    else:
        p[0].children.append(AST.ValueNode(p[3]))

def p_selector(p):
    '''
    selectors : SELECTOR
    '''
    p[0] = AST.SelectorsNode([AST.SelectorNode(p[1])])

def p_selectors_without_sep(p):
    '''
    selectors : selectors string_values
            |   selectors STRING_VALUE
    '''
    if isinstance(p[2], AST.ValuesNode):
        p[1].children += p[2].children
    else:
        p[1].children.append(AST.SelectorNode(p[2]))

    p[0] = p[1]

def p_selectors_without_sep_selectors_right(p):
    '''
    selectors : string_values selectors
            |   SELECTOR selectors
            |   STRING_VALUE selectors
    '''
    if isinstance(p[1], AST.ValuesNode):
        p[2].children = p[1].children + p[2].children
    else:
        p[2].children.insert(0, AST.SelectorNode(p[1]))

    p[0] = p[2]


def p_selector_sep_str(p):
    '''
    selectors : STRING_VALUE SEPARATOR STRING_VALUE
    '''
    p[0] = AST.SelectorsNode([AST.SelectorNode(p[1]),AST.SelectorNode(p[2]),AST.SelectorNode(p[3])])

def p_selectors_with_sep(p):
    '''
    selectors : selectors SEPARATOR string_values
            |   selectors SEPARATOR STRING_VALUE
    '''
    p[1].children.append(AST.SelectorNode(p[2]))
    if isinstance(p[3], AST.ValuesNode):
        p[1].children += p[3].children
    else:
        p[1].children.append(AST.SelectorNode(p[3]))

    p[0] = p[1]

def p_selectors_with_sep_selectors_right(p):
    '''
    selectors : SELECTOR SEPARATOR selectors
            |   string_values SEPARATOR selectors
            |   STRING_VALUE SEPARATOR selectors
    '''
    p[3].children.insert(0, AST.SelectorNode(p[2]))

    if isinstance(p[1], AST.ValuesNode):
        p[3].children = p[1].children + p[3].children
    else:
        p[3].children.insert(0, AST.SelectorNode(p[1]))

    p[0] = p[3]

def p_string_values(p):
    '''
    string_values : STRING_VALUE string_values
                |   STRING_VALUE STRING_VALUE
    '''
    if isinstance(p[2], AST.ValuesNode):
        p[2].children.insert(0, AST.ValueNode(p[1]))
        p[0] = p[2]
    else:
        p[0] = AST.ValuesNode([AST.ValueNode(p[1]), AST.ValueNode(p[2])])

def p_values(p):
    '''
    values : string_values values
             | values string_values
    '''
    p[0] = AST.ValuesNode(p[1].children + p[2].children)

def p_values_STRING_VALUE_first(p):
    '''
    values : STRING_VALUE values
    '''
    p[2].children.insert(0, AST.ValueNode(p[1]))
    p[0] = p[2]

def p_values_STRING_VALUE_last(p):
    '''
    values : values STRING_VALUE
    '''
    p[1].children.insert(0, AST.ValueNode(p[2]))
    p[0] = p[1]

def p_values_numbers(p):
    '''
    values : number values
            | number
    '''
    if len(p) == 2:
        p[0] = AST.ValuesNode([p[1]])
    else:
        p[2].children.insert(0, p[1])
        p[0] = p[2]

def p_number(p):
    '''
    number : NUMBER
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

def p_number_operation(p):
    '''
    number : number ADD_OP number
            | number MUL_OP number
    '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_variable(p):
    '''
    variable : VARIABLE
    '''
    p[0] = AST.VariableNode(p[1])

# def p_structure(p):
#     ''' structure : WHILE expression '{' programme '}' '''
#     p[0] = AST.WhileNode([p[2],p[4]])

# def p_expression_op(p):
#     '''expression : expression ADD_OP expression
#             | expression MUL_OP expression'''
#     p[0] = AST.OpNode(p[2], [p[1], p[3]])

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
    ('nonassoc', 'SEPARATOR'),
    ('nonassoc', 'SELECTOR'),
    ('nonassoc', 'NUMBER'),
    ('nonassoc', 'STRING_VALUE'),
    ('nonassoc', 'VARIABLE'),
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
    if result:
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
