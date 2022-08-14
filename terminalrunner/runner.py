import importlib
import pkgutil
from itertools import combinations
from timeit import default_timer as timer
from typing import List, Type

import playables as playables
from connect4.game import Game, ChipColors
from connect4.playable import Playable
from connect4.winstates import WinStates
from playables.joshw.logger import Logger
from terminalrunner.matchstats import MatchStats
from terminalrunner.outputable import Outputable
from terminalrunner.roundstats import RoundStats


class Runner:

    def __init__(self, output: Outputable):
        self.output = output

    # todo - add turn time limit
    def run_round(self, playable1: Playable, playable2: Playable,
                  p1starts: bool, output_turns: bool = True,
                  output_wins: bool = True) -> RoundStats:
        game = Game()
        stats = RoundStats(
            playable1=playable1,
            playable2=playable2
        )
        turn = 0
        while game.get_win_state() is None:
            start_time = timer()
            if (turn % 2 == 0 and p1starts) or (turn % 2 != 0 and not p1starts):
                move = playable1.move(game.state)
                stats.p1_move_times.append(timer() - start_time)
                game.drop_chip(playable1.color, move)
            else:
                move = playable2.move(game.state)
                stats.p2_move_times.append(timer() - start_time)
                game.drop_chip(playable2.color, move)

            if output_turns:
                self.output.output_board(game.state)

            turn += 1

        stats.win_state = game.get_win_state()

        if output_wins:
            self.output.output_round_end(stats, game.state)

        # if game.get_win_state() == WinStates.BLACK:
        #     print("printing buffer")
        #     print(Logger().buffer)
        # Logger().buffer = ""

        return stats

    def run_match(self, playable1: Playable, playable2: Playable,
                  rounds: int = 100, output_turns: bool = True,
                  output_wins: bool = True) -> MatchStats:
        match_stats = MatchStats(playable1, playable2)

        playable1_starts = True
        for i in range(rounds):
            win_state = self.run_round(playable1, playable2, playable1_starts,
                                       output_turns, output_wins)
            match_stats.add_round(win_state)
            playable1_starts = not playable1_starts

        return match_stats

    @staticmethod
    def _import_submodules(package, recursive=True):
        """ Import all submodules of a module, recursively,
        including subpackages
        :param package: package (name or actual module)
        :type package: str | module
        :rtype: dict[str, types.ModuleType]
        """
        if isinstance(package, str):
            package = importlib.import_module(package)
        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(Runner._import_submodules(full_name))
        return results

    @staticmethod
    def get_all_playables() -> List[Type[Playable]]:
        """
        :return: list of all playables within playables folder (or
        sub-folders).
        """
        Runner._import_submodules(playables)
        return Playable.__subclasses__()

    def run_tournament(self, playable_classes: List[Type[Playable]],
                       rounds_per_match: int = 100, output_turns: bool = True,
                       output_wins: bool = True):
        match_stats_list = []

        playable_matchups = combinations(playable_classes, 2)

        for playable_matchup in playable_matchups:
            red_player = playable_matchup[0](ChipColors.RED)
            black_player = playable_matchup[1](ChipColors.BLACK)

            match_stats = self.run_match(red_player, black_player,
                                         rounds_per_match, output_turns,
                                         output_wins)
            match_stats_list.append(match_stats)
    

