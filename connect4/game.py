from typing import List

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.winstates import WinStates


class Game:

    ROWS = 6
    COLUMNS = 7
    WINNING_NUMBER = 4

    def __init__(self):
        self.state = GameState.new_game(self.ROWS, self.COLUMNS,
                                        self.WINNING_NUMBER)

    def open_columns(self) -> List[int]:
        return self.state.open_columns()

    def drop_chip(self, color: ChipColors, col: int) -> None:
        self.state = self.state.drop_chip(color, col)

    def get_win_state(self) -> WinStates:
        return self.state.get_win_state()
