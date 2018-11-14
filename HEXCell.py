class HEXCell:

    def __init__(self, x, y):
        self.player = None
        self.neighbours = set()
        self.owner = None
        self.x = x
        self.y = y

    def add_neighbour(self, hex_cell):
        self.neighbours.add(hex_cell)
        hex_cell.neighbours.add(self)

    def __str__(self):
        return "{x="+str(self.x)+" ,y="+str(self.y)+", player=" + str(self.player) + "}"

    def __repr__(self):
        return self.__str__()
