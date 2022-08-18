from math import inf
from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.game import Game
from playables.joshw.minimax import Minimax
import numpy as np


class BenMMiniMax(Minimax):
    INFINITY = float(inf)
    DEPTH = 4
    EMPTY = 0
    WINDOW_LENGTH = 4

    @classmethod
    def get_name(cls) -> str:
        return "BenM Minimax"

    @classmethod
    def _static_eval(cls, game_state: GameState) -> float:
        win_state = game_state.get_win_state()
        if win_state == cls.MAXIMISING_COLOR.to_win_state():
            return cls.INFINITY
        elif win_state == cls.MINIMISING_COLOR.to_win_state():
            return -cls.INFINITY
        else:
            return cls.score_position(game_state, cls.MAXIMISING_COLOR)

    @classmethod
    def evaluate_window(cls, window, color_val: int) -> int:
        score = 0
        opposing_color_val = (color_val % 2) + 1

        if window.count(color_val) == 4:
            score += 100
        elif window.count(color_val) == 3 and window.count(cls.EMPTY) == 1:
            score += 5
        elif window.count(color_val) == 2 and window.count(cls.EMPTY) == 2:
            score += 2

        if window.count(opposing_color_val) == 3 and window.count(cls.EMPTY) == 1:
            score -= 4
        elif window.count(opposing_color_val) == 2 and window.count(cls.EMPTY) == 2:
            score -= 1

        return score

    @classmethod
    def score_position(cls, game_state: GameState, color: ChipColors):
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
                window = row_array[c:c+cls.WINDOW_LENGTH]
                score += cls.evaluate_window(window, color_val)

        # Score Vertical
        for c in range(Game.COLUMNS):
            col_array = [int(i)
                         for i in list(game_state_arr[:, c])]
            for r in range(Game.ROWS-3):
                window = col_array[r:r+cls.WINDOW_LENGTH]
                score += cls.evaluate_window(window, color_val)

        # Score Diagonal
        for r in range(Game.ROWS-3):
            for c in range(Game.COLUMNS-3):
                window = [game_state_arr[r+i][c+i]
                          for i in range(cls.WINDOW_LENGTH)]
                score += cls.evaluate_window(window, color_val)
                window = [game_state_arr[r+3-i][c+i]
                          for i in range(cls.WINDOW_LENGTH)]
                score += cls.evaluate_window(window, color_val)

        return score
