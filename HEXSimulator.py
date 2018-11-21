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
        # Randomize start
        game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))
        game_copy.do_move_from_cell(random.choice(game_copy.get_all_legal_moves()))

        while not game_copy.is_done():
            action = nn_policy.chose(game_copy, game_copy.get_all_legal_moves())
            game_copy.do_move_from_cell(action)

        if game_copy.get_winner() == Player.PLAYER_1:
            wins += 1
        else:
            losses += 1

    print("Tested Neural network", num_games, "times, winrate:", (wins / num_games) * 100, "%")


def play_game(mcts, nn_policy: NNPolicy):
    if verbose:
        print("Playing game")

    start: Node = mcts.tree
    state: Node = start

    while not stateman.is_final_state(state.content):
        edge: Edge = mcts.pick_action(state, replay_buffer)
        move: Move = edge.content

        if verbose:
            print("Chose Move", move.move, "by player", state.content.player)

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

    size = 4
    G = 10
    P = "Player 1"
    M = 20
    verbose = False
    write_image = False
    save_networks = False
    save_networks_interval = G / 10
    plot_winrate = False
    debug = False

    num_nodes = size ** 2
    config: KerasConfig = KerasConfig(ndim=[num_nodes + 1, num_nodes * 2, num_nodes],
                                      oaf="sigmoid", haf="tanh",
                                      optimizer="adam", lr=0.01)
    initial_player = Player.player_from_string(P)

    policy = Policy(initial_player)  # same as from last assignment
    nn_policy = NNPolicy(config)

    stateman = HEXStateManager()
    game: HEX = stateman.generate_initial_state([size], player=initial_player)

    replay_buffer: ReplayBuffer = ReplayBuffer()

    wins = 0
    losses = 0
    winrate = []

    for i in range(G):
        if i % (G / 10) == 0 and not verbose:
            print((i / G) * 100, "%", "done")

        mcts = MCTS(statemanager=stateman, initial_state=game.__copy__(), target_policy=nn_policy,
                    default_policy=nn_policy,
                    tree_policy=policy, M=M)

        winner = play_game(mcts, nn_policy)
        if i != G - 1:
            replay_buffer.clear()
        if winner == initial_player:
            wins += 1
        else:
            losses += 1
        winrate.append(wins / (i + 1))

        if i % (save_networks_interval) == 0 or i == G - 1 and save_networks:
            ## save net for tournement
            nn_policy.model.save("networks/mcts" + str(i))
            pass

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

        training_cases = replay_buffer.get_minibatch(1000000)
        X = [t.F() for t in training_cases]
        Y = [t.D() for t in training_cases]
        X = np.array(X)
        Y = np.array(Y)
        Y = np.interp(Y, (0, Y.max()), (0, 1))

        scores = nn_policy.model.evaluate(X, Y)
        print("\n%s: %.2f%%" % (nn_policy.model.metrics_names[1], scores[1] * 100))

    test_neural_net(nn_policy, 1000)
    time_end = time.time()
    print("Took:", time_end - time_start, " seconds")
