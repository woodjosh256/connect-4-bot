from typing import List, Tuple
import random

from game.chipcolors import ChipColors
from game.playable import Playable

class BennettW_Random(Playable):
    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: List[List[int]], available_moves: List[int], prev_moves: List[Tuple]) -> int:
        return available_moves[random.randint(0, len(available_moves) - 1)]

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Random"