import keras.models
import os

from numpy import mean

import kerasnn.KerasNN
from NNPolicy import *
from HEXSimulator import *
import itertools


def load_policy(path) -> NNPolicy:
    model = keras.models.load_model(path)

    policy = NNPolicy()

    policy.model = model

    return policy


def test_single(path: str, iterations: int, size: int) -> float:
    policy: NNPolicy = load_policy(path)
    return test_neural_net(policy, iterations, size)


def test_folder(folder: str, iterations: int, size: int) -> [float]:
    files = os.listdir(folder)
    winrate: [float] = []
    best = (files[0], 0)
    for file in sorted(files):
        path = os.path.join(folder, file)

        policy: NNPolicy = load_policy(path)

        wr = test_neural_net(policy, iterations, size)
        if wr > best[1]:
            best = (file, wr)
        print(file, "tested", iterations, "times, winrate", wr)
        winrate.append(wr)

    print("Best Winrate", best[0], best[1])
    return winrate, best[0]


def TOPP(folder, file1, file2, size, num_games):
    path1 = os.path.join(folder, file1)
    path2 = os.path.join(folder, file2)
    policy1: NNPolicy = load_policy(path1)
    policy2: NNPolicy = load_policy(path2)

    return test_TOPP(policy1, policy2, size, num_games)


def best_fit_slope_and_intercept(xs, ys):
    xs = np.array(xs)
    ys = np.array(ys)
    m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
         ((mean(xs) * mean(xs)) - mean(xs * xs)))

    b = mean(ys) - m * mean(xs)

    return m, b

def TOPP_tournement_folder(files, size, num_games):
    files = sorted(files)
    policies = {file: None for file in files}
    for file in files:
        path = os.path.join(folder, file)
        policy: NNPolicy = load_policy(path)
        policies[file] = policy

    # winratemap = [(file, [(file1,0) for file1 in files]) for file in files]
    winratemap = {file: {file1: 0.5 for file1 in files} for file in files}
    combinations = itertools.combinations(list(policies.keys()), 2)
    for file1, file2 in combinations:
        p1 = policies[file1]
        p2 = policies[file2]
        print(file1, "VS", file2)
        wr1, wr2 = test_TOPP(p1, p2, size, num_games)
        # wr1, wr2 = TOPP(folder, file1, file2, size, num_games)
        # print(file1, "winrate", wr1)
        # print(file2, "winrate", wr2)
        winratemap[file1][file2] = wr1
        winratemap[file2][file1] = wr2

        print()
    print(winratemap)
    for file in winratemap.keys():
        print("***", file, "***")
        wrs = winratemap[file]
        for wr in wrs:
            if wr != file:
                print(wr, "\t:", winratemap[file][wr])
        print()
    data = []
    for file in winratemap.keys():
        wrs = list(winratemap[file].values())
        data.append(wrs)

    for d in data:
        x = list(range(0, len(files)))
        y=d
        m, b = best_fit_slope_and_intercept(x, y)

        regression_line = [(m * xs) + b for xs in x]
        plt.scatter(x=x,y=y)
        plt.plot(x,regression_line)
    plt.legend([x for x in winratemap.keys()], loc="upper left", bbox_to_anchor=(1,1))
    plt.show()


if __name__ == '__main__':
    games = 1000
    size = 5
    plot_winrate = False

    folder = "networks/size" + str(size)+ "_1000_100"
    files = os.listdir(folder)
    files = list(filter(lambda file: os.path.isfile(os.path.join(folder,file)),files))
    print(files)

    TOPP_tournement_folder(files, size, 100)

    # exit(1)
    # wr1, wr2 = TOPP(folder, "mcts5_1000_100_600", "mcts5_1000_100_0", size, 1)
    # print("mcts5_1000_100_600 wr:", wr1)
    # print("mcts5_1000_100_0 wr:", wr2)
    # exit(1)
    # winrate, best_file = test_folder(folder, games, size)
    #
    # best_result = test_single(os.path.join(folder, best_file), games, size)
    # print(best_file, "gets", best_result, "winrate")
    #
    # if plot_winrate:
    #     plt.plot(winrate)
    #     plt.xlabel("Neural Net")
    #     plt.ylabel("Winrate")
    #     plt.show()
