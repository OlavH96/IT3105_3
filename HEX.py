from HEXCell import *


class HEX:

    def __init__(self, height, width, initial_player):
        self.board = [[HEXCell(x, y) for x in range(width)] for y in range(height)]
        self.initial_player = initial_player
        self.height = height
        self.width = width

    def get_cell(self, x, y):
        #if x >= 0 and x <= self.width - 1 and y >= 0 and y <= self.height - 1:
        return self.board[y][x]
        #return None

    def get_legal_moves(self, x, y):
        indices = self.get_surounding_indices(x, y)
        moves = [self.get_cell(x, y) for (x, y) in indices]
        moves = list(filter(lambda x: x != None, moves))

        return list(filter(lambda cell: self.is_valid_move(cell.x, cell.y), moves))

    def get_surounding_indices(self, x, y):
        #            self   left      up      right   down   up-right    down-left
        potential = [(x, y), (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
        return list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] <= self.width-1 and x[1] <= self.height-1, potential))

    def do_move(self, x, y, player):
        self.board[y][x].player = player

    def is_valid_move(self, x, y):
        cell = self.get_cell(x, y)
        return cell.player == None

    def is_done(self):
        pass

    def print_board(self):
        pass
