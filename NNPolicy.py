from HEX import *
from HEXCell import *
import math


class NNPolicy:

    def map_by_player(self, hexcell: HEXCell):
        return Player.to_int(hexcell.player)

    def index_to_value(self, index, original):
        return original[index]

    def cells_to_indices(self, hex_cells: [HEXCell]):
        return list(map(lambda hexcell: int(hexcell.x) + int(math.sqrt(self.num_inputs) * hexcell.y), hex_cells))

    def zero_pad(self, hexcells):
        indices = self.cells_to_indices(hexcells)
        out = [0 for i in range(self.max_num_outputs)]
        for (i, cell) in zip(indices, hexcells):
            out[i] = self.map_by_player(cell)
        return out

    def __hex_to_nn_inputs__(self, hex: HEX):
        cells = hex.__get_all_cells_as_list__()
        mapped = list(map(lambda hexcell: self.map_by_player(hexcell), cells))
        return mapped

    def __init__(self, num_inputs, max_outputs):
        print(num_inputs)
        print(max_outputs)
        self.num_inputs = num_inputs
        self.max_num_outputs = max_outputs
        self.inputs = [0 for i in range(num_inputs)]
        self.outputs = [0 for i in range(max_outputs)]
        print(self.inputs)

    # hex in this case is a "current" state.
    # returns probabilties for every possible move from there
    def chose(self, hex: HEX):
        inputs = self.__hex_to_nn_inputs__(hex)
        possible_moves = hex.get_all_legal_moves()
        mapped = list(map(lambda hexcell: self.map_by_player(hexcell), possible_moves))
        indexes = list(
            map(lambda hexcell: int(hexcell.x) + int(math.sqrt(self.num_inputs) * hexcell.y), possible_moves))
        print(indexes)
        print(possible_moves)
        print(mapped)
        print(inputs)
        print("padded",self.zero_pad(possible_moves))
        ## noe nn greier
        index = mapped.index(max(mapped))
        return self.index_to_value(index, mapped)
