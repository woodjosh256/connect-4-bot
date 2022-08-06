from enum import Enum

from connect4.winstates import WinStates


class ChipColors(Enum):
    RED = 0
    BLACK = 1

    def get_opposing_color(self):
        if self == ChipColors.RED:
            return ChipColors.BLACK
        else:
            return ChipColors.RED

    def to_win_state(self):
        if self == ChipColors.RED:
            return WinStates.RED
        elif self == ChipColors.BLACK:
            return WinStates.BLACK