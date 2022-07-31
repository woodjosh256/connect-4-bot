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

        self.last_row = None
        self.last_col = None
        self.last_color = None

    def insert_chip(self, chip: ChipColors, col: int) -> None:
        if col not in self._open_columns():
            raise ValueError("Invalid column")

        row = 0
        while row < self.ROWS - 1 and self.board_state[row + 1][col] is None:
            row += 1

        self.board_state[row][col] = chip

        self.last_row = row
        self.last_col = col
        self.last_color = ChipColors

    def _open_columns(self) -> List[int]:
        # todo actually implement
        return [i for i in range(self.COLUMNS)]

    def get_win_state(self) -> WinStates:
        h_win = self.check_horiz_win()
        if h_win:
            return h_win

        v_win = self.check_vert_win()
        if v_win:
            return v_win

        d_win = self.check_diagonal_win()
        if d_win:
            return d_win

    def check_horiz_win(self) -> WinStates:
        row = self.last_row
        col = self.last_col

        while col > 0 and self.board_state[row][col - 1] == self.last_color:


    def check_vert_win(self) -> WinStates:
        pass

    def check_diagonal_win(self) -> WinStates:
        pass