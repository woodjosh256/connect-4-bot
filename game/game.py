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
        open_cols = self.open_columns()

        if col not in open_cols:
            raise ValueError("Invalid column")

        row = 0
        while row < self.ROWS - 1 and self.board_state[row + 1][col] is None:
            row += 1

        self.board_state[row][col] = chip

        if(self.board_state[0][col] is not None):
            open_cols.remove(col)
        if self.win_state is None and len(open_cols) == 0:
            self.win_state = self.WinStates.TIE
            return self.win_state

        self._update_win_state(row, col)
        return self.win_state

    def open_columns(self) -> List[int]:
        valid_cols = []
        for col in range(self.COLUMNS):
            if self.board_state[0][col] is None:
                valid_cols.append(col)
        return valid_cols

    def _update_win_state(self, last_row: int, last_col: int):
        is_win = self._is_move_vert_win(last_row, last_col) or self._is_move_horiz_win(last_row, last_col) \
            or self._is_move_right_diag_win(last_row, last_col) or self._is_move_left_diag_win(last_row, last_col)
        if(is_win):
            self.win_state = self.WinStates.RED if self.board_state[last_row][last_col] == ChipColors.RED else self.WinStates.BLACK

    def _is_move_vert_win(self, row: int, col: int) -> bool:
        chip = self.board_state[row][col]
        if chip is None:
            return False

        row_consecutive_total = 0
        for i in range(row, self.ROWS):
            if self.board_state[i][col] != chip:
                return False
            row_consecutive_total += 1
            if row_consecutive_total == self.WINNING_NUMBER:
                return True

        return False

    def _is_move_horiz_win(self, row: int, col: int) -> bool:
        chip = self.board_state[row][col]
        if chip is None:
            return False

        col_consecutive_total = 0
        for i in range(self.COLUMNS):
            if(self.board_state[row][i] == chip):
                col_consecutive_total += 1
                if(col_consecutive_total == self.WINNING_NUMBER):
                    return True
            else:
                col_consecutive_total = 0
        
        if col_consecutive_total >= self.WINNING_NUMBER:
            return True
        
        return False

    def _is_move_right_diag_win(self, row: int, col: int) -> bool:
        chip = self.board_state[row][col]
        if chip is None:
            return False

        upper_row, upper_col = 0, 0
        if(row > col):
            upper_row = row - col
            upper_col = 0
        elif col > row:
            upper_row = 0
            upper_col = col - row
        else:
            upper_row = 0
            upper_col = 0

        right_diag_consecutive_total = 0
        curr_col = upper_col
        for i in range(upper_row, self.ROWS):
            if self.board_state[i][curr_col] != chip:
                return False
            right_diag_consecutive_total += 1
            if right_diag_consecutive_total == self.WINNING_NUMBER:
                return True
            if curr_col == self.COLUMNS - 1:
                return False
            curr_col += 1

        return False

    def _is_move_left_diag_win(self, row: int, col: int) -> bool:
        chip = self.board_state[row][col]
        if chip is None:
            return False

        upper_row, upper_col = 0, 0
        if(row > col):
            upper_row = self.COLUMNS - (row - col)
            upper_col = 0
        elif col > row:
            upper_row = 0
            upper_col = self.ROWS - (col - row)
        else:
            upper_row = 0
            upper_col = self.COLUMNS - 1

        left_diag_consecutive_total = 0
        curr_col = upper_col
        for i in range(upper_row, self.ROWS):
            if self.board_state[i][curr_col] != chip:
                return False
            left_diag_consecutive_total += 1
            if left_diag_consecutive_total == self.WINNING_NUMBER:
                return True
            if curr_col == 0:
                return False
            curr_col -= 1

        return False