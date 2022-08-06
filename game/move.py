from dataclasses import dataclass

from game.chipcolors import ChipColors


@dataclass
class Move:
    row: int
    col: int
    color: ChipColors
