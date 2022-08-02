from abc import ABC, abstractmethod
from typing import List, Optional

from game.game import ChipColors, Move


class Playable(ABC):

    def __init__(self, color: ChipColors):
        self.color = color

    @abstractmethod
    def move(self, state: List[List[Optional[ChipColors]]],
             available_moves: List[int], past_moves: List[Move]) -> int:
        """
        :param state: a 2-dimensional list containing the game's
        current state. (6 rows, 7 columns)
        :param available_moves: a list of all slots that chips could
        go in represented by ints in range: [0, 6]
        :param past_moves: a list of all past moves for the current game
        :return an int representing the slot the chip will go in.
        Returning an invalid choice here results in a forfeit
        """
        raise NotImplementedError()

    @abstractmethod
    def get_name(self) -> str:
        """
        :return name of the playable
        """
        raise NotImplementedError()
