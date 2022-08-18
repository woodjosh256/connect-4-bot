import random
from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable

class ImprovedRandom(Playable):

    def __init__(self, color: ChipColors):
        super().__init__(color)

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Improved Random Bot"

    def move(self, game_state: GameState) -> int:
        winning_move = self._get_winning_move(game_state)
        if winning_move is not None:
            return winning_move

        blocking_move = self._get_blocking_move(game_state)
        if blocking_move is not None:
            return  blocking_move
        
        three_sequence_move = self._get_sequence_move(game_state, 3)
        if three_sequence_move is not None:
            return three_sequence_move

        three_sequence_blocking_move = self._get_sequence_blocking_move(game_state, 3)
        if three_sequence_blocking_move is not None:
            return three_sequence_blocking_move

        two_sequence_move = self._get_sequence_move(game_state, 2)
        if two_sequence_move is not None:
            return two_sequence_move

        two_sequence_blocking_move = self._get_sequence_blocking_move(game_state, 2)
        if two_sequence_blocking_move is not None:
            return two_sequence_blocking_move

        return random.choice(game_state.open_columns())

    def _get_winning_move(self, game_state: GameState) -> int:
        for col in game_state.open_columns():
            if self._is_winning_move(game_state, col):
                return col
        return None

    def _is_winning_move(self, game_state: GameState, col: int) -> bool:
        temp_game_state = game_state.drop_chip(self.color, col)
        return temp_game_state.get_win_state() is not None

    def _get_blocking_move(self, game_state: GameState) -> int:
        for col in game_state.open_columns():
            if self._is_blocking_move(game_state, col):
                return col
        return None

    def _is_blocking_move(self, game_state: GameState, col: int) -> bool:
        temp_game_state = game_state.drop_chip(self.color.get_opposing_color(), col)
        return temp_game_state.get_win_state() is not None   

    def _get_sequence_move(self, game_state: GameState, seq_len: int) -> int:
        for col in game_state.open_columns():
            if self._is_sequence(game_state, col, seq_len):
                return col
        return None

    def _is_sequence(self, game_state: GameState, col: int, seq_len: int) -> bool:
        temp_game_state = game_state.drop_chip(self.color, col)
        return temp_game_state.chips_in_last_pos_row() >= seq_len

    def _get_sequence_blocking_move(self, game_state: GameState, seq_len: int) -> int:
        for col in game_state.open_columns():
            if self._is_sequence_blocking(game_state, col, seq_len):
                return col
        return None

    def _is_sequence_blocking(self, game_state: GameState, col: int, seq_len: int) -> bool:
        temp_game_state = game_state.drop_chip(self.color.get_opposing_color(), col)
        return temp_game_state.chips_in_last_pos_row() >= seq_len
