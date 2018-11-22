import numpy as np

from HEX import *
from HEXCell import *
import math

from Move import Move
from Node import Node
from TrainingCase import TrainingCase
from kerasnn.KerasConfig import *
from kerasnn.KerasNN import *

from sklearn.preprocessing import scale

class NNPolicy:

    def map_by_player(self, hexcell: HEXCell):
        return Player.to_int(hexcell.player)

    def index_to_value(self, index, original):
        return original[index]

    # def cells_to_indices(self, hex_cells: [HEXCell]):
    #     return list(map(lambda hexcell: int(hexcell.x) + int(math.sqrt(self.num_inputs) * hexcell.y), hex_cells))
    #
    # def zero_pad(self, hexcells):
    #     indices = self.cells_to_indices(hexcells)
    #     out = [0 for i in range(self.max_num_outputs)]
    #     for (i, cell) in zip(indices, hexcells):
    #         out[i] = self.map_by_player(cell)
    #     return out

    def __hex_to_nn_inputs__(self, hex: HEX):
        cells = hex.__get_all_cells_as_list__()
        mapped = list(map(lambda hexcell: self.map_by_player(hexcell), cells))
        return mapped

    def __init__(self, keras_config: KerasConfig=None):
        if keras_config:
            self.config: KerasConfig = keras_config
            self.nn: KerasNN = KerasNN(keras_config)
            self.model: Model = self.nn.build()

    # hex in this case is a "current" state.
    # returns probabilties for every possible move from there
    def chose(self, node: Node, actions=None, init_player=None, player=None) -> Move:
        if hasattr(node, "content"):
            hex: HEX = node.content
        else:
            hex: HEX = node
        # possible_moves = hex.get_all_legal_moves()

        model: Model = self.model
        inputs = self.__hex_to_nn_inputs__(hex)
        inputs = [[inputs + [Player.to_int(hex.player)]]]

        prediction = model.predict(inputs)
        prediction = prediction.tolist()[0]
        prediction = [(i, v) for (i, v) in enumerate(prediction)]
        prediction.sort(key=lambda x: x[1], reverse=True)
        for (index, value) in prediction:
            if index < len(actions):
                return actions[index]
        print("None found")
        print(prediction)
        print(inputs)

    def train(self, training_cases: [TrainingCase]):
        X = [t.F() for t in training_cases]
        Y = [t.D() for t in training_cases]
        X = np.array(X)
        Y = np.array(Y)
        # print("X",X)
        # print("Y",Y)
        # print(len(Y))
        if len(Y) > 1:
            Y = np.interp(Y, (0, Y.max()), (0, 1))
            # print("Interp",Y)
        #print(Y)
            self.model.fit(x=X, y=Y, epochs=100, verbose=0)

    def __create_training_case__(self, hex_state, distribution):
        inputs = self.__hex_to_nn_inputs__(hex_state)
        dist = [v for d, v in distribution]
        PID = Player.to_int(hex_state)
        #print(inputs)
        #print(dist)
        dist = [dist.pop(0) if d == 0 else 0 for i,d in enumerate(inputs)]
        #print(dist)
        # inputs = [[inputs]]
        return TrainingCase(inputs, dist, PID)
