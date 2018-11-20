import TrainingCase
import random


class ReplayBuffer:

    def __init__(self):
        self.buffer: [TrainingCase] = []

    def add(self, training_case: TrainingCase) -> None:
        self.buffer.append(training_case)

    def get_minibatch(self, size: int) -> [TrainingCase]:
        random.shuffle(self.buffer)
        return self.buffer[:size]

    def clear(self):
        self.buffer = []
