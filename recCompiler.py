import AST
from AST import addToClass
from functools import reduce

operations = {
    '+': lambda x,y : f"{x}{y}ADD\n",
    '-': lambda x,y : f"{x}{y}SUB\n",
    '*': lambda x,y : f"{x}{y}MUL\n",
    '/': lambda x,y : f"{x}{y}DIV\n",
}

vars = {}
lineSeperator = '\n'

def compileListToString(list, separator):
    compiledString = separator.join([element.compile() for element in list])

    return compiledString

@addToClass(AST.ValueNode)
def compile(self):
    return str(self.value)

@addToClass(AST.NumberNode)
def compile(self):
    return str(self.value)

@addToClass(AST.SelectorNode)
def compile(self):
    return str(self.selectorStr)

@addToClass(AST.ValuesNode)
def compile(self):
    return compileListToString(self.children, ' ')

@addToClass(AST.RuleNode)
def compile(self):
    children = self.children

    return f'{children[0].compile()} : {children[1].compile()};'

@addToClass(AST.RulesNode)
def compile(self):
    return compileListToString(self.children, '\n');

@addToClass(AST.SelectorsNode)
def compile(self):
    return compileListToString(self.children, ' ')

@addToClass(AST.StatementNode)
def compile(self):
    selector = self.children[0]
    compiledString = f'{selector.compile()} {{ \n'
    compiledStatements = []

    for child in self.children[1:]:
        if isinstance(child, AST.StatementNode):
            childrenStatement = child.children[0].children
            childrenStatement = selector + childrenStatement

            compiledStatements.append(child.compile())
        else:
            compiledString += child.compile()

    compiledString += '}'

    for compiledStatement in compiledStatements:
        compiledString += compiledStatement

    return compiledString

@addToClass(AST.ProgramNode)
def compile(self):
    return compileListToString(self.children, '\n')

def getFileName(path):
    return path.split('/')[-1].split('.')[0]

if __name__ == "__main__" :
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiledString = ast.compile()
    pathCompiled = f'compiled/{getFileName(sys.argv[1])}.css'
    with open(pathCompiled, 'w') as f :
        f.write(compiledString)
