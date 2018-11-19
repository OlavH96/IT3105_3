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
from Policy import *
from kerasnn.KerasConfig import *


def play_game(mcts, player, policy, stateman: HEXStateManager, data):
    start: Node = mcts.tree
    state: Node = start

    while not stateman.is_final_state(state.content):

        choice: Move = mcts.tree_search(state)
        print("Choice", choice)

        child_node: Node = state.getChildByEdge(choice)
        print("Child node",child_node)
        mcts.tree.print_entire_tree()
        state: Node = child_node

    state.content.__graph_current_state__(i)
    return state.content.get_winner()





if __name__ == '__main__':
    print("Simulating HEX")

    size = 3
    G = 10
    P = "Player 1"
    M = 10
    initial_player = Player.player_from_string(P)
    default_policy = Policy(initial_player)
    stateman = HEXStateManager()
    game: HEX = stateman.generate_initial_state([size], player=initial_player)

    config: KerasConfig = KerasConfig(ndim=[size**2, size**2, size**2], oaf="relu")
    nn_policy = NNPolicy(config)
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
        mcts = MCTS(statemanager=stateman, initial_state=copy, policy=nn_policy, default_policy=nn_policy,
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
