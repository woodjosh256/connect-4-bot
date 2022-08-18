from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple, Set

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.winstates import WinStates
from playables.joshw.GameStateHash import GameStateHash


@dataclass
class FastMove:
    row: int
    col: int
    maximising_player: bool


@dataclass
class MutableGameState:
    rows: int
    columns: int
    winning_number: int
    state: List[List[Optional[bool], ...], ...]
    is_black_next: bool

    open_slots_per_column: List[int]
    even_empty_slots: List[int]
    open_columns: List[int]

    red_threats: Set[Tuple[int, int]]
    black_threats: Set[Tuple[int, int]]

    # red - true, maximising player
    # black - false, minimising player

    def __post_init__(self):
        self.state_hash = GameStateHash.generate(self)

        self.win_check_methods = [self.horiz_dist,
                                  self.vert_dist,
                                  self.incline_diagonal_dist,
                                  self.decline_diagonal_dist]

        # todo calculate threats

    @staticmethod
    def new_game(rows: int, columns: int, winning_number: int,
                 is_black_next: bool) -> MutableGameState:
        return MutableGameState(
            rows=rows,
            columns=columns,
            winning_number=winning_number,
            state=[[None] * columns for i in range(rows)],
            open_slots_per_column=[rows] * columns,
            even_empty_slots=[rows % 2 == 0] * columns,
            open_columns=list(range(columns)),
            is_black_next=is_black_next,
            red_threats=set(),
            black_threats=set(),
        )

    @staticmethod
    def from_gamestate(gamestate: GameState,
                       is_black_next: bool) -> MutableGameState:
        open_slots_per_column = []
        for col in range(gamestate.columns):
            count = gamestate.rows
            for row in range(gamestate.rows):
                if gamestate.state[row][col] is not None:
                    count -= 1
            open_slots_per_column.append(count)

        return MutableGameState(
            rows=gamestate.rows,
            columns=gamestate.columns,
            winning_number=gamestate.winning_number,
            state=[[(col == ChipColors.RED) if col is not None else None
                    for col in row] for row in gamestate.state],
            open_slots_per_column=open_slots_per_column,
            even_empty_slots=[slot_count % 2 == 0
                              for slot_count in open_slots_per_column],
            open_columns=gamestate.open_columns(),
            is_black_next=is_black_next,
            red_threats=set(),
            black_threats=set(),
        )

    def drop_chip(self, maximising_player: bool, col: int) -> FastMove:
        row = self.open_slots_per_column[col] - 1
        move = FastMove(row=row, col=col, maximising_player=maximising_player)
        self.do_fastmove(move)
        return move

    def do_fastmove(self, move: FastMove) -> None:
        self.state[move.row][move.col] = move.maximising_player

        self.open_slots_per_column[move.col] -= 1
        self.even_empty_slots[move.col] = not self.even_empty_slots[move.col]
        if self.open_slots_per_column[move.col] == 0:
            self.open_columns.remove(move.col)
        self.is_black_next = not self.is_black_next
        self.state_hash.update_hash(move.row, move.col, None,
                                    move.maximising_player)

    def undo_fastmove(self, move: FastMove) -> None:
        self.state[move.row][move.col] = None

        if self.open_slots_per_column[move.col] == 0:
            self.open_columns.append(move.col)
            self.open_columns.sort()
        self.open_slots_per_column[move.col] += 1
        self.even_empty_slots[move.col] = not self.even_empty_slots[move.col]
        self.is_black_next = not self.is_black_next
        self.state_hash.update_hash(move.row, move.col, move.maximising_player,
                                    None)

    def get_win_state(self, last_move: FastMove) -> Optional[WinStates]:
        if last_move is None:
            return None

        if self.chips_in_row_from_move(last_move) >= self.winning_number:
            if last_move.maximising_player:
                return WinStates.RED
            else:
                return WinStates.BLACK

        if not self.open_columns:
            return WinStates.TIE

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
        for win_condition in self.win_check_methods:
            distance = win_condition(last_move)
            if distance > max_dist:
                max_dist = distance
                if max_dist >= self.winning_number:
                    return max_dist

        return max_dist

    def _check_threats(self, positions: List[Tuple[int, int]],
                       maximising_player: bool) -> None:
        """checks if positions entered are threats,
        if they are adds them."""
        for pos in positions:
            row = pos[0]
            col = pos[1]
            if not (0 <= row < self.rows and 0 <= col < self.columns):
                continue

            if self.state[row][col] is None:
                if maximising_player:
                    self.red_threats.add(pos)
                else:
                    self.black_threats.add(pos)

    def horiz_dist(self, last_move: FastMove) -> int:
        min_col = max_col = last_move.col
        player_bool = last_move.maximising_player

        while (min_col > 0
               and self.state[last_move.row][min_col - 1] == player_bool):
            min_col -= 1
        while (max_col < self.columns - 1
               and self.state[last_move.row][max_col + 1] == player_bool):
            max_col += 1

        distance = max_col - min_col + 1
        if distance == self.winning_number - 1:
            self._check_threats([(last_move.row, min_col - 1),
                                 (last_move.row, max_col + 1)],
                                last_move.maximising_player)

        return distance

    def vert_dist(self, last_move: FastMove) -> int:
        min_row = max_row = last_move.row
        player_bool = last_move.maximising_player

        while (min_row > 0
               and self.state[min_row - 1][last_move.col] == player_bool):
            min_row -= 1
        while (max_row < self.rows - 1
               and self.state[max_row + 1][last_move.col] == player_bool):
            max_row += 1

        distance = max_row - min_row + 1
        if distance == self.winning_number - 1:
            self._check_threats([(min_row - 1, last_move.col),
                                 (max_row + 1, last_move.col)],
                                last_move.maximising_player)

        return distance

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

        distance = max_row - min_row + 1

        if distance == self.winning_number - 1:
            self._check_threats([(min_row + 1, min_col - 1),
                                 (max_row - 1, max_col + 1)],
                                last_move.maximising_player)

        return distance

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

        distance = max_row - min_row + 1

        if distance == self.winning_number - 1:
            self._check_threats([(min_row - 1, min_row - 1),
                                 (max_row + 1, max_row + 1)],
                                last_move.maximising_player)

        return distance

    def get_hash(self) -> int:
        return self.state_hash.cur_hash
