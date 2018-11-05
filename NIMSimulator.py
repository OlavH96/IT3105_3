from Player import *
from NIM import *
import random
from StateManager import *
from MCTS import *
from Policy import *
import matplotlib.pyplot as plt


def play_game(mcts, player):
    start = mcts.tree
    state = start
    game = start.content.__copy__()
    game.player = player
    game.initial_player = player

    history = []
    while not game.isDone():

        choice = mcts.tree_search(state)
        # print("choice is",choice)
        # print(game)
        history.append((game.player, choice))
        game.take(choice.move)  # take real move
        # print(game)

        state = state.getChildByEdge(choice)

        if game.isDone():
            if verbose:
                if game.winner == player:
                    print("Initial Player", player, "won!")
                else:
                    print("Initial Player", player, "lost!")
            break
    if verbose:
        print("History")
        for h in history:
            print(h[0],h[1])
        print("-" * 30)
    return game.winner


if __name__ == '__main__':
    verbose = True
    print_tree = True
    show_winrate_graph = True

    G = 20
    M = 100

    N = 7
    K = 3
    P = "Player 1"

    c = 0 # exploration bonus











    if P == "Player 1":
        init_player = Player.PLAYER_1
    elif P == "Player 2":
        init_player = Player.PLAYER_2
    elif P == "mix":
        init_player = random.choice([Player.PLAYER_1, Player.PLAYER_2])
    else: raise Exception("Invalid Player Choice")

    wins = 0
    losses = 0
    winrate = []
    policy = Policy(init_player, c=c)

    stateman = StateManager()
    game = stateman.generate_initial_state([N, K], player=init_player)


    for i in range(G):

        mcts = MCTS(statemanager=stateman, initial_state=game, policy=policy, default_policy=policy, M=M)

        winner = play_game(mcts, init_player)
        # mcts.tree.print_entire_tree()
        if winner == init_player:
            wins += 1
        else:
            losses += 1
        winrate.append(((wins) /(wins+losses)) * 100)
        if P == "mix" or P == "Mix":
            init_player = random.choice([Player.PLAYER_1, Player.PLAYER_2])

    if print_tree:
        mcts.tree.print_entire_tree()
    if show_winrate_graph:
        plt.plot(winrate)
        plt.xlabel("Games")
        plt.ylabel("Winrate %")
        plt.show()

    print("Wins", wins)
    print("Losses", losses)
    print("Winrate", (wins / G) * 100, "%")
