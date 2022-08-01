from game.game import Game, ChipColors
from terminalrunner.outputable import Outputable


def test(color, pos, game, outputable):
    game.insert_chip(color, pos)
    outputable.output_board(game.chip_state)
    print(game.get_win_state())


if __name__ == '__main__':
    outputable = Outputable()
    game = Game()

    test(ChipColors.RED, 0, game, outputable)
    test(ChipColors.RED, 1, game, outputable)
    test(ChipColors.RED, 1, game, outputable)
    test(ChipColors.BLACK, 2, game, outputable)
    test(ChipColors.RED, 2, game, outputable)
    test(ChipColors.RED, 2, game, outputable)
    test(ChipColors.RED, 3, game, outputable)

    test(ChipColors.RED, 3, game, outputable)
    test(ChipColors.RED, 3, game, outputable)
    test(ChipColors.RED, 3, game, outputable)
    test(ChipColors.RED, 4, game, outputable)

    test(ChipColors.BLACK, 9, game, outputable)
    test(ChipColors.BLACK, 8, game, outputable)
    test(ChipColors.BLACK, 8, game, outputable)
    test(ChipColors.BLACK, 7, game, outputable)
    test(ChipColors.BLACK, 7, game, outputable)
    test(ChipColors.BLACK, 7, game, outputable)
    test(ChipColors.BLACK, 6, game, outputable)
    test(ChipColors.BLACK, 6, game, outputable)
    test(ChipColors.BLACK, 6, game, outputable)
    test(ChipColors.BLACK, 6, game, outputable)
