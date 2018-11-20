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


def test_neural_net(nn_policy: NNPolicy, num_games: int):
    game = HEX(size, Player.PLAYER_1)
    wins = 0
    losses = 0

    for i in range(num_games):

        game_copy = game.__copy__()
        game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))
        game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))
        while not game_copy.is_done():
            action = nn_policy.chose(game_copy, game_copy.get_all_legal_moves())
            game_copy.do_move_from_cell(action)

        if game_copy.get_winner() == Player.PLAYER_1:
            wins += 1
        else:
            losses += 1
    print("Tested NN, winrate:", wins / num_games)


def play_game(mcts, player, policy: NNPolicy, stateman: HEXStateManager, data):
    start: Node = mcts.tree
    state: Node = start  # root in psudocode from assignment

    while not stateman.is_final_state(state.content):
        choice: Move = mcts.tree_search(state)
        if verbose:
            print("Choice", choice)
            # start.print_entire_tree()

        child_node: Node = state.getChildByEdge(choice)
        # print("Child node",child_node.content.get_cell(choice.move.x, choice.move.y))
        # mcts.tree.print_entire_tree()
        # print("visits",list(map(lambda e: e.content.visits,state.edges)))
        dist = state.get_visit_count_distribution()
        training_case: TrainingCase = policy.__create_training_case__(state.content, dist)
        replay_buffer.add(training_case)

        state: Node = child_node
    # dist = start.get_visit_count_distribution()
    # training_case: TrainingCase = policy.__create_training_case__(start.content, dist)
    # replay_buffer.add(training_case)

    policy.train(replay_buffer.get_minibatch(100))
    # replay_buffer.clear()
    if write_image:
        state.content.__graph_current_state__()

    return state.content.get_winner()


def play_game_new(mcts, initial_game: HEX):
    start_state = initial_game
    state = start_state
    while not stateman.is_final_state(state):
        move: Move = mcts.pick_action(state)
        print("Chose Move",move)
        state = stateman.do_move(state, move)
    return state.get_winner()


if __name__ == '__main__':
    print("Simulating HEX")

    size = 2
    num_nodes = size ** 2
    G = 100
    P = "Player 1"
    M = 10
    verbose = False
    write_image = False

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
    mcts = MCTS(statemanager=stateman, initial_state=copy, target_policy=nn_policy, default_policy=nn_policy,
                tree_policy=default_policy,M=M)

    winner = play_game_new(mcts, game.__copy__())
    print("Winnner",winner)
    exit(1)
    save_interval = G / 1
    wins = 0
    losses = 0
    winrate = []

    for i in range(G):
        if i % (G / 10):
            print((i / G) * 100, "% done")

        copy = game.__copy__()
        mcts = MCTS(statemanager=stateman, initial_state=copy, target_policy=nn_policy, default_policy=nn_policy,
                    tree_policy=default_policy
                    , M=M)

        winner = play_game(mcts, initial_player, nn_policy, stateman, [size])
        # mcts.tree.print_entire_tree()
        if verbose:
            print("Winner", winner)
        if winner == initial_player:
            wins += 1
        else:
            losses += 1
        winrate.append(wins / (i + 1))
        if i % save_interval - 1 == 0:
            nn_policy.model.save("networks/mcts" + str(i))

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

    scores = nn_policy.model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (nn_policy.model.metrics_names[1], scores[1] * 100))

    print("Wins", wins)
    print("Losses", losses)
    print("Winrate", wins / G)

    print(nn_policy.model.get_weights())
    test_neural_net(nn_policy, 1000)
