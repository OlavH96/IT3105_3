from HEXCell import *


class HEX:

    def __init__(self, height, width, initial_player):
        self.board = [[HEXCell(x, y) for x in range(width)] for y in range(height)]
        self.initial_player = initial_player
        self.height = height
        self.width = width
        self.connect_board()

    def connect_board(self):
        board = self.board

        for row in board:
            # print(row)
            for cell in row:
                # print(cell)
                legal_moves = self.get_legal_moves(cell.x, cell.y)
                for l in legal_moves:
                    cell.add_neighbour(l)

    def get_cell(self, x, y):
        return self.board[y][x]

    def get_legal_moves(self, x, y):
        indices = self.get_surounding_indices(x, y)
        moves = [self.get_cell(x, y) for (x, y) in indices]
        moves = list(filter(lambda x: x != None, moves))

        return list(filter(lambda cell: self.is_valid_move(cell.x, cell.y), moves))

    def get_surounding_indices(self, x, y):
        #                left      up      right   down   up-right    down-left
        potential = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
        return list(filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] <= self.width-1 and x[1] <= self.height-1, potential))

    def do_move(self, x, y, player):
        self.board[y][x].player = player

    def is_valid_move(self, x, y):
        cell = self.get_cell(x, y)
        return cell.player is None

    def is_done(self):
        pass

    def print_board(self):
        pass
