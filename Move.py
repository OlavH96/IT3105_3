class Move:

    def __init__(self, parent, move, result, player):
        self.parent = parent
        self.move = move
        self.result = result
        self.player = player
        self.visits = 0
        self.reward = 0

    def __str__(self):
        return "Move: " + str(self.parent) + " -> " + str(self.move) + " -> " + str(self.result) + ", visits=" + str(
            self.visits) + ", reward=" + str(self.reward)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.parent, self.move, self.result))

    def __eq__(self, other):
        return hash(self) == hash(other)
