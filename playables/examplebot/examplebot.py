import random
from typing import Optional

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable


class ExampleBot(Playable):

    def __init__(self, color: ChipColors,
                 seed: Optional[int] = 0):
        super().__init__(color)
        if seed is None:
            self.random = random.Random()
        else:
            self.random = random.Random(seed)

    def move(self, game_state: GameState) -> int:
        return self.random.choice(game_state.open_columns())

    @classmethod
    def get_name(cls) -> str:
        return "Example Bot"
