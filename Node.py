from Edge import *


class Node:

    def __init__(self, content, parent=None):
        self.content = content
        self.edges = set()
        self.parent = parent
        self.visits = 0

    def addChild(self, edgeContent, toContent):
        toNode = Node(toContent, self)
        edge = Edge(self, toNode, edgeContent)
        self.edges.add(edge)
        return toNode

    def getChild(self, content):
        return Node.find(content, self)

    def getChildByEdge(self, edgeContent):
        # print("Getting child by edge",self, edgeContent)
        for edge in self.edges:
            # print("Edge",edge.content)
            if edge.content == edgeContent: return edge.toNode

    def getEdgeTo(self, otherNode):

        for edge in self.edges:
            if edge.toNode == otherNode:
                return edge
        return None

    def __str__(self):
        return "Node{content=" + str(self.content) + ", children=" + str(len(self.edges)) + "}"

    def print_entire_tree(self):
        self.print_tree(self, 0)

    def print_tree(self, node, i, edge=None):
        to_print = "|" * i
        # if edge: print(to_print, edge)
        if edge:
            print(to_print, edge.content.move, "->", edge.toNode.content, "[reward=", edge.content.reward, ", visits=",
                  str(edge.content.visits) + "]")
        else:
            print(to_print, node.content)

        for edge in node.edges:
            # print("Edge",edge)
            to = edge.toNode
            # print("To",to)
            self.print_tree(to, i + 1, edge)

    # DFS search
    @staticmethod
    def find(content, tree):
        if tree.content == content: return tree

        for c in tree.edges:
            node = Node.find(content, c.toState)
            if node is not None:
                return node

    def get_visit_count_distribution(self):
        dist = [(e.content.parent, e.toNode.visits) for e in self.edges]
        return dist