import random
from abc import abstractmethod
from copy import deepcopy
from typing import Dict, List

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
from playables.joshw.MutableGameState import MutableGameState, FastMove
from playables.transpositiontable import TranspositionTable


class MinimaxWithCaching(Playable):
    MAXIMISING_COLOR = ChipColors.RED
    MINIMISING_COLOR = ChipColors.BLACK
    DEPTH = 8
    MAX_SORT_DEPTH = 3

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

        self.transposition_table = TranspositionTable()
        self.starting = None

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

    def score_move(self, game_state: GameState, move: int, depth: int):
        is_black_next = self.color == ChipColors.BLACK
        child_game = MutableGameState.from_gamestate(game_state,
                                                     is_black_next)
        last_move = child_game.drop_chip(self.maximising, move)
        return self.eval(child_game, self.DEPTH, not self.maximising, last_move)

    def move(self, game_state: GameState) -> int:
        if self.starting is None:
            if len(game_state.moves) == 0:
                self.starting = True
            else:
                self.starting = False

        move_scores = {}
        # for depth in range(1, self.DEPTH):
        for move in game_state.open_columns():
            score = self.score_move(game_state, move, self.DEPTH)
            move_scores[move] = score

        # Logger().log_buffer(move_scores)
        # print(move_scores)

        if self.maximising:
            return self.random.choice(self._get_max_keys(move_scores))
        else:
            return self.random.choice(self._get_min_keys(move_scores))

    def eval(self, game_state: MutableGameState, depth: int,
             maximising_player: bool, last_move: FastMove,
             alpha: float = float('-inf'),
             beta: float = float('inf')) -> float:
        cached = self.transposition_table.get_eval(game_state.get_hash())
        if cached is not None and cached.depth >= depth:
            return cached.score
        else:
            score = self._calc_eval(game_state, depth, maximising_player,
                                  last_move, alpha, beta)
            self.transposition_table.cache_eval(game_state.get_hash(), score,
                                                depth)
            return score

    def _calc_eval(self, game_state: MutableGameState, depth: int,
                   maximising_player: bool, last_move: FastMove,
                   alpha: float, beta: float) -> float:
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
            return self._static_eval(game_state, last_move)
        elif maximising_player:
            return self._max_eval(depth, game_state, alpha, beta, last_move)
        else:
            return self._min_eval(depth, game_state, alpha, beta, last_move)

    def _max_eval(self, depth: int, game_state: MutableGameState, alpha: float,
                  beta: float, last_move: FastMove) -> float:
        """

        :param depth:
        :param game_state:
        :return:
        """
        max_eval = float('-inf')
        for col in self.open_columns_sorted(game_state, depth, True, last_move):
            move = game_state.drop_chip(True, col)
            move_eval = self.eval(game_state, depth - 1, False, move, alpha,
                                  beta)
            game_state.undo_fastmove(move)
            max_eval = max(max_eval, move_eval)
            alpha = max(alpha, move_eval)
            if beta <= alpha:
                break
        return max_eval

    def _min_eval(self, depth: int, game_state: MutableGameState, alpha: float,
                  beta: float, last_move: FastMove) -> float:
        """

        :param depth:
        :param game_state:
        :return:
        """
        min_eval = float('inf')
        for col in self.open_columns_sorted(game_state, depth, False, last_move):
            move = game_state.drop_chip(False, col)
            move_eval = self.eval(game_state, depth - 1, True, move, alpha,
                                  beta)
            game_state.undo_fastmove(move)
            min_eval = min(min_eval, move_eval)
            beta = min(beta, move_eval)
            if beta <= alpha:
                break
        return min_eval

    def _sort_eval(self, game_state: MutableGameState, col: int,
                   maximising_player: bool, last_move: FastMove) -> float:
        move = game_state.drop_chip(maximising_player, col)
        cached = self.transposition_table.get_eval(game_state.get_hash())
        game_state.undo_fastmove(move)
        if cached is not None:
            return cached.score
        else:
            return self._static_eval(game_state, last_move)

    def open_columns_sorted(self, game_state: MutableGameState, depth: int,
                            maximising_player: bool,
                            last_move: FastMove) -> List[int]:
        if depth > self.MAX_SORT_DEPTH:
            open_columns = deepcopy(game_state.open_columns)
            open_columns.sort(
                reverse=maximising_player,
                key=lambda col: self._sort_eval(game_state, col, maximising_player,
                                                last_move))
            return open_columns
        else:
            return game_state.open_columns

    def new_game(self) -> None:
        self.starting = None

    @abstractmethod
    def _static_eval(self, game_state: MutableGameState, last_move: FastMove) -> float:
        raise NotImplementedError()
