import random

from HEX import *
from HEXCell import *
from Player import *
import HEXDrawer
import time

if __name__ == '__main__':

    print("Simulating HEX")

    size = 4

    game = HEX(size, Player.PLAYER_1)

    game.__graph_current_state__()

    for i in range(size):
        game.get_cell(3,i).player = Player.PLAYER_2
        game.__graph_current_state__()
    print(game.is_done())

    # while not game.is_done():
    #     print(game.is_done())
    #     choices = game.__get_all_nodes_as_list__()
    #     valid = list(filter(lambda cell: game.is_valid_move_cell(cell), choices))
    #     choice = random.choice(valid)
    #     game.do_move_from_cell(choice)
    #     game.__graph_current_state__()

    game.__graph_current_state__()
