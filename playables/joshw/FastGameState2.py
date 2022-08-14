from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Tuple, Optional, List

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.move import Move
from connect4.winstates import WinStates


@dataclass
class FastMove:
    row: int
    col: int
    maximising_player: bool


@dataclass
class FastGameState2:
    rows: int
    columns: int
    winning_number: int
    state: List[List[Optional[bool], ...], ...]

    # red - true, maximising player
    # black - false, minimising player

    @staticmethod
    def new_game(rows: int, columns: int,
                 winning_number: int) -> FastGameState2:
        return FastGameState2(
            rows=rows,
            columns=columns,
            winning_number=winning_number,
            state=[[None] * columns for i in range(rows)]
        )

    @staticmethod
    def from_gamestate(gamestate: GameState) -> FastGameState2:
        return FastGameState2(
            rows=gamestate.rows,
            columns=gamestate.columns,
            winning_number=gamestate.winning_number,
            state=[list(row) for row in gamestate.state]
        )

    def open_columns(self) -> List[int]:
        return [col for col in range(self.columns)
                if self.state[0][col] is None]

    def drop_chip(self, maximising_player: bool, col: int) -> FastMove:
        row = 0
        while row < self.rows - 1 \
                and self.state[row + 1][col] is None:
            row += 1

        self.state[row][col] = maximising_player
        return FastMove(row=row, col=col, maximising_player=maximising_player)

    def undo_fastmove(self, move: FastMove) -> None:
        self.state[move.row][move.col] = None

    def get_win_state(self, last_move: FastMove) -> Optional[WinStates]:
        if last_move is None:
            return None

        if not self.open_columns():
            return WinStates.TIE

        if self.chips_in_row_from_move(last_move) >= self.winning_number:
            if last_move.maximising_player:
                return WinStates.RED
            else:
                return WinStates.BLACK

        return None

    def chips_in_row_from_move(self, last_move: FastMove) -> int:
        """
        :return: the largest number of chips in a row that are the last
                    placed chip's color. Checks horizontal, vertical and
                    diagonal rows. If a row of chips is found that is
                    the winning number or higher, that row length is
                    returned.
        """
        max_dist = 0
        # todo - issue of some sort with this
        for win_condition in [self.horiz_dist,
                              self.vert_dist,
                              self.incline_diagonal_dist,
                              self.decline_diagonal_dist]:
            distance = win_condition(last_move)
            max_dist = max(distance, max_dist)
            if max_dist >= self.winning_number:
                return max_dist

        return max_dist

    def horiz_dist(self, last_move: FastMove) -> int:
        min_col = max_col = last_move.col
        player_bool = last_move.maximising_player

        while (min_col > 0
               and self.state[last_move.row][min_col - 1] == player_bool):
            min_col -= 1
        while (max_col < self.columns - 1
               and self.state[last_move.row][max_col + 1] == player_bool):
            max_col += 1

        return max_col - min_col + 1

    def vert_dist(self, last_move: FastMove) -> int:
        min_row = max_row = last_move.row
        player_bool = last_move.maximising_player

        while (min_row > 0
               and self.state[min_row - 1][last_move.col] == player_bool):
            min_row -= 1
        while (max_row < self.rows - 1
               and self.state[max_row + 1][last_move.col] == player_bool):
            max_row += 1

        return max_row - min_row + 1

    def incline_diagonal_dist(self, last_move: FastMove) -> int:
        min_row = max_row = last_move.row
        min_col = max_col = last_move.col
        player_bool = last_move.maximising_player

        while (max_row < self.rows - 1 and min_col > 0
               and self.state[max_row + 1][min_col - 1] == player_bool):
            max_row += 1
            min_col -= 1
        while (min_row > 0 and max_col < self.columns - 1
               and self.state[min_row - 1][max_col + 1] == player_bool):
            min_row -= 1
            max_col += 1

        return max_row - min_row + 1

    def decline_diagonal_dist(self, last_move: FastMove) -> int:
        min_row = max_row = last_move.row
        min_col = max_col = last_move.col
        player_bool = last_move.maximising_player

        while (min_row > 0 and min_col > 0
               and self.state[min_row - 1][min_col - 1] == player_bool):
            min_row -= 1
            min_col -= 1
        while (max_row < self.rows - 1 and max_col < self.columns - 1
               and self.state[max_row + 1][max_col + 1] == player_bool):
            max_row += 1
            max_col += 1

        return max_row - min_row + 1




