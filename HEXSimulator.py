from HEX import *
from HEXCell import *
from Player import *
import HEXDrawer

if __name__ == '__main__':


    print("Simulating HEX")

    game = HEX(4,4, Player.PLAYER_1)

    board = game.board

    # print(game.is_valid_move(0, 0))
    # for row in board:
    #     print(row)
    # print(game.get_cell(0,0).neighbours)
    # for c in board[0]:
    #     c.player = Player.PLAYER_1
    # for c in board[3]:
    #     c.player = Player.PLAYER_1
    var = board[0][0]
    var.player = Player.PLAYER_1
    # for n in var.neighbours:
    #     n.player = Player.PLAYER_2

    HEXDrawer.graph(board)

    #print(game.get_legal_moves(0,0))



    # print(game.get_legal_moves(0, 0))
    # print(game.get_legal_moves(1, 1))
    # print(game.get_legal_moves(3, 3))