import numpy as np

from HEX import *
from HEXCell import *
import math
from kerasnn.KerasConfig import *
from kerasnn.KerasNN import *


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

    def __init__(self, keras_config: KerasConfig):
        self.config: KerasConfig = keras_config
        self.nn: KerasNN = KerasNN(keras_config)
        self.model: Model = self.nn.build()

    # hex in this case is a "current" state.
    # returns probabilties for every possible move from there
    def chose(self, hex: HEX, actions=None, init_player=None):
        possible_moves = hex.get_all_legal_moves()

        model: Model = self.model
        inputs = self.__hex_to_nn_inputs__(hex)
        inputs = [[inputs]]

        prediction = model.predict(inputs)
        prediction = prediction.tolist()[0]
        prediction = [(i,v) for (i,v) in enumerate(prediction)]
        prediction.sort(key=lambda x:x[1], reverse=True)
        for (index, value) in prediction:
            if index < len(possible_moves):
                return possible_moves[index]