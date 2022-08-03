from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from game.chipcolors import ChipColors

class WinStates(Enum):
    RED = 0
    BLACK = 1
    TIE = 2


@dataclass
class Move:
    row: int
    col: int
    color: ChipColors


class Game:

    ROWS = 10
    COLUMNS = 10
    WINNING_NUMBER = 4

    def __init__(self) -> None:
        self.state: List[List[Optional[ChipColors]]] \
            = [[None] * self.COLUMNS for i in range(self.ROWS)]
        self.moves: List[Move] = []

    def insert_chip(self, color: ChipColors, col: int) -> None:
        if col not in self.open_columns():
            raise ValueError(f"Invalid column. "
                             f"Valid columns: {self.open_columns()}")

        row = 0
        while row < self.ROWS - 1 \
                and self.state[row + 1][col] is None:
            row += 1

        self.state[row][col] = color
        self.moves.append(Move(row, col, color))

    def open_columns(self) -> List[int]:
        return [col for col in range(self.COLUMNS)
                if self.state[0][col] is None]

    def get_win_state(self) -> Optional[WinStates]:
        if not self.moves:
            return None

        for win_condition in [self._horiz_dist,
                              self._vert_dist,
                              self._incline_diagonal_dist,
                              self._decline_diagonal_dist]:
            distance = win_condition()
            if distance >= self.WINNING_NUMBER - 1:
                last_color = self.moves[-1].color
                if last_color == ChipColors.RED:
                    return WinStates.RED
                else:
                    return WinStates.BLACK

        if not self.open_columns():
            return WinStates.TIE

        return None

    def _horiz_dist(self) -> int:
        last_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_col > 0
               and self.state[last_row][min_col - 1] == last_color):
            min_col -= 1
        while (max_col < self.COLUMNS - 1
               and self.state[last_row][max_col + 1] == last_color):
            max_col += 1

        return max_col - min_col

    def _vert_dist(self) -> int:
        min_row = max_row = self.moves[-1].row
        last_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_row > 0
               and self.state[min_row - 1][last_col] == last_color):
            min_row -= 1
        while (max_row < self.ROWS - 1
               and self.state[max_row + 1][last_col] == last_color):
            max_row += 1

        return max_row - min_row

    def _incline_diagonal_dist(self) -> int:
        min_row = max_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (max_row < self.ROWS - 1 and min_col > 0
               and self.state[max_row + 1][min_col - 1] == last_color):
            max_row += 1
            min_col -= 1
        while (min_row > 0 and max_col < self.COLUMNS - 1
               and self.state[min_row - 1][max_col + 1] == last_color):
            min_row -= 1
            max_col += 1

        return max_row - min_row

    def _decline_diagonal_dist(self) -> int:
        min_row = max_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_row > 0 and min_col > 0
               and self.state[min_row - 1][min_col - 1] == last_color):
            min_row -= 1
            min_col -= 1
        while (max_row < self.ROWS - 1 and max_col < self.COLUMNS - 1
               and self.state[max_row + 1][max_col + 1] == last_color):
            max_row += 1
            max_col += 1

        return max_row - min_row
