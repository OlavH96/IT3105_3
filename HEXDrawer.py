import pydot
from pydot import Dot, Edge
from  Player import *

def print_board(node, depth=0, printed=[]):
    to_print = " " * depth
    print(node)
    printed.append(node)
    print(to_print, node)
    current = node

    for n in current.neighbours:
        if n not in printed:
            print(n, end="-")
            print_board(n, depth + 1, printed)

def color_of_node(node):
    if node.player == Player.PLAYER_1:
        return "blue"
    elif node.player == Player.PLAYER_2:
        return "red"
    else:
        return "green"


def graph(nodes, name="HEX", dname="graphs", draw_branches=True):
    g = Dot(graph_type="digraph")
    g.set_node_defaults(color='lightgray', style='filled', shape='box',
                        fontname='Courier', fontsize='10')

    _nodes = []
    for row in nodes:
        for cell in row:
            _nodes.append(cell)
    nodes = _nodes

    for node in nodes:

        g.add_node(pydot.Node(hash(node), label="", shape="hexagon", width=1, height=1, color=color_of_node(node)))
        for suc in node.neighbours:
            g.add_edge(Edge(node.__hash__(), suc.__hash__(), color='red', shape='-' ))

    g.write_png('%s/%s.png' % (dname, name), prog='neato')
