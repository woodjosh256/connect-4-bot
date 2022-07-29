from game.chipcolors import ChipColors
from game.game import Game
from game.outputable import Outputable

if __name__ == '__main__':
    outputable = Outputable()
    game = Game()
    game.insert_chip(ChipColors.RED, 0)
    game.insert_chip(ChipColors.BLACK, 0)
    game.insert_chip(ChipColors.RED, 0)
    game.insert_chip(ChipColors.BLACK, 6)

    outputable.output_board(game.board_state)
