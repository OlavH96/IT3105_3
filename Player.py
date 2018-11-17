from enum import Enum


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
