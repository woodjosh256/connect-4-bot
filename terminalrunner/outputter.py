from os import name as system_name, system
from statistics import mean

from connect4.game import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
from connect4.winstates import WinStates
from terminalrunner.matchstats import MatchStats
from terminalrunner.outputable import Outputable
from terminalrunner.roundstats import RoundStats


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
        if system_name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

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

    def output_board(self, game_state: GameState) -> None:
        self.clear()
        colored_sep_char = (Outputter.EMPTY_CODE + Outputter.SEPARATING_CHAR
                            + Outputter.END_CODE)
        for row in game_state.state:
            print(colored_sep_char
                  + colored_sep_char.join(map(Outputter._chip_to_str, row))
                  + colored_sep_char)
        print()

    def request_move(self, playable: Playable) -> None:
        print(f"{playable.get_name()}'s turn:")

    def output_match_stats(self, stats: MatchStats) -> None:
        p1_name = stats.playable1.get_name()
        p2_name = stats.playable2.get_name()
        rounds = len(stats.round_stats_list)
        p1_win_percentage = stats.get_win_state_percentage(
            stats.playable1.color.to_win_state()
        )
        p2_win_percentage = stats.get_win_state_percentage(
            stats.playable2.color.to_win_state()
        )
        tie_percentage = stats.get_win_state_percentage(WinStates.TIE)

        p1_move_time = stats.get_p1_avg_move_time()
        p2_move_time = stats.get_p2_avg_move_time()

        print(f"{p1_name} v {p2_name}" +
              "\n\t" + f"Rounds: {rounds}" +
              "\n\t" + f"Win Percentages:" +
              "\n\t\t" + f"{p1_name} - {p1_win_percentage * 100:.1f}%" +
              "\n\t\t" + f"{p2_name} - {p2_win_percentage * 100:.1f}%" +
              "\n\t\t" + f"Tie - {tie_percentage * 100:.1f}%" +
              "\n\t" + f"Mean time / move" +
              "\n\t\t" + f"{p1_name} - {p1_move_time * 1000:.2f} ms" +
              "\n\t\t" + f"{p2_name} - {p2_move_time * 1000:.2f} ms"
              )

    def output_round_end(self, round_stats: RoundStats,
                         game_state: GameState) -> None:
        winner = round_stats.win_state

        if round_stats.playable1.color.to_win_state() == winner:
            win_name = round_stats.playable1.get_name()
        elif round_stats.playable2.color.to_win_state() == winner:
            win_name = round_stats.playable2.get_name()
        else:
            win_name = "Tie"

        print(f"Winner: {win_name}")
        print(f"P1 mean time/move: {mean(round_stats.p1_move_times) * 1000} ms")
        print(f"P2 mean time/move: {mean(round_stats.p2_move_times)* 1000} ms")
        self.output_board(game_state)
