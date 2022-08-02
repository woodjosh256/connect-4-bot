from copy import deepcopy
from dataclasses import dataclass

from game.game import Game, WinStates, ChipColors
from game.playable import Playable
from terminalrunner.outputter import Outputter
from terminalrunner.playables.randombot import RandomBot


class MatchStats:

    def __init__(self):
        self.black_win_count: int = 0
        self.red_win_count: int = 0
        self.tie_count: int = 0
        self.game_count: int = 0

    def __str__(self):
        return f"Red: {self.red_win_count} Black: {self.black_win_count} " \
               f"Tie: {self.tie_count}"

    def add_round(self, win_state: WinStates):
        match win_state:
            case WinStates.RED:
                self.red_win_count += 1
            case WinStates.BLACK:
                self.black_win_count += 1
            case WinStates.TIE:
                self.tie_count += 1
        self.game_count += 1

    def get_win_state_percentage(self, win_state: WinStates):
        match win_state:
            case WinStates.RED:
                return self.red_win_count / self.game_count
            case WinStates.BLACK:
                return self.black_win_count / self.game_count
            case WinStates.TIE:
                return self.tie_count / self.game_count


class Runner:

    playables = [RandomBot]

    # todo - add turn time limit

    @staticmethod
    def run_round(playable1: Playable, playable2: Playable,
                  output_turns: bool = True,
                  output_wins: bool = True) -> WinStates:
        game = Game()
        outputter = Outputter()
        turn = 0

        while game.get_win_state() is None:
            state = deepcopy(game.state)
            moves = deepcopy(game.moves)
            if turn % 2 == 0:
                move = playable1.move(state, game.open_columns(), moves)
                game.insert_chip(playable1.color, move)
            else:
                move = playable2.move(state, game.open_columns(), moves)
                game.insert_chip(playable2.color, move)

            if output_turns:
                outputter.output_board(game.state)

            turn += 1

        win_state = game.get_win_state()

        if output_wins:
            outputter.output_board(game.state)
            outputter.output_results(win_state)

        return win_state

    @staticmethod
    def run_match(playable1: Playable, playable2: Playable, rounds: int = 100,
                  output_turns: bool = True,
                  output_wins: bool = True) -> MatchStats:
        match_stats = MatchStats()

        for i in range(rounds):
            win_state = Runner.run_round(playable1, playable2, output_turns,
                                         output_wins)
            match_stats.add_round(win_state)

        return match_stats
