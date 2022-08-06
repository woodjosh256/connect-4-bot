from connect4.playable import Playable
from connect4.winstates import WinStates


class MatchStats:

    def __init__(self, playable1: Playable, playable2: Playable):
        self.playable1_win_count: int = 0
        self.playable2_win_count: int = 0
        self.tie_count: int = 0
        self.game_count: int = 0
        self.playable1 = playable1
        self.playable2 = playable2

    def __str__(self):
        return f"\t{self.playable1.get_name()} wins: {self.playable1_win_count}\r\n" \
               f"\t{self.playable2.get_name()} wins: {self.playable2_win_count}\r\n" \
               f"\tTie: {self.tie_count}"

    def add_round(self, win_state: WinStates):
        match win_state:
            case WinStates.RED:
                self.playable1_win_count += 1
            case WinStates.BLACK:
                self.playable2_win_count += 1
            case WinStates.TIE:
                self.tie_count += 1
        self.game_count += 1

    def get_win_state_percentage(self, win_state: WinStates):
        match win_state:
            case WinStates.RED:
                return self.playable1_win_count / self.game_count
            case WinStates.BLACK:
                return self.playable2_win_count / self.game_count
            case WinStates.TIE:
                return self.tie_count / self.game_count