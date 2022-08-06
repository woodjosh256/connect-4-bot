from dataclasses import dataclass

from connect4.chipcolors import ChipColors


@dataclass(frozen=True)
class Move:
    row: int
    col: int
    color: ChipColors
