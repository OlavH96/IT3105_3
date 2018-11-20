class Edge:

    def __init__(self, fromNode, toNode, content):
        self.fromNode = fromNode
        self.toNode = toNode
        self.content = content

    def quality(self):
        return self.content.reward / self.content.visits

    def __str__(self):
        return "Edge{from=" + str(self.fromNode) + ", to=" + str(self.toNode) + ", content=" + str(self.content) + "}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash((self.fromNode, self.toNode, self.content))
