from dataclasses import dataclass, field
from typing import List

from connect4.playable import Playable
from connect4.winstates import WinStates


@dataclass
class RoundStats:

    playable1: Playable
    playable2: Playable
    win_state: WinStates = None

    p1_move_times: List[float] = field(default_factory=lambda: [])
    p2_move_times: List[float] = field(default_factory=lambda: [])
