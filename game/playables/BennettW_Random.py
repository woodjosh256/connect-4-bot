from typing import List
import random

from game.chipcolors import ChipColors
from game.playable import Playable

class BennettW_Random(Playable):
    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: List[List[int]], available_moves: List[int]) -> int:
        return available_moves[random.randint(0, len(available_moves) - 1)]

    def get_name(self) -> str:
        return "BennettW_Random"