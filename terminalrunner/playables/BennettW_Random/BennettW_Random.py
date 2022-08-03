import random
from typing import List, Optional
from game.chipcolors import ChipColors
from game.game import Move
from game.playable import Playable

class BennettW_Random(Playable):
    
    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, state: List[List[Optional[ChipColors]]],
            available_moves: List[int],
            prev_moves: List[Move]) -> int:
        return random.choice(available_moves)

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Random Bot"