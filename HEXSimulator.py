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
from ReplayBuffer import *
import matplotlib.pyplot as plt


def play_game(mcts, player, policy: NNPolicy, stateman: HEXStateManager, data):
    start: Node = mcts.tree
    state: Node = start  # root in psudocode from assignment

    while not stateman.is_final_state(state.content):
        choice: Move = mcts.tree_search(state)
        print("Choice", choice.move)

        child_node: Node = state.getChildByEdge(choice)
        # print("Child node",child_node.content.get_cell(choice.move.x, choice.move.y))
        # mcts.tree.print_entire_tree()
        dist = start.get_visit_count_distribution()
        training_case: TrainingCase = policy.__create_training_case__(state.content, dist)
        replay_buffer.add(training_case)

        state: Node = child_node
        # policy.train(*dist)
    policy.train(replay_buffer.get_minibatch(5))
    #replay_buffer.clear()
    state.content.__graph_current_state__()

    return state.content.get_winner()


if __name__ == '__main__':
    print("Simulating HEX")

    size = 3
    num_nodes = size ** 2
    G = 20
    P = "Player 1"
    M = 5
    initial_player = Player.player_from_string(P)
    default_policy = Policy(initial_player)
    stateman = HEXStateManager()
    game: HEX = stateman.generate_initial_state([size], player=initial_player)

    replay_buffer: ReplayBuffer = ReplayBuffer()

    config: KerasConfig = KerasConfig(ndim=[num_nodes + 1, num_nodes, num_nodes], oaf="relu")
    nn_policy = NNPolicy(config)
    # game.do_move(0,0)
    # game.do_move(1,1)
    # print(nn_policy.chose(game))

    # game.__graph_current_state__()
    # states: [HEX] = stateman.generate_child_states(game)
    # for s in states:
    #     s.__graph_current_state__()
    # exit(1)
    save_interval = G/1
    wins = 0
    losses = 0
    winrate = []

    for i in range(G):
        copy = game.__copy__()
        mcts = MCTS(statemanager=stateman, initial_state=copy, policy=nn_policy, default_policy=nn_policy,
                    M=M)

        winner = play_game(mcts, initial_player, nn_policy, stateman, [size])
        # mcts.tree.print_entire_tree()
        print("Winner", winner)
        if winner == initial_player:
            wins += 1
        else:
            losses += 1
        winrate.append(wins/(i+1))
        if i % save_interval-1 == 0:
            nn_policy.model.save("networks/mcts"+str(i))

    plt.plot(winrate)
    plt.xlabel("Game")
    plt.ylabel("Winrate")
    plt.show()
    mcts.tree.print_entire_tree()

    training_cases = replay_buffer.get_minibatch(1000000)
    X = [t.F() for t in training_cases]
    Y = [t.D() for t in training_cases]
    X = np.array(X)
    Y = np.array(Y)
    Y = np.interp(Y, (0, Y.max()), (0, 1))


    print(nn_policy.model.evaluate(X,Y))
    print("Wins", wins)
    print("Losses", losses)
    print("Winrate", wins / G)
