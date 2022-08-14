from connect4.gamestate import GameState
from playables.joshw.minimax import Minimax


class StandardMinimax(Minimax):

    @classmethod
    def get_name(cls) -> str:
        return "Standard Minimax"

    @classmethod
    def _static_eval(cls, game_state: GameState) -> float:
        return 0
