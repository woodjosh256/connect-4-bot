from copy import deepcopy

from game.game import Game, WinStates
from game.playable import Playable
from terminalrunner.outputter import Outputter
from terminalrunner.playables.randombot import RandomBot


class Runner:

    playables = [RandomBot]

    # todo - add turn time limit

    @staticmethod
    def run_match(playable1: Playable, playable2: Playable):
        game = Game()
        outputter = Outputter()
        turn = 0

        while game.get_win_state() is None:
            state = deepcopy(game.state)
            if turn % 2 == 0:
                move = playable1.move(state, game.open_columns())
                game.insert_chip(playable1.color, move)
            else:
                move = playable2.move(state, game.open_columns())
                game.insert_chip(playable2.color, move)

            outputter.output_board(game.state)

            turn += 1

        outputter.output_board(game.state)
        outputter.output_results(game.get_win_state())

    @staticmethod
    def benchmark(playable1: Playable, playable2: Playable, rounds: int = 100,
                  show_turns: bool = True):
        # todo - add code for calculating stats, add option for hiding turns

        for i in range(rounds):
            Runner.run_match(playable1, playable2)
