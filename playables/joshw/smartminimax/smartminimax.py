from playables.joshw.MutableGameState import FastMove, MutableGameState
from playables.joshw.minimaxwithcaching import MinimaxWithCaching


class SmartMinimax(MinimaxWithCaching):
    DEPTH = 8

    @classmethod
    def get_name(cls) -> str:
        return "Smart Minimax"

    def _static_eval(self, game_state: MutableGameState, last_move: FastMove) -> float:
        winstate = game_state.get_win_state(last_move)
        if winstate == self.MAXIMISING_COLOR.to_win_state():
            return 10
        elif winstate == self.MINIMISING_COLOR.to_win_state():
            return -10
        else:
            return 0
