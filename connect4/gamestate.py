from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional, List

from connect4.chipcolors import ChipColors
from connect4.move import Move
from connect4.winstates import WinStates


@dataclass(frozen=True)
class GameState:
    rows: int
    columns: int
    winning_number: int
    state: Tuple[Tuple[Optional[ChipColors], ...], ...]
    moves: Tuple[Move, ...]

    @staticmethod
    def new_game(rows: int, columns: int, winning_number: int) -> GameState:
        return GameState(
            rows=rows,
            columns=columns,
            winning_number=winning_number,
            state=((None,) * columns,) * rows,
            moves=()
        )

    def copy(self, rows: int = None, columns: int = None,
             winning_number: int = None,
             state: Tuple[Tuple[Optional[ChipColors], ...], ...] = None,
             moves: Tuple[Move] = None
             ):
        return GameState(
            rows=self.rows if rows is None else rows,
            columns=self.columns if columns is None else columns,
            winning_number=self.winning_number if winning_number is None
            else winning_number,
            state=self.state if state is None else state,
            moves=self.moves if moves is None else moves
        )

    def _place_chip(self, move: Move) -> GameState:
        return self.copy(
            moves=self.moves + (move,),
            state=tuple(
                tuple(
                    move.color if r == move.row and c == move.col
                    else self.state[r][c]
                    for c in range(self.columns)
                )
                for r in range(self.rows)
            )
        )

    def open_columns(self) -> List[int]:
        return [col for col in range(self.columns)
                if self.state[0][col] is None]

    def drop_chip(self, color: ChipColors, col: int) -> GameState:
        if col not in self.open_columns():
            raise ValueError(f"Invalid column. "
                             f"Valid columns: {self.open_columns()}")
        row = 0
        while row < self.rows - 1 \
                and self.state[row + 1][col] is None:
            row += 1

        return self._place_chip(Move(row, col, color))

    def get_win_state(self) -> Optional[WinStates]:
        if not self.moves:
            return None

        if not self.open_columns():
            return WinStates.TIE

        if self.chips_in_last_pos_row() >= self.winning_number:
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
            if max_dist >= self.winning_number:
                return max_dist

        return max_dist

    def horiz_dist(self) -> int:
        last_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (min_col > 0
               and self.state[last_row][min_col - 1] == last_color):
            min_col -= 1
        while (max_col < self.columns - 1
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
        while (max_row < self.rows - 1
               and self.state[max_row + 1][last_col] == last_color):
            max_row += 1

        return max_row - min_row + 1

    def incline_diagonal_dist(self) -> int:
        min_row = max_row = self.moves[-1].row
        min_col = max_col = self.moves[-1].col
        last_color = self.moves[-1].color

        while (max_row < self.rows - 1 and min_col > 0
               and self.state[max_row + 1][min_col - 1] == last_color):
            max_row += 1
            min_col -= 1
        while (min_row > 0 and max_col < self.columns - 1
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
        while (max_row < self.rows - 1 and max_col < self.columns - 1
               and self.state[max_row + 1][max_col + 1] == last_color):
            max_row += 1
            max_col += 1

        return max_row - min_row + 1


state1 = GameState.new_game(6, 7, 4)
state2 = state1.copy(rows=5)
