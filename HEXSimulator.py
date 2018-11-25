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
import TOPP


def test_TOPP(policy_1: NNPolicy, policy_2: NNPolicy, size: int, num_games: int, verbose=False):
    if verbose:
        print("TOPP")
        print("Policy 1", policy_1)
        print("Policy 2", policy_2)
    game = HEX(size, Player.PLAYER_1)
    wins_1 = 0
    wins_2 = 0

    for _ in range(num_games):
        if verbose:
            print("Game", _)
        game_copy = game.__copy__()
        # game_copy.do_move_from_cell(random.choice(game.get_all_legal_moves()))
        policy = random.choice([policy_1, policy_2])

        while not game_copy.is_done():
            cell: HEXCell = policy.chose(game_copy, game_copy.get_all_legal_moves(), Player.PLAYER_1, game_copy.player)
            if verbose:
                print("Move", cell, "by policy", policy)
            game_copy.do_move_from_cell(cell)

            if policy == policy_1:
                policy = policy_2
            else:
                policy = policy_1

        if policy == policy_1:
            wp = policy_2
            wins_2 += 1
        else:
            wp = policy_1
            wins_1 += 1
        if verbose:
            print("Winning policy", wp)

        # winner = game_copy.get_winner()
        # print(winner)
        # if winner == Player.PLAYER_1:  # policy 1 won
        #     wins_1 += 1
        # else:
        #     wins_2 += 1
    if verbose:
        print("Finished TOPP")
        print("Policy 1 won ", wins_1, "/", num_games)
        print("Policy 2 won ", wins_2, "/", num_games)
        print("Policy 1 winrate", wins_1 / num_games)
        print("Policy 2 winrate", wins_2 / num_games)

    return wins_1 / num_games, wins_2 / num_games


def test_neural_net(nn_policy: NNPolicy, num_games: int, size):
    game = HEX(size, Player.PLAYER_1)
    wins = 0

    for i in range(num_games):

        game_copy = game.__copy__()
        # Randomize start
        # game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))
        # game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))

        while not game_copy.is_done():
            action = nn_policy.chose(game_copy, game_copy.get_all_legal_moves())
            game_copy.do_move_from_cell(action)

            if game_copy.is_done(): break

            game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))

        if game_copy.get_winner() == Player.PLAYER_1:
            wins += 1

    # print("Tested Neural network", num_games, "times, winrate:", (wins / num_games) * 100, "%")
    return wins / num_games


def play_game(mcts, nn_policy: NNPolicy):
    if verbose:
        print("Playing game", i, "/", G)

    start: Node = mcts.tree
    state: Node = start
    if write_image:
        state.content.__graph_current_state__()

    while not stateman.is_final_state(state.content):
        edge: Edge = mcts.pick_action(state, replay_buffer)
        move: Move = edge.content

        if verbose:
            print("Chose Move", move.move, "by player", state.content.player)
        if graph_every_move[0]:
            state.content.__graph_current_state__()
            time.sleep(graph_every_move[1])
        state = edge.toNode
    if debug:
        print(len(replay_buffer.buffer))
        for tc in replay_buffer.get_minibatch(100):
            print(tc.F())
            print(tc.D())
    nn_policy.train(replay_buffer.get_minibatch(10))

    if write_image:
        state.content.__graph_current_state__()
    return state.content.get_winner()


if __name__ == '__main__':
    print("Simulating HEX")
    time_start = time.time()

    size = 5  # size of game board
    G = 15  # episodes
    P = "Player 1"
    M = 10  # number of search games
    K = 3
    verbose = True
    write_image = True
    graph_every_move = (True, 0.1)  # sleep time
    save_networks = True
    plot_winrate = False
    debug = False

    save_networks_interval = G / K  # 'is'
    num_nodes = size ** 2
    config: KerasConfig = KerasConfig(ndim=[num_nodes + 1, 100, 100, num_nodes],
                                      oaf="softmax", haf="tanh",  # haf relu, oaf softmax
                                      optimizer="rmsprop", lr=0.1)

    replay_buffer: ReplayBuffer = ReplayBuffer()

    initial_player = Player.player_from_string(P)

    policy = Policy(initial_player)  # same as from last assignment
    nn_policy = NNPolicy(config)

    stateman = HEXStateManager()
    game: HEX = stateman.generate_initial_state([size], player=initial_player)

    wins = 0
    losses = 0
    winrate = []

    for i in range(G):  # actual games
        if i == 0 and save_networks:
            nn_policy.model.save("networks/mcts" + str(size) + "_" + str(G) + "_" + str(M) + "_" + str(i))

        if i % (G / 10) == 0 and not verbose:
            print((i / G) * 100, "%", "done")

        mcts = MCTS(statemanager=stateman, initial_state=game.__copy__(),
                    target_policy=nn_policy,
                    default_policy=nn_policy,
                    tree_policy=policy, M=M)

        winner = play_game(mcts, nn_policy)
        if verbose:
            print("Winner:", winner)
        if i != G - 1:
            replay_buffer.clear()
        if winner == initial_player:
            wins += 1
        else:
            losses += 1
        winrate.append(wins / (i + 1))

        if ((i % (save_networks_interval) == 0 and i != 0) or i == G - 1) and save_networks:
            ## save net for tournement
            nn_policy.model.save("networks/mcts" + str(size) + "_" + str(G) + "_" + str(M) + "_" + str(i))

        if P == "mix":
            rand = Player.player_from_string(P)
            game.initial_player = rand  # random if "mix"
            game.player = rand  # random if "mix"
            initial_player = rand

    print("Wins", wins)
    print("Losses", losses)
    print("Winrate", (wins / G) * 100, " %")
    if plot_winrate:
        plt.plot(winrate)
        plt.xlabel("Game")
        plt.ylabel("Winrate")
        plt.show()

    if debug:
        print(nn_policy.model.get_weights())
    # Test accuracy of network
    training_cases = replay_buffer.get_minibatch(1000000)
    X = [t.F() for t in training_cases]
    Y = [t.D() for t in training_cases]
    X = np.array(X)
    Y = np.array(Y)
    Y = np.interp(Y, (0, Y.max()), (0, 1))

    scores = nn_policy.model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (nn_policy.model.metrics_names[1], scores[1] * 100))
    # Test vs random player
    wr = test_neural_net(nn_policy, 1000, size)
    print("Winrate vs random player: ", wr)
    time_end = time.time()
    print("Took:", time_end - time_start, " seconds")
