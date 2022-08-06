from abc import ABC, abstractmethod
from typing import Optional

from connect4.gamestate import GameState
from connect4.playable import Playable
from connect4.winstates import WinStates


class Outputable(ABC):

    @abstractmethod
    def output_board(self, game_state: GameState) -> None:
        raise NotImplementedError()

    @abstractmethod
    def request_move(self, playable: Playable):
        raise NotImplementedError()

    @abstractmethod
    def output_results(self, win_state: WinStates,
                       winner: Optional[Playable] = None):
        raise NotImplementedError()
