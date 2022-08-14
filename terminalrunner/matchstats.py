from dataclasses import dataclass, field
from itertools import chain
from statistics import mean
from typing import List, Optional

from connect4.playable import Playable
from connect4.winstates import WinStates
from terminalrunner.roundstats import RoundStats


@dataclass
class MatchStats:
    playable1: Playable
    playable2: Playable

    round_stats_list: List[RoundStats] = field(default_factory=lambda: [])

    def add_round(self, round_stats: RoundStats) -> None:
        self.round_stats_list.append(round_stats)

    def get_win_state_percentage(self, win_state: WinStates) -> Optional[float]:
        rounds = len(self.round_stats_list)
        if rounds == 0:
            return None

        wins = sum(r.win_state == win_state for r in self.round_stats_list)
        return wins / rounds

    def get_p1_avg_move_time(self) -> Optional[float]:
        rounds = len(self.round_stats_list)
        if rounds == 0:
            return None

        return mean(chain(*[r.p1_move_times for r in self.round_stats_list]))

    def get_p2_avg_move_time(self) -> Optional[float]:
        rounds = len(self.round_stats_list)
        if rounds == 0:
            return None

        return mean(chain(*[r.p2_move_times for r in self.round_stats_list]))
