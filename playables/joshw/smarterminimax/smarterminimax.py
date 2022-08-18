from connect4.chipcolors import ChipColors
from playables.joshw.MutableGameState import FastMove, MutableGameState
from playables.joshw.minimaxwithcaching import MinimaxWithCaching


class SmarterMinimax(MinimaxWithCaching):
    WINNING_NUMBER = 4
    COLUMNS = 7
    DEPTH = 7

    def __init__(self, color: ChipColors):
        super().__init__(color)
        self.maximising = self.color == ChipColors.RED
        self.threat_arr = [0] * self.COLUMNS

    @classmethod
    def get_name(cls) -> str:
        return "Smarter Minimax"


    def get_threat_pts(self, game_state: MutableGameState,
                       maximising_next: bool) -> float:
        immediate_red = 0
        immediate_black = 0
        for threat in game_state.red_threats:
            if threat[0] == game_state.open_slots_per_column[threat[1]] - 1:
                immediate_red += 1
        for threat in game_state.black_threats:
            if threat[0] == game_state.open_slots_per_column[threat[1]] - 1:
                immediate_black += 1

        if maximising_next and immediate_red > 0:
            return 10000
        elif not maximising_next and immediate_black > 0:
            return -10000
        elif immediate_red > 1:
            return 10000
        elif immediate_black > 1:
            return -10000

        return len(game_state.red_threats) - len(game_state.black_threats)

    def _static_eval(self, game_state: MutableGameState,
                     last_move: FastMove) -> float:
        chips_in_row = game_state.chips_in_row_from_move(last_move)

        score = 0
        if chips_in_row >= self.WINNING_NUMBER:
            if last_move.maximising_player:
                score += 100000
            else:
                score -= 100000

        threat_pts = self.get_threat_pts(game_state, not last_move.maximising_player)
        score += threat_pts

        return score




