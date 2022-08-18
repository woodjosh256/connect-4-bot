import random
from abc import abstractmethod
from typing import Dict, List

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
from playables.joshw.MutableGameState import MutableGameState, FastMove


class Minimax(Playable):
    MAXIMISING_COLOR = ChipColors.RED
    MINIMISING_COLOR = ChipColors.BLACK
    DEPTH = 3
    COLOR_MAP = {
        ChipColors.RED: True,
        ChipColors.BLACK: False
    }

    # red is maximizing

    def __init__(self, color: ChipColors, seed: int = 0):
        super().__init__(color)
        if seed is not None:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()
        self.maximising = self.COLOR_MAP[self.color]

    @staticmethod
    def _get_max_keys(dictionary: Dict[int, float]):
        max_val = dictionary[max(dictionary, key=dictionary.get)]

        max_keys = []
        for key in dictionary.keys():
            if dictionary[key] == max_val:
                max_keys.append(key)
        return max_keys

    @staticmethod
    def _get_min_keys(dictionary: Dict[int, float]):
        min_val = dictionary[min(dictionary, key=dictionary.get)]
        min_keys = []
        for key in dictionary.keys():
            if dictionary[key] == min_val:
                min_keys.append(key)
        return min_keys

    def move(self, game_state: GameState) -> int:
        move_scores = {}
        is_black_next = self.color == ChipColors.BLACK
        for move in game_state.open_columns():
            child_game = MutableGameState.from_gamestate(game_state,
                                                         is_black_next)
            last_move = child_game.drop_chip(self.maximising, move)
            move_scores[move] = self.eval(child_game, self.DEPTH,
                                          not self.maximising, last_move)
        # Logger().log_buffer(move_scores)
        # print(move_scores)

        if self.maximising:
            return self.random.choice(self._get_max_keys(move_scores))
        else:
            return self.random.choice(self._get_min_keys(move_scores))

    @classmethod
    def eval(cls, game_state: MutableGameState, depth: int,
             maximising_player: bool, last_move: FastMove,
             alpha: float = float('-inf'), beta: float = float('inf')) -> float:
        """
        Minimax algorithm for determining next move.
        Maximizing player is red, minimizing player is black
        :param last_move:
        :param maximising_player:
        :param beta:
        :param alpha:
        :param game_state:
        :param depth:
        :return:
        """
        if depth == 0 or game_state.get_win_state(last_move) is not None:
            return cls._static_eval(game_state, last_move)
        elif maximising_player:
            return cls._max_eval(depth, game_state, alpha, beta)
        else:
            return cls._min_eval(depth, game_state, alpha, beta)

    @classmethod
    def _max_eval(cls, depth: int, game_state: MutableGameState, alpha: float,
                  beta: float) -> float:
        """

        :param depth:
        :param game_state:
        :return:
        """
        max_eval = float('-inf')
        for col in cls.open_columns_sorted(game_state, True):
            move = game_state.drop_chip(True, col)
            move_eval = cls.eval(game_state, depth - 1, False, move, alpha,
                                 beta)
            game_state.undo_fastmove(move)
            max_eval = max(max_eval, move_eval)
            alpha = max(alpha, move_eval)
            if beta <= alpha:
                break
        return max_eval

    @classmethod
    def _min_eval(cls, depth: int, game_state: MutableGameState, alpha: float,
                  beta: float) -> float:
        """

        :param depth:
        :param game_state:
        :return:
        """
        min_eval = float('inf')
        for col in cls.open_columns_sorted(game_state, False):
            move = game_state.drop_chip(False, col)
            move_eval = cls.eval(game_state, depth - 1, True, move, alpha, beta)
            game_state.undo_fastmove(move)
            min_eval = min(min_eval, move_eval)
            beta = min(beta, move_eval)
            if beta <= alpha:
                break
        return min_eval

    @classmethod
    def open_columns_sorted(cls, game_state: MutableGameState,
                            maximising_player: bool) -> List[int]:
        open = game_state.open_columns
        return open

    @classmethod
    @abstractmethod
    def _static_eval(cls, game_state: MutableGameState, last_move: FastMove) -> float:
        raise NotImplementedError()
