# coding: latin-1

''' Petit module utilitaire pour la construction, la manipulation et la
representation d'arbres syntaxiques abstraits.

Surement plein de bugs et autres surprises a prendre comme un
"work in progress"...
Notamment, l'utilisation de pydot pour representer un arbre syntaxique cousu
est une utilisation un peu "limite" de graphviz. ca marche, mais le layout n'est
pas toujours optimal...
'''

import pydot

class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type

    def makegraphicaltree(self, dot=None, edgeLabels=True):
            if not dot: dot = pydot.Dot()
            dot.add_node(pydot.Node(self.ID,label=repr(self), shape=self.shape))
            label = edgeLabels and len(self.children)-1
            
            for i, c in enumerate(self.children):
                c.makegraphicaltree(dot, edgeLabels)
                edge = pydot.Edge(self.ID,c.ID)
                if label:
                    edge.set_label(str(i))
                dot.add_edge(edge)
                #Workaround for a bug in pydot 1.0.2 on Windows:
                #dot.set_graphviz_executables({'dot': r'C:\Program Files\Graphviz2.38\bin\dot.exe'})
            return dot

    def threadTree(self, graph, seen = None, col=0):
            colors = ('red', 'green', 'blue', 'yellow', 'magenta', 'cyan')
            if not seen: seen = []
            if self in seen: return
            seen.append(self)
            new = not graph.get_node(self.ID)
            if new:
                graphnode = pydot.Node(self.ID,label=repr(self), shape=self.shape)
                graphnode.set_style('dotted')
                graph.add_node(graphnode)
            label = len(self.next)-1
            for i,c in enumerate(self.next):
                if not c: return
                col = (col + 1) % len(colors)
                col=0 # FRT pour tout afficher en rouge
                color = colors[col]
                c.threadTree(graph, seen, col)
                edge = pydot.Edge(self.ID,c.ID)
                edge.set_color(color)
                edge.set_arrowsize('.5')
                # Les arretes correspondant aux coutures ne sont pas prises en compte
                # pour le layout du graphe. Ceci permet de garder l'arbre dans sa representation
                # "standard", mais peut provoquer des surprises pour le trajet parfois un peu
                # tarabiscote des coutures...
                # En commantant cette ligne, le layout sera bien meilleur, mais l'arbre nettement
                # moins reconnaissable.
                edge.set_constraint('false')
                if label:
                    edge.set_taillabel(str(i))
                    edge.set_labelfontcolor(color)
                graph.add_edge(edge)
            return graph

#done
class ProgramNode(Node):
    type = 'Program'

#done
class StatementNode(Node):
    type = 'Statement'

#done
class ExtendNodeDefine(Node):
    type = 'ExtendNodeDefine'
    def __init__(self, identifier, children):
        Node.__init__(self, children)
        self.identifier = identifier

#done
class MixinNode(Node):
    type = 'MixinNode'
    def __init__(self, identifier, parameters, children):
        Node.__init__(self, children)
        self.parameters = parameters
        self.identifier = identifier

# done
class IncludeNode(Node):
    type = 'IncludeNode'
    def __init__(self, identifier, children = None):
        Node.__init__(self, children)
        self.identifier = identifier

#done
class IfNode(Node):
    type = 'IfNode'
    def __init__(self, children):
        Node.__init__(self, children)

#done
class WhileNode(Node):
    type = 'WhileNode'
    def __init__(self, children):
        Node.__init__(self, children)

# done
class BoolNode(Node):
    type = 'BoolNode'
    def __init__(self, value):
        Node.__init__(self)
        self.value = value

    def __repr__(self):
        return repr(self.value)

#done
class ImportNode(Node):
    type = 'ImportNode'
    def __init__(self, value):
        Node.__init__(self)
        self.value = value

    def __repr__(self):
        return repr(self.value)

#done
class ExtendNode(Node):
    type = 'ExtendStatement'
    def __init__(self, identifier, children = None):
        Node.__init__(self, children)
        self.identifier = identifier

#done
class SelectorsNode(Node):
    type = 'selectors'
    def __init__(self, identifier, children = None):
        Node.__init__(self, children)
        self.identifier = identifier

#done
class NumberNode(Node):
    type = 'number'

    def __init__(self, value, unit = ''):
        Node.__init__(self)
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f'N : {self.value}{self.unit}'

#done
class VariableNode(Node):
    type = 'variable'

    def __init__(self, value):
        Node.__init__(self)
        self.value = value

    def __repr__(self):
        return "V : " + repr(self.value)

#done
class ValueNode(Node):
    type = 'number'

    def __init__(self, value):
        Node.__init__(self)
        self.value = value

    def __repr__(self):
        return repr(self.value)

#done
class ValuesNode(Node):
    type = 'values'

#done
class RuleNode(Node):
    type = 'rule'

#done
class BoolOpNode(Node):
    type = 'BoolOpNode'
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op

    def __repr__(self):
        return repr(self.op)

#done
class OpNode(Node):
    type = "OpNode"
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op

        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1

    def __repr__(self):
        return repr(self.op)

#done
class AssignNode(Node):
    type = '='


def addToClass(cls):
    ''' Decorateur permettant d'ajouter la fonction decoree en tant que methode
    a une classe.

    Permet d'implementer une forme elementaire de programmation orientee
    aspects en regroupant les methodes de differentes classes implementant
    une meme fonctionnalite en un seul endroit.

    Attention, apres utilisation de ce decorateur, la fonction decoree reste dans
    le namespace courant. Si cela derange, on peut utiliser del pour la detruire.
    Je ne sais pas s'il existe un moyen d'eviter ce phenomene.
    '''
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator
