from enum import Enum
import random

class Player(Enum):
    PLAYER_1 = "Player 1"
    PLAYER_2 = "Player 2"

    @staticmethod
    def other(player):
        if player is Player.PLAYER_1:
            return Player.PLAYER_2
        return Player.PLAYER_1

    @staticmethod
    def to_int(player: object) -> int:
        if player is None: return 0
        return 1 if player == Player.PLAYER_1 else -1
    @staticmethod
    def player_from_string(P):
        if P == "Player 1":
            init_player = Player.PLAYER_1
        elif P == "Player 2":
            init_player = Player.PLAYER_2
        elif P == "mix":
            init_player = random.choice([Player.PLAYER_1, Player.PLAYER_2])
        else:
            raise Exception("Invalid Player Choice")
        return init_player
    @staticmethod
    def player_from_int(i):
        return Player.PLAYER_1 if i == 1 else Player.PLAYER_2 if i == -1 else None