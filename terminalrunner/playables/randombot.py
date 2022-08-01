import random
from typing import List

from game.game import ChipColors
from game.playable import Playable


class RandomBot(Playable):

    def __init__(self, color: ChipColors, seed: int = 0):
        super().__init__(color)
        self.random = random.Random(seed)

    def move(self, state: List[List[int]],
             available_moves: List[int]) -> int:
        return self.random.choice(available_moves)

    def get_name(self) -> str:
        return "Random Bot"
