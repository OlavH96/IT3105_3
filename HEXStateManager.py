import random
from Move import *

from HEX import *


class HEXStateManager:

    def __init__(self):
        pass

    def generate_initial_state(self, data, player):
        self.initial_player = player
        self.game = HEX(*data, player)
        return self.game

    def get_current_player(self):
        return self.game.player

    def generate_child_states(self, state: HEX) -> [HEX]:
        out = []
        for cell in state.get_all_legal_moves():
            copy = state.__copy__()
            copy.do_move_from_cell(cell)
            out.append(copy)
        return out

    def get_moves(self, state: HEX) -> [Move]:
        out = []
        for e in state.get_all_legal_moves():
            copy: HEX = state.__copy__()
            copy.do_move_from_cell(e)
            out.append(Move(state, e, copy, state.player))
        return out

    def random_legal_move(self, state):
        moves = self.get_moves(state)
        if len(moves) == 0: return None
        return moves[random.randint(0, len(moves) - 1)]

    def is_final_state(self, state: HEX) -> bool:
        return state.is_done()

    def reward(self, state):
        return 1 if state.is_final_state() and state.player == self.initial_player else -1

    def do_move(self, state: HEX, move: Move):
        copy: HEX = state.__copy__()
        copy.do_move_from_cell(move)
        return copy

    def is_win(self, state: HEX, player):
        return state.get_winner() == player
