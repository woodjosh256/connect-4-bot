from typing import List, Optional

from game.chipcolors import ChipColors
from game.move import Move
from game.winstates import WinStates


class Game:

    ROWS = 6
    COLUMNS = 7
    WINNING_NUMBER = 4

    def __init__(self,
                 state: Optional[List[List[Optional[ChipColors]]]] = None,
                 moves: Optional[List[Move]] = None) -> None:
        if moves is None:
            moves = []
        if state is None:
            state = [[None] * self.COLUMNS for i in range(self.ROWS)]

        self.state = state
        self.moves = moves

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

        if not self.open_columns():
            return WinStates.TIE

        if self.chips_in_last_pos_row() >= self.WINNING_NUMBER:
            last_color = self.moves[-1].color
            if last_color == ChipColors.RED:
                return WinStates.RED
            else:
                return WinStates.BLACK

        return None

    def chips_in_last_pos_row(self) -> int:
        """
        :return: the largest number of chips in a row that are the last
                    placed chip's color. Checks horizontal, vertical and
                    diagonal rows. If a row of chips is found that is
                    the winning number or higher, that row length is
                    returned.
        """
        if not self.moves:
            return 0

        max_dist = 0
        for win_condition in [self.horiz_dist,
                              self.vert_dist,
                              self.incline_diagonal_dist,
                              self.decline_diagonal_dist]:
            distance = win_condition()
            max_dist = max(max_dist, distance)
            if max_dist >= self.WINNING_NUMBER:
                return max_dist

        return max_dist

    def horiz_dist(self) -> int:
        last_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_col > 0
               and self.state[last_row][min_col - 1] == last_color):
            min_col -= 1
        while (max_col < self.COLUMNS - 1
               and self.state[last_row][max_col + 1] == last_color):
            max_col += 1

        return max_col - min_col + 1

    def vert_dist(self) -> int:
        min_row = max_row = self.moves[-1].row
        last_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_row > 0
               and self.state[min_row - 1][last_col] == last_color):
            min_row -= 1
        while (max_row < self.ROWS - 1
               and self.state[max_row + 1][last_col] == last_color):
            max_row += 1

        return max_row - min_row + 1

    def incline_diagonal_dist(self) -> int:
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

        return max_row - min_row + 1

    def decline_diagonal_dist(self) -> int:
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

        return max_row - min_row + 1
