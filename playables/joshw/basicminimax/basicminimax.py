from connect4.gamestate import GameState
from playables.joshw.FastGameState2 import FastMove, FastGameState2
from playables.joshw.fastminimax2 import FastMinimax2
from playables.joshw.minimax import Minimax


class BasicMinimax(Minimax):

    @classmethod
    def get_name(cls) -> str:
        return "Basic Minimax"

    @classmethod
    def _static_eval(cls, game_state: GameState) -> float:
        if game_state.get_win_state() == cls.MAXIMISING_COLOR.to_win_state():
            return 10
        elif game_state.get_win_state() == cls.MINIMISING_COLOR.to_win_state():
            return -10
        else:
            return 0

class BasicMinimax2(FastMinimax2):

    @classmethod
    def get_name(cls) -> str:
        return "Basic Minimax"

    @classmethod
    def _static_eval(cls, game_state: FastGameState2, last_move: FastMove) -> float:
        if game_state.get_win_state(last_move) == cls.MAXIMISING_COLOR.to_win_state():
            return 10
        elif game_state.get_win_state(last_move) == cls.MINIMISING_COLOR.to_win_state():
            return -10
        else:
            return 0
