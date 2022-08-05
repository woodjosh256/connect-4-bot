import random
from typing import List

from game.chipcolors import ChipColors
from game.playable import Playable
from game.game import Move

class RandomBot(Playable):

    def __init__(self, color: ChipColors, seed: int = 0):
        super().__init__(color)
        self.random = random.Random()

    def move(self, state: List[List[int]],
             available_moves: List[int],
             prev_moves: List[Move]) -> int:
        return self.random.choice(available_moves)

    @classmethod
    def get_name(cls) -> str:
        return "Random Bot"
