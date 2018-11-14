import random

class RandomPolicy:

    def __init__(self):
        pass

    def chose(self, cell, actions, initial_player):

        return random.choice(actions)