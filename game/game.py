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
        self.prev_moves = []

    def insert_chip(self, chip: ChipColors, col: int) -> WinStates:
        row = self.drop_chip(chip, col, self.board_state)

        self.prev_moves.append((chip, (row, col)))

        self._update_win_state(row, col)
        return self.win_state

    @classmethod
    def open_columns(cls, board_state: List[List[int]]) -> List[int]:
        open_cols = []
        for col in range(cls.COLUMNS):
            if board_state[0][col] is None:
                open_cols.append(col)
        return open_cols

    @classmethod
    def is_last_move_win(cls, last_row: int, last_col: int, board_state: List[List[int]]) -> bool:
        return cls._is_move_vert_win(last_row, last_col, board_state) or cls._is_move_horiz_win(last_row, last_col, board_state) \
            or cls._is_move_right_diag_win(last_row, last_col, board_state) or cls._is_move_left_diag_win(last_row, last_col, board_state)

    @classmethod
    def drop_chip(cls, chip: ChipColors, col: int, board_state: List[List[int]]) -> None:
        """
        Drops a chip into a column.
        :return the integer index of the row the chip landed in
        """
        open_cols = cls.open_columns(board_state=board_state)

        if col not in open_cols:
            raise ValueError("Invalid column")

        row = 0
        while row < cls.ROWS - 1 and board_state[row + 1][col] is None:
            row += 1

        board_state[row][col] = chip
        return row

    def _update_win_state(self, last_row: int, last_col: int):    
        open_cols = self.open_columns(self.board_state)
        if self.win_state is None and len(open_cols) == 0:
            self.win_state = self.WinStates.TIE
        elif(self.is_last_move_win(last_row, last_col, self.board_state)):
            self.win_state = self.WinStates.RED if self.board_state[last_row][last_col] == ChipColors.RED else self.WinStates.BLACK

    @classmethod
    def _is_move_vert_win(cls, row: int, col: int, board_state: List[List[int]]) -> bool:
        chip = board_state[row][col]
        if chip is None:
            return False

        row_consecutive_total = 0
        for i in range(row, cls.ROWS):
            if board_state[i][col] != chip:
                return False
            row_consecutive_total += 1
            if row_consecutive_total == cls.WINNING_NUMBER:
                return True

        return False

    @classmethod
    def _is_move_horiz_win(cls, row: int, col: int, board_state: List[List[int]]) -> bool:
        chip = board_state[row][col]
        if chip is None:
            return False

        col_consecutive_total = 0
        for i in range(cls.COLUMNS):
            if(board_state[row][i] == chip):
                col_consecutive_total += 1
                if(col_consecutive_total == cls.WINNING_NUMBER):
                    return True
            else:
                col_consecutive_total = 0
        
        if col_consecutive_total >= cls.WINNING_NUMBER:
            return True
        
        return False

    @classmethod
    def _is_move_right_diag_win(cls, row: int, col: int, board_state: List[List[int]]) -> bool:
        chip = board_state[row][col]
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
        for i in range(upper_row, cls.ROWS):
            if board_state[i][curr_col] != chip:
                return False
            right_diag_consecutive_total += 1
            if right_diag_consecutive_total == cls.WINNING_NUMBER:
                return True
            if curr_col == cls.COLUMNS - 1:
                return False
            curr_col += 1

        return False

    @classmethod
    def _is_move_left_diag_win(cls, row: int, col: int, board_state: List[List[int]]) -> bool:
        chip = board_state[row][col]
        if chip is None:
            return False

        upper_row, upper_col = 0, 0
        if(row > col):
            upper_row = cls.COLUMNS - (row - col)
            upper_col = 0
        elif col > row:
            upper_row = 0
            upper_col = cls.ROWS - (col - row)
        else:
            upper_row = 0
            upper_col = cls.COLUMNS - 1

        left_diag_consecutive_total = 0
        curr_col = upper_col
        for i in range(upper_row, cls.ROWS):
            if board_state[i][curr_col] != chip:
                return False
            left_diag_consecutive_total += 1
            if left_diag_consecutive_total == cls.WINNING_NUMBER:
                return True
            if curr_col == 0:
                return False
            curr_col -= 1

        return False