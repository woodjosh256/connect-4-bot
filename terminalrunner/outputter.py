from typing import Optional, Tuple

from connect4.game import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
from connect4.winstates import WinStates
from terminalrunner.matchstats import MatchStats
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
        return
        # if system_name == 'nt':
        #     _ = system('cls')
        # else:
        #     _ = system('clear')

    def output_board(self, game_state: GameState) -> None:
        Outputter.clear()
        colored_sep_char = (Outputter.EMPTY_CODE + Outputter.SEPARATING_CHAR
                            + Outputter.END_CODE)
        for row in game_state.state:
            print(colored_sep_char
                  + colored_sep_char.join(map(Outputter._chip_to_str, row))
                  + colored_sep_char)
        print()

    @staticmethod
    def _chip_to_str(chip: ChipColors) -> str:
        if chip == ChipColors.RED:
            return Outputter.RED_CODE + Outputter.CHIP_CHAR + Outputter.END_CODE
        elif chip == ChipColors.BLACK:
            return Outputter.BLACK_CODE + Outputter.CHIP_CHAR + \
                   Outputter.END_CODE
        else:
            return Outputter.EMPTY_CODE + Outputter.EMPTY_CHAR + \
                   Outputter.END_CODE

    def request_move(self, playable: Playable) -> None:
        print(f"{playable.get_name()}'s turn:")

    def output_results(self, win_state: WinStates,
                       winner: Optional[Playable] = None) -> None:
        print(win_state)  # todo improve

    def output_tournament_stats(self, tournament_stats: Tuple[Playable, Playable, MatchStats]) -> None:
        for playable1, playable2, match_stats in tournament_stats:
            print(f"{playable1.get_name()} vs {playable2.get_name()}")
            print(match_stats)
            print()
