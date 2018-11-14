import random

from HEX import *
from HEXCell import *
from Player import *
import HEXDrawer
import time
from MCTS import *
from HEXStateManager import *
from RandomPolicy import *
def play_game(mcts, player):
    hex = HEX(5, player)  # todo get from mcts

    while not game.is_done():
        pass


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


if __name__ == '__main__':
    print("Simulating HEX")

    size = 4
    G = 1
    P = "Player 1"
    default_policy = RandomPolicy()
    initial_player = player_from_string(P)
    stateman = HEXStateManager()
    game = stateman.generate_initial_state([size], player=initial_player)

    for i in range(G):

        mcts = MCTS(statemanager=stateman, initial_state=game, policy=policy, default_policy=policy, M=M)

        winner = play_game(mcts, initial_player)
        # mcts.tree.print_entire_tree()
        print("Winner",winner)

        if P == "mix" or P == "Mix":
            init_player = random.choice([Player.PLAYER_1, Player.PLAYER_2])
