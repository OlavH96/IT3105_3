from HEX import HEX
from Player import Player


class TrainingCase:

    def __init__(self, feature_set: [float], target_distribution: [float], PID: int):
        self.feature_set: [float] = feature_set
        self.target_distribution: [float] = target_distribution
        self.PID: int = PID

    def F(self) -> [float]:
        return self.feature_set + [float(self.PID)]

    def D(self) -> [float]:
        return self.target_distribution


def __hex_to_nn_inputs__(hex: HEX):
    cells = hex.__get_all_cells_as_list__()
    mapped = list(map(lambda hexcell: Player.to_int(hexcell.player), cells))
    return mapped


def __create_training_case__(hex_state, distribution):
    inputs = __hex_to_nn_inputs__(hex_state)
    dist = [v for d, v in distribution]
    PID = Player.to_int(hex_state.player)
    # print(inputs)
    # print(dist)
    dist = [dist.pop(0) if d == 0 else 0 for i, d in enumerate(inputs)]
    # print(dist)
    # inputs = [[inputs]]
    return TrainingCase(inputs, dist, PID)
