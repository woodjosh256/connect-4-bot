from enum import Enum
from typing import List

from game.chipcolors import ChipColors


class Game:

    ROWS = 6
    COLUMNS = 7
    WINNING_NUMBER = 4

    class WinStates(Enum):
        RED = 0
        BLACK = 1
        TIE = 2

    def __init__(self) -> None:
        self.board_state = [[None] * self.COLUMNS for i in range(self.ROWS)]
        self.win_state = None

    def insert_chip(self, chip: ChipColors, col: int) -> WinStates:
        if col not in self._open_columns():
            raise ValueError("Invalid column")

        row = 0
        while row < self.ROWS - 1 and self.board_state[row + 1][col] is None:
            row += 1

        self.board_state[row][col] = chip

        self._update_win_state(row, col)
        return self.win_state

    def _open_columns(self) -> List[int]:
        # todo actually implement
        return [i for i in range(self.COLUMNS)]

    def _update_win_state(self, last_row: int, last_col: int):
        pass
