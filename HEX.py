from HEXCell import *
from Player import *
import HEXDrawer
import copy


class HEX:

    def __init__(self, size: int, initial_player: Player):
        self.visits = 0
        self.size: int = size
        self.board: [[HEXCell]] = [[HEXCell(x, y) for x in range(size)] for y in range(size)]
        self.initial_player: Player = initial_player
        self.player: Player = initial_player  # current player
        self.connect_board()
        self.initial_player_owned_top, self.initial_player_owned_bottom = self.create_owned_cells(initial_player)
        self.other_player_owned_top, self.other_player_owned_top_bottom = self.create_owned_cells(
            Player.other(initial_player))

        intersection = set(self.initial_player_owned_top + self.initial_player_owned_bottom).intersection(
            set(self.other_player_owned_top + self.other_player_owned_top_bottom))
        # cover edge cases of both players owning the edge cells
        for cell in intersection:
            cell.owner = "both"

    def connect_board(self) -> None:
        board: [[HEXCell]] = self.board
        for row in board:
            for cell in row:
                legal_moves = self.__get_legal_moves_around_cell__(cell.x, cell.y)
                for l in legal_moves:
                    cell.add_neighbour(l)

    def create_owned_cells(self, player: Player):
        if player == self.initial_player:
            first = [self.board[x][0] for x in range(self.size)]
            second = [self.board[x][self.size - 1] for x in range(self.size)]
        else:
            first = [self.board[0][y] for y in range(self.size)]
            second = [self.board[self.size - 1][y] for y in range(self.size)]
        for cell in first + second:
            cell.owner = player
        return first, second

    def get_cell(self, x, y) -> HEXCell:
        return self.board[y][x]

    def get_all_legal_moves(self):
        all_nodes = self.__get_all_cells_as_list__()
        legal = list(filter(lambda node: self.is_valid_move_cell(node), all_nodes))
        return legal

    def __get_legal_moves_around_cell__(self, x, y):
        indices = self.get_surounding_indices(x, y)
        moves = [self.get_cell(x, y) for (x, y) in indices]
        moves = list(filter(lambda x: x != None, moves))

        return list(filter(lambda cell: self.is_valid_move(cell.x, cell.y), moves))

    def get_surounding_indices(self, x, y) -> [(int, int)]:
        #                left      up           right      down      up-right    down-left
        potential = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
        return list(
            filter(lambda x: x[0] >= 0 and x[1] >= 0 and x[0] <= self.size - 1 and x[1] <= self.size - 1, potential))

    def do_move(self, x, y) -> None:
        if self.is_valid_move(x, y):
            self.board[y][x].player = self.player
            self.__switch_player__()
        else:
            raise Exception("Invalid move, x=", x, "y=", y, self.player, "On cell", self.get_cell(x, y))

    def do_move_from_cell(self, hex_cell) -> None:
        self.do_move(hex_cell.x, hex_cell.y)

    def is_valid_move(self, x, y) -> bool:
        cell = self.get_cell(x, y)
        return self.is_valid_move_cell(cell)

    def is_valid_move_cell(self, cell) -> bool:
        return cell.player is None

    def is_done_naive(self) -> bool:
        return sum(map(lambda cell: cell.player is not None, self.__get_all_cells_as_list__())) == self.size ** 2

    def is_done(self) -> bool:
        visited = []
        player = self.initial_player
        for cell in self.initial_player_owned_top:
            if self.__has_path__(self.initial_player_owned_top, self.initial_player_owned_bottom, cell, player,
                                 visited):
                return True
        for cell in self.initial_player_owned_bottom:
            if self.__has_path__(self.initial_player_owned_bottom, self.initial_player_owned_top, cell, player,
                                 visited):
                return True

        player = Player.other(player)
        for cell in self.other_player_owned_top:
            if self.__has_path__(self.other_player_owned_top, self.other_player_owned_top_bottom, cell, player,
                                 visited):
                return True
        for cell in self.other_player_owned_top_bottom:
            if self.__has_path__(self.other_player_owned_top_bottom, self.other_player_owned_top, cell, player,
                                 visited):
                return True

        return self.is_done_naive()

    def get_winner(self) -> Player or None:

        if self.is_done():
            return Player.other(self.player)
        return None

    def __has_path__(self, from_owned, to_owned, node, player, visited) -> bool:
        if node in to_owned: return True

        if node.player == player:
            visited.append(node)
            ns = node.neighbours
            next_nodes = list(filter(lambda cell: cell.player == player and cell not in visited, ns))
            if len(next_nodes) > 0:
                return self.__has_path__(from_owned, to_owned, next_nodes[0], player, visited)
        return False

    def __next_player__(self) -> Player:
        return Player.other(self.player)

    def __current_player__(self) -> Player:
        return self.player

    def __switch_player__(self) -> None:
        self.player = Player.other(self.player)

    def __get_all_cells_as_list__(self) -> [HEXCell]:

        # if hasattr(self, "all_nodes"): return self.all_nodes

        _nodes = []
        for row in self.board:
            for cell in row:
                _nodes.append(cell)
        # self.all_nodes = _nodes  # caching
        return _nodes

    def __graph_current_state__(self, file_number=""):
        HEXDrawer.graph(self.__get_all_cells_as_list__(), name="HEX"+str(file_number))

    def __copy__(self):
        return copy.deepcopy(self)

    def __str__(self):
        taken = sum(map(lambda cell: cell.player is not None, self.__get_all_cells_as_list__()))
        return "HEX{" + str(taken) + "/" + str(self.size ** 2) + "}"
