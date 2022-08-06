from abc import ABC, abstractmethod
from typing import List, Optional

from game.game import ChipColors
from game.playable import Playable
from game.winstates import WinStates


class Outputable(ABC):

    @abstractmethod
    def output_board(self, board: List[List[ChipColors]]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def request_move(self, playable: Playable):
        raise NotImplementedError()

    @abstractmethod
    def output_results(self, win_state: WinStates,
                       winner: Optional[Playable] = None):
        raise NotImplementedError()