from abc import ABC, abstractmethod

from connect4.gamestate import GameState
from connect4.playable import Playable
from terminalrunner.matchstats import MatchStats
from terminalrunner.roundstats import RoundStats


class Outputable(ABC):

    @abstractmethod
    def output_board(self, game_state: GameState) -> None:
        raise NotImplementedError()

    @abstractmethod
    def request_move(self, playable: Playable) -> None:
        raise NotImplementedError()

    @abstractmethod
    def output_match_stats(self, match_stats: MatchStats) -> None:
        raise NotImplementedError()

    @abstractmethod
    def output_round_end(self, round_stats: RoundStats,
                         game_state: GameState) -> None:
        raise NotImplementedError()
