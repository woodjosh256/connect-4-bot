from os import name as system_name, system
from typing import List, Optional

from game.game import ChipColors, WinStates
from game.playable import Playable
from terminalrunner.outputable import Outputable


class Outputter(Outputable):
    RED_CODE = '\033[1;31;47m'
    BLACK_CODE = '\033[1;30;47m'
    EMPTY_CODE = '\033[1;36;47m'
    END_CODE = '\033[0;0m'
    CHIP_CHAR = '●'
    EMPTY_CHAR = '○'
    SEPARATING_CHAR = " "

    @staticmethod
    def clear():
        if system_name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def output_board(self, board: List[List[ChipColors]]) -> None:
        self.clear()
        colored_sep_char = (self.EMPTY_CODE + self.SEPARATING_CHAR
                            + self.END_CODE)
        for row in board:
            print(colored_sep_char
                  + colored_sep_char.join(map(self._chip_to_str, row))
                  + colored_sep_char)
        print()

    def _chip_to_str(self, chip: ChipColors) -> str:
        if chip == ChipColors.RED:
            return self.RED_CODE + self.CHIP_CHAR + self.END_CODE
        elif chip == ChipColors.BLACK:
            return self.BLACK_CODE + self.CHIP_CHAR + self.END_CODE
        else:
            return self.EMPTY_CODE + self.EMPTY_CHAR + self.END_CODE

    def request_move(self, playable: Playable) -> None:
        print(f"{playable.get_name()}'s turn:")

    def output_results(self, win_state: WinStates,
                       winner: Optional[Playable] = None) -> None:
        print(win_state)  # todo improve
