from abc import ABC, abstractmethod
from typing import List, Optional

from game.chipcolors import ChipColors
from game.move import Move


class Playable(ABC):

    def __init__(self, color: ChipColors):
        self.color = color

    @abstractmethod
    def move(self, state: List[List[Optional[ChipColors]]],
             available_moves: List[int],
             prev_moves: List[Move]) -> int:
        """
        :param state: a 2-dimensional list containing the game's
        current state. (6 rows, 7 columns)
        :param available_moves: a list of all slots that chips could
        go in represented by ints in range: [0, columns]
        :param prev_moves: an array of all previous moves for the game
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

    def new_game(self) -> None:
        """
        Method called at the start of each new game, to alert the
        playable a new game has started.
        """
        pass
