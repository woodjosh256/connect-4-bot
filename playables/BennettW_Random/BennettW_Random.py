import random

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable


class BennettW_Random(Playable):

    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: GameState) -> int:
        return random.choice(game_state.open_columns())

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Random Bot"
