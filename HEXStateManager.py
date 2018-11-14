import random

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

    def generate_child_states(self, state):
        out = []
        for e in state.getValidMoves():
            copy = state.__copy__()
            copy.take(e)
            out.append(copy)  # Move(state, e, copy))
        return out

    def get_moves(self, state):
        out = []
        for e in state.getValidMoves():
            copy = state.__copy__()
            out.append(Move(state, e, copy.take(e), state.player))
        return out

    def random_legal_move(self, state):
        moves = self.get_moves(state)
        if len(moves) == 0: return None
        return moves[random.randint(0, len(moves) - 1)]

    def is_final_state(self, state):
        return state.isDone()

    def reward(self, state):
        return 1 if state.is_final_state() and state.player == self.initial_player else -1

    def do_move(self, state, move):
        copy = state.__copy__()
        copy.take(move.move)
        return copy

    def is_win(self, state, player):
        return state.winnerF() == player