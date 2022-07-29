from abc import ABC
from typing import List

from game.chipcolors import ChipColors


class Outputable(ABC):
    RED_CODE = '\033[1;31;47m'
    BLACK_CODE = '\033[1;30;47m'
    EMPTY_CODE = '\033[1;36;47m'
    END_CODE = '\033[0;0m'
    CHIP_CHAR = '●'
    EMPTY_CHAR = '○'
    SEPARATING_CHAR = " "

    def output_board(self, board: List[List[ChipColors]]) -> None:
        colored_sep_char = self.EMPTY_CODE + self.SEPARATING_CHAR \
                           + self.END_CODE
        for row in board:
            print(colored_sep_char
                  + colored_sep_char.join(map(self._chip_to_str, row))
                  + colored_sep_char)

    def _chip_to_str(self, chip: ChipColors) -> str:
        if chip == ChipColors.RED:
            return self.RED_CODE + self.CHIP_CHAR + self.END_CODE
        elif chip == ChipColors.BLACK:
            return self.BLACK_CODE + self.CHIP_CHAR + self.END_CODE
        else:
            return self.EMPTY_CODE + self.EMPTY_CHAR + self.END_CODE
