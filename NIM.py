from Move import *
from Player import *


class NIM:

    def __init__(self, N, K, player, initial_player):
        self.initial_player = initial_player
        self.player = player
        self.N = N  # Pieces on the board
        self.K = K  # max pieces you can take, you can take less, but not more.
        self.visits = 0
        self.winner = None

    def winnerF(self):
        if not self.isDone(): return None

        return self.player

    def take(self, number):

        if not self.isValidMove(number):
            raise Exception("Invalid move", number, "for game", self)

        self.N -= number

        if self.isDone():
            self.winner = self.player
        else:
            self.player = Player.other(self.player)

        return self

    def isValidMove(self, number):

        return number <= self.K and self.N - number >= 0

    def getValidMoves(self):

        if self.K > self.N:
            return list(range(1, self.N + 1))

        return list(range(1, self.K + 1))

    def isDone(self):

        return self.N <= 0

    def __str__(self):
        return "{N=" + str(self.N) + ", K=" + str(self.K) + "}"

    def __copy__(self):

        return NIM(self.N, self.K, self.player, self.initial_player)

    def __eq__(self, other):

        return hash(other) == hash(self)

        # return self.K == other.K and self.N == other.N and self.player == other.player

    def __hash__(self):
        return hash((self.K, self.N))
