from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

import numpy as np
from numpy import int8
from numpy.typing import ArrayLike
from scipy.signal import convolve2d

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.move import Move
from connect4.winstates import WinStates


@dataclass
class FastGameState:
    rows: int
    columns: int
    winning_number: int
    state: ArrayLike[ArrayLike[int8]]
    chips_per_col: ArrayLike[int8]
    moves: List[Move]

    @staticmethod
    def int_to_chip(val: int) -> ChipColors:
        if val == ChipColors.RED.value:
            return ChipColors.RED
        elif val == ChipColors.BLACK.value:
            return ChipColors.BLACK

    @staticmethod
    def new_game(rows: int, columns: int, winning_number: int) -> FastGameState:
        return FastGameState(
            rows=rows,
            columns=columns,
            winning_number=winning_number,
            state=np.zeros(shape=(rows, columns), dtype=int8),
            chips_per_col=np.zeros(shape=columns, dtype=int8),
            moves=[],
        )

    @staticmethod
    def from_gamestate(gamestate: GameState) -> FastGameState:
        chips_per_col = [0] * gamestate.columns
        updated_state = [[0] * gamestate.columns for i in range(gamestate.rows)]
        for col in range(gamestate.columns):
            total = 0
            for row in range(gamestate.rows):
                if gamestate.state[row][col] is not None:
                    updated_state[row][col] = gamestate.state[row][col].value
                    total += 1

            chips_per_col[col] = total

        return FastGameState(
            rows=gamestate.rows,
            columns=gamestate.columns,
            winning_number=gamestate.winning_number,
            state=np.array(updated_state, dtype=int8),
            chips_per_col=np.array(chips_per_col, dtype=int8),
            moves=list(gamestate.moves),
        )

    @staticmethod
    def find_first_nonzero(arr: np.ndarray[int8]):
        """
        :param arr: numpy array to search
        :return: index of the first non-zero element
        """
        idx = arr.view(bool).argmax() // arr.itemsize
        return idx - 1 if arr[idx] else -1

    def open_columns(self) -> ArrayLike[int]:
        return np.where(self.chips_per_col < self.rows)[0]

    def drop_chip(self, color: ChipColors, col: int):
        if self.chips_per_col[col] == 0:
            row = self.rows - 1
        else:
            selected_col = self.state[:, col]
            row = self.find_first_nonzero(selected_col)
        self.state[row, col] = color.value
        self.chips_per_col[col] += 1
        self.moves.append(Move(row, col, color))

    def undo_last_move(self, num: int = 1):
        for i in range(num):
            move = self.moves.pop()
            self.state[move.row, move.col] = 0
            self.chips_per_col[move.col] -= 1

    def get_win_state(self) -> Optional[WinStates]:
        if not self.moves:
            return None

        return self._move_winstate(self.moves[-1])

    def _move_winstate(self, move: Move) -> Optional[WinStates]:
        """

        :param move:
        :return:
        """
        if self.open_columns()[0].shape == (0,):
            return WinStates.TIE
        elif (self.horiz_dist(move) >= self.winning_number
              or self.vert_dist(move) >= self.winning_number
              or self.incline_diagonal_dist(move) >= self.winning_number
              or self.decline_diagonal_dist(move) >= self.winning_number):
            return move.color.to_win_state()

        return None

    def horiz_dist(self, move: Move) -> int:
        last_row = move.row
        min_col = max_col = move.col
        last_color = move.color.value

        while (min_col > 0
               and self.state[last_row, min_col - 1] == last_color):
            min_col -= 1
        while (max_col < self.columns - 1
               and self.state[last_row, max_col + 1] == last_color):
            max_col += 1

        return max_col - min_col + 1

    def vert_dist(self, move: Move) -> int:
        min_row = max_row = move.row
        last_col = move.col
        last_color: int = move.color.value

        while (min_row > 0
               and self.state[min_row - 1, last_col] == last_color):
            min_row -= 1
        while (max_row < self.rows - 1
               and self.state[max_row + 1, last_col] == last_color):
            max_row += 1

        return max_row - min_row + 1

    def incline_diagonal_dist(self, move: Move) -> int:
        min_row = max_row = move.row
        min_col = max_col = move.col
        last_color = move.color.value

        while (max_row < self.rows - 1 and min_col > 0
               and self.state[max_row + 1, min_col - 1] == last_color):
            max_row += 1
            min_col -= 1
        while (min_row > 0 and max_col < self.columns - 1
               and self.state[min_row - 1, max_col + 1] == last_color):
            min_row -= 1
            max_col += 1

        return max_row - min_row + 1

    def decline_diagonal_dist(self, move: Move) -> int:
        min_row = max_row = move.row
        min_col = max_col = move.col
        last_color = move.color.value

        while (min_row > 0 and min_col > 0
               and self.state[min_row - 1, min_col - 1] == last_color):
            min_row -= 1
            min_col -= 1
        while (max_row < self.rows - 1 and max_col < self.columns - 1
               and self.state[max_row + 1, max_col + 1] == last_color):
            max_row += 1
            max_col += 1

        return max_row - min_row + 1




