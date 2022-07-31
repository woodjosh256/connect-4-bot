from abc import ABC, abstractmethod
from typing import List, Tuple

from game.chipcolors import ChipColors


class Playable(ABC):

    def __init__(self, color: ChipColors):
        self.color = color

    @abstractmethod
    def move(self, game_state: List[List[int]],
             available_moves: List[int],
             prev_moves: List[Tuple]) -> int:
        """
        :param game_state: a 2-dimensional array containing the game's
        current state. (6 rows, 7 columns)
        :param available_moves: an array of all slots that chips could
        go in represented by ints in range: [0, 6]
        :param prev_moves: an array of all previous moves in the game
        in the form of (color, (row, column))
        :return an int representing the slot the chip will go in.
        Returning an invalid choice here results in a forfeit
        """
        raise NotImplementedError

    @classmethod
    def get_name(cls) -> str:
        """
        :return name of the playable
        """
        raise NotImplementedError
