from HEXCell import *
from Player import *
import HEXDrawer


class HEX:

    def __init__(self, size, initial_player):
        self.size = size
        self.height = size
        self.width = size
        self.board = [[HEXCell(x, y) for x in range(self.width)] for y in range(self.height)]
        self.initial_player = initial_player
        self.player = initial_player  # current player
        self.connect_board()
        self.initial_player_owned_top, self.initial_player_owned_bottom = self.create_owned_cells(initial_player)
        self.other_player_owned_top, self.other_player_owned_top_bottom = self.create_owned_cells(Player.other(initial_player))

        intersection = set(self.initial_player_owned_top+self.initial_player_owned_bottom).intersection(set(self.other_player_owned_top+self.other_player_owned_top_bottom))
        # cover edge cases of both players owning the edge cells
        for cell in intersection:
            cell.owner = "both"

    def connect_board(self):
        board = self.board

        for row in board:
            # print(row)
            for cell in row:
                # print(cell)
                legal_moves = self.get_legal_moves(cell.x, cell.y)
                for l in legal_moves:
                    cell.add_neighbour(l)

    def create_owned_cells(self, player):
        if player == self.initial_player:
            first = [self.board[x][0] for x in range(self.size)]
            second = [self.board[x][self.size - 1] for x in range(self.size)]
        else:
            first = [self.board[0][y] for y in range(self.size)]
            second = [self.board[self.size - 1][y] for y in range(self.size)]
        for cell in first+second:
            cell.owner = player
        return first, second

    def get_cell(self, x, y):
        return self.board[y][x]

    def get_legal_moves(self, x, y):
        indices = self.get_surounding_indices(x, y)
        moves = [self.get_cell(x, y) for (x, y) in indices]
        moves = list(filter(lambda x: x != None, moves))

        return list(filter(lambda cell: self.is_valid_move(cell.x, cell.y), moves))

    def get_surounding_indices(self, x, y):
        #                left      up           right      down      up-right    down-left
        potential = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
        return list(
            filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] <= self.width - 1 and x[1] <= self.height - 1, potential))

    def do_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[y][x].player = self.player
            self.__switch_player__()
        else:
            raise Exception("Invalid move, x=", x, "y=", y, self.player, "On cell", self.get_cell(x, y))

    def do_move_from_cell(self, hex_cell):
        self.do_move(hex_cell.x, hex_cell.y)

    def is_valid_move(self, x, y):
        cell = self.get_cell(x, y)
        return cell.player is None

    def is_valid_move_cell(self, cell):
        return self.is_valid_move(cell.x, cell.y)

    def is_done(self):
        player = self.initial_player
        for cell in self.initial_player_owned_top:
            if self.__find_path__(self.initial_player_owned_top, self.initial_player_owned_bottom, cell, player):
                return True
        for cell in self.initial_player_owned_bottom:
            if self.__find_path__(self.initial_player_owned_bottom, self.initial_player_owned_top, cell, player):
                return True

        player = Player.other(player)
        for cell in self.other_player_owned_top:
            if self.__find_path__(self.other_player_owned_top, self.other_player_owned_top_bottom, cell, player):
                return True
        for cell in self.other_player_owned_top_bottom:
            if self.__find_path__(self.other_player_owned_top_bottom, self.other_player_owned_top, cell, player):
                return True

        return False

    def __find_path__(self, from_owned, to_owned, node, player, visited=[]):
        if node in to_owned: return True

        if node.player == player:
            visited.append(node)
            ns = node.neighbours
            next = list(filter(lambda cell: cell.player == player and cell not in visited, ns))
            if len(next) > 0:
                return self.__find_path__(from_owned, to_owned, next[0], player, visited)
        return False

    def __next_player__(self):
        return Player.other(self.player)

    def __current_player__(self):
        return self.player

    def __switch_player__(self):
        self.player = Player.other(self.player)

    def __get_all_nodes_as_list__(self):
        if hasattr(self,"all_nodes"): return self.all_nodes

        _nodes = []
        for row in self.board:
            for cell in row:
                _nodes.append(cell)
        self.all_nodes = _nodes  # caching
        return _nodes

    def __graph_current_state__(self):
        HEXDrawer.graph(self.__get_all_nodes_as_list__())
