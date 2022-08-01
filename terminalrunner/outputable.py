from abc import ABC, abstractmethod
from typing import List, Optional

from game.game import ChipColors, WinStates
from game.playable import Playable


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