import random

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable


class ExampleBot(Playable):

    def __init__(self, color: ChipColors,
                 seed: int = 0):
        super().__init__(color)
        self.random = random.Random(seed)

    def move(self, game_state: GameState) -> int:
        return self.random.choice(game_state.open_columns())

    @classmethod
    def get_name(cls) -> str:
        return "Example Bot"
