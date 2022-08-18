from math import inf
import random
from typing import Dict, List
from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.game import Game
import numpy as np
from playables.joshw.minimaxwithcaching import MinimaxWithCaching
from playables.joshw.MutableGameState import FastMove
from playables.transpositiontable import TranspositionTable


class BenMBot(MinimaxWithCaching):
    INFINITY = float(inf)
    DEPTH = 5
    MAX_SORT_DEPTH = 3
    EMPTY = 0
    WINDOW_LENGTH = 4

    def __init__(self, color: ChipColors):
        super().__init__(color)
        self.random = random.Random(42069)
        self.maximising = self.COLOR_MAP[self.color]
        self.transposition_table = TranspositionTable()
        self.starting = None

    @classmethod
    def get_name(cls) -> str:
        return "BenM Bot"

    @classmethod
    def _static_eval(self, game_state: GameState, last_move: FastMove) -> float:
        win_state = game_state.get_win_state(last_move)
        if win_state == self.MAXIMISING_COLOR.to_win_state():
            return self.INFINITY
        elif win_state == self.MINIMISING_COLOR.to_win_state():
            return -self.INFINITY
        else:
            return self.score_position(game_state, self.MAXIMISING_COLOR)

    @classmethod
    def evaluate_window(self, window, color_val: int) -> int:
        score = 0
        opposing_color_val = (color_val % 2) + 1

        if window.count(color_val) == 4:
            score += 100
        elif window.count(color_val) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(color_val) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opposing_color_val) == 3 and window.count(self.EMPTY) == 1:
            score -= 4
        elif window.count(opposing_color_val) == 2 and window.count(self.EMPTY) == 2:
            score -= 1

        return score

    @classmethod
    def score_position(self, game_state: GameState, color: ChipColors):
        score = 0
        game_state_arr = np.asarray(game_state.state)
        game_state_arr[game_state_arr == None] = 0
        game_state_arr[game_state_arr ==
                       ChipColors.BLACK] = ChipColors.BLACK.value
        game_state_arr[game_state_arr == ChipColors.RED] = ChipColors.RED.value
        color_val = color.value

        # Score center column
        center_array = [int(i)
                        for i in list(game_state_arr[:, Game.ROWS//2])]
        center_count = center_array.count(color_val)
        score += center_count * 3

        # Score Horizontal
        for r in range(Game.ROWS):
            row_array = [int(i)
                         for i in list(game_state_arr[r, :])]
            for c in range(Game.COLUMNS-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, color_val)

        # Score Vertical
        for c in range(Game.COLUMNS):
            col_array = [int(i)
                         for i in list(game_state_arr[:, c])]
            for r in range(Game.ROWS-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, color_val)

        # Score Diagonal
        for r in range(Game.ROWS-3):
            for c in range(Game.COLUMNS-3):
                window = [game_state_arr[r+i][c+i]
                          for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, color_val)
                window = [game_state_arr[r+3-i][c+i]
                          for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, color_val)

        return score
