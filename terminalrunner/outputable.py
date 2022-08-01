from abc import ABC, abstractmethod
from typing import List

from game.game import ChipColors


class Outputable(ABC):

    @abstractmethod
    def output_board(self, board: List[List[ChipColors]]) -> None:
        raise NotImplementedError()
