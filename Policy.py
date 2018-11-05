from Player import Player
from Move import *

from math import sqrt, log10
import random


class Policy:

    def __init__(self, player, c = 1):
        self.player = player
        self.c = c  # exploration factor

    def Q(self, state, move, z=0):
        return move.reward

    def u(self, node, action):
        Ns = node.visits
        Nsa = action.visits
        if Ns == 0: Ns = 1

        return self.c * sqrt(log10(Ns) / (1 + Nsa))

    def chose(self, node, actions, initial_player):

        if hasattr(node, "content"):
            state = node.content
        else:
            state = node
        options = []
        for action in actions:
            Q = self.Q(node, action)
            u = self.u(node, action)

            if state.player == initial_player:
                sum = Q + u
            else:
                sum = Q - u
            options.append(PolicyChoice(state, action, sum))
        # If there are several with the same value, return a random one

        if state.player == initial_player:
            max_indices = [i for i in range(len(options)) if options[i] == max(options, key=lambda e: e.QuSum)]
            # Optimization
            if len(max_indices) == 1: return options[max_indices[0]].move
            return options[max_indices[random.randint(0, len(max_indices) - 1)]].move

        else:
            min_indices = [i for i in range(len(options)) if options[i] == min(options, key=lambda e: e.QuSum)]
            # Optimization
            if len(min_indices) == 1: return options[min_indices[0]].move
            return options[min_indices[random.randint(0, len(min_indices) - 1)]].move


class PolicyChoice:

    def __init__(self, state, move, QuSum):
        self.state = state
        self.move = move
        self.QuSum = QuSum

    def __str__(self):
        return "State=" + str(self.state) + ", move=" + str(self.move) + ", quSum=" + str(self.QuSum)

    def __eq__(self, other):
        return self.QuSum == other.QuSum
