from copy import deepcopy
from dataclasses import dataclass
import importlib
from itertools import combinations
import pkgutil

from game.game import Game, WinStates, ChipColors
from game.playable import Playable
from terminalrunner.matchstats import MatchStats
from terminalrunner.outputter import Outputter
from terminalrunner.playables.randombot import RandomBot
import terminalrunner.playables as playables


class Runner:

    # todo - add turn time limit

    @staticmethod
    def run_round(playable1: Playable, playable2: Playable,
                  output_turns: bool = True,
                  output_wins: bool = True) -> WinStates:
        game = Game()
        turn = 0

        while game.get_win_state() is None:
            state = deepcopy(game.state)
            if turn % 2 == 0:
                move = playable1.move(state, game.open_columns(), game.moves)
                game.insert_chip(playable1.color, move)
            else:
                move = playable2.move(state, game.open_columns(), game.moves)
                game.insert_chip(playable2.color, move)

            if output_turns:
                Outputter.output_board(game.state)

            turn += 1

        win_state = game.get_win_state()

        if output_wins:
            Outputter.output_board(game.state)
            Outputter.output_results(win_state)

        return win_state

    @staticmethod
    def run_match(playable1: Playable, playable2: Playable, rounds: int = 100,
                  output_turns: bool = True,
                  output_wins: bool = True) -> MatchStats:
        match_stats = MatchStats(playable1, playable2)

        for i in range(rounds):
            win_state = Runner.run_round(playable1, playable2, output_turns, output_wins) \
                    if i % 2 == 0 else \
                    Runner.run_round(playable2, playable1, output_turns, output_wins)
            match_stats.add_round(win_state)

        return match_stats

    @staticmethod
    def _import_submodules(package, recursive=True):
        """ Import all submodules of a module, recursively, including subpackages
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
    def run_tournament(rounds_per_match: int = 100, output_turns: bool = True, output_wins: bool = True):
        # Import all playable classes
        Runner._import_submodules(playables)
        playable_classes = Playable.__subclasses__()
        tournament_stats = []

        playable_matchups = combinations(playable_classes, 2)

        for playable_matchup in playable_matchups:
            red_player = playable_matchup[0](ChipColors.RED)
            black_player = playable_matchup[1](ChipColors.BLACK)

            match_stats = Runner.run_match(red_player, black_player, rounds_per_match, output_turns, output_wins)
            tournament_stats.append((playable_matchup[0], playable_matchup[1], match_stats))
    
        return tournament_stats