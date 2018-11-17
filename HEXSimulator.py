import random

from HEX import *
from HEXCell import *
from Player import *
import HEXDrawer
import time
from MCTS import *
from HEXStateManager import *
from RandomPolicy import *
from NNPolicy import *


def play_game(mcts, player, policy, stateman: HEXStateManager, data):
    start: Node = mcts.tree
    state: Node = start
    #game: HEX = state.content.__copy__()

    while not stateman.is_final_state(state.content):#game.is_done():

        # if stateman.is_final_state(game) or stateman.is_final_state(state.content):
        #     print("ERROR")
        #     print(game)
        #     print(state)
        #     print(stateman.is_final_state(game))
        #     print(stateman.is_final_state(state.content))

        choice = mcts.tree_search(state)

        child_node: Node = state.getChildByEdge(choice)

        # game.do_move_from_cell(choice.move)

        state = child_node  ##stateman.do_move(hex, choice)

        state.content.__graph_current_state__()

    return state.content.get_winner()


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

    size = 3
    G = 50
    P = "Player 1"
    M = 1
    default_policy = RandomPolicy()
    initial_player = player_from_string(P)
    stateman = HEXStateManager()
    game: HEX = stateman.generate_initial_state([size], player=initial_player)

    nn_policy = NNPolicy(len(game.__get_all_cells_as_list__()), len(game.get_all_legal_moves()))
    # game.do_move(0,0)
    # game.do_move(1,1)
    print(nn_policy.chose(game))

    # game.__graph_current_state__()
    # states: [HEX] = stateman.generate_child_states(game)
    # for s in states:
    #     s.__graph_current_state__()
    # exit(1)
    wins = 0
    losses = 0
    for i in range(G):
        copy = game.__copy__()
        mcts = MCTS(statemanager=stateman, initial_state=copy, policy=default_policy, default_policy=default_policy,
                    M=M)

        winner = play_game(mcts, initial_player, default_policy, stateman, [size])
        # mcts.tree.print_entire_tree()
        print("Winner", winner)
        if winner == initial_player:
            wins += 1
        else:
            losses += 1
    mcts.tree.print_entire_tree()
    print("Wins", wins)
    print("Losses", losses)
    print("Winrate", wins / G)
