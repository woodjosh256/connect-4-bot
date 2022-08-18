from playables.joshw.MutableGameState import FastMove, MutableGameState
from playables.joshw.minimax import Minimax


class BasicMinimax(Minimax):
    DEPTH = 3

    @classmethod
    def get_name(cls) -> str:
        return "Basic Minimax"

    @classmethod
    def _static_eval(cls, game_state: MutableGameState, last_move: FastMove) -> float:
        if game_state.get_win_state(last_move) == cls.MAXIMISING_COLOR.to_win_state():
            return 10
        elif game_state.get_win_state(last_move) == cls.MINIMISING_COLOR.to_win_state():
            return -10
        else:
            return 0
