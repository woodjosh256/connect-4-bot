import random
from abc import abstractmethod
from typing import Dict, List

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable


class Minimax(Playable):
    MAXIMISING_COLOR = ChipColors.RED
    MINIMISING_COLOR = ChipColors.BLACK
    DEPTH = 5

    def __init__(self, color: ChipColors, seed: int = 0):
        super().__init__(color)
        if seed is not None:
            self.random = random.Random(seed)
        else:
            self.random = random.Random()

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
        for move in game_state.open_columns():
            child_game = game_state.drop_chip(self.color, move)
            move_scores[move] = self.eval(child_game, self.DEPTH,
                                          self.color.get_opposing_color())
        # Logger().log_buffer(move_scores)

        if self.color == self.MAXIMISING_COLOR:
            return self.random.choice(self._get_max_keys(move_scores))
        else:
            return self.random.choice(self._get_min_keys(move_scores))

    @classmethod
    def eval(cls, game_state: GameState, depth: int, color: ChipColors,
             alpha: float = float('-inf'), beta: float = float('inf')) -> float:
        """
        Minimax algorithm for determining next move.
        Maximizing player is red, minimizing player is black
        :param beta:
        :param alpha:
        :param game_state:
        :param depth:
        :param color:
        :return:
        """
        if depth == 0 or game_state.get_win_state() is not None:
            return cls._static_eval(game_state)
        elif color == cls.MAXIMISING_COLOR:
            return cls._max_eval(depth, game_state, alpha, beta)
        elif color == cls.MINIMISING_COLOR:
            return cls._min_eval(depth, game_state, alpha, beta)
        else:
            raise ValueError(f"Cannot score game state for {color}")

    @classmethod
    def _max_eval(cls, depth: int, game_state: GameState, alpha: float,
                  beta: float) -> float:
        """

        :param depth:
        :param game_state:
        :return:
        """
        max_eval = float('-inf')
        for sub_game in cls._get_child_games(game_state, cls.MAXIMISING_COLOR,
                                             True):
            move_eval = cls.eval(sub_game, depth - 1, cls.MINIMISING_COLOR,
                                 alpha, beta)
            max_eval = max(max_eval, move_eval)
            alpha = max(alpha, move_eval)
            if beta <= alpha:
                break
        return max_eval

    @classmethod
    def _min_eval(cls, depth: int, game: GameState, alpha: float,
                  beta: float) -> float:
        """

        :param depth:
        :param game:
        :return:
        """
        min_eval = float('inf')
        for sub_game in cls._get_child_games(game, cls.MINIMISING_COLOR, False):
            move_eval = cls.eval(sub_game, depth - 1, cls.MAXIMISING_COLOR,
                                 alpha, beta)
            min_eval = min(min_eval, move_eval)
            beta = min(beta, move_eval)
            if beta <= alpha:
                break
        return min_eval

        # evals = []
        # for sub_game in cls._get_child_games(game, cls.MAXIMISING_COLOR):
        #     evals.append(cls.eval(sub_game, depth - 1, cls.MAXIMISING_COLOR))
        # return mean(evals)

    @classmethod
    def _get_child_games(cls, game_state: GameState, color: ChipColors,
                         maximising_player: bool) -> List[GameState]:
        child_games = []
        for open_col in game_state.open_columns():
            child_games.append(game_state.drop_chip(color, open_col))
        
        if maximising_player:
            child_games.sort(reverse=True, key=lambda s: cls._static_eval(s))
        else:
            child_games.sort(key=lambda s: cls._static_eval(s))

        return child_games

    @classmethod
    @abstractmethod
    def _static_eval(cls, game_state: GameState) -> float:
        raise NotImplementedError
