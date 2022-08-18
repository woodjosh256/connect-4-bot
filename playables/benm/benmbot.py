from typing import Optional
from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
from ...connect4.winstates import WinStates
from benmminimax import BenMMiniMax


class BenMBot(Playable):

    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: GameState) -> int:
        BenMMiniMax.move(game_state)

    @classmethod
    def get_name(cls) -> str:
        return "BenM Bot"
