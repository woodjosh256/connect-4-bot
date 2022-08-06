from abc import ABC, abstractmethod

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState


class Playable(ABC):

    def __init__(self, color: ChipColors):
        self.color = color

    @abstractmethod
    def move(self, state: GameState) -> int:
        """
        :param state: immutable GameState object containing the game's
        state and move history.
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
        Method called at the start of each new connect4, to alert the
        playable a new connect4 has started.
        """
        pass
