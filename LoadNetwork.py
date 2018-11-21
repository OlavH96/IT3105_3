import keras.models
import os
import kerasnn.KerasNN
from NNPolicy import *

def load_policy(path) -> NNPolicy:

    model = keras.models.load_model(path)

    policy = NNPolicy()

    policy.model = model

    return policy


if __name__ == '__main__':
    folder = "networks/"
    network_to_load = "mcts999"
    path = os.path.join(folder, network_to_load)

    policy: NNPolicy = load_policy(path)
    print(policy)
