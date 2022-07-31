import importlib
import pkgutil
from itertools import combinations
from copy import deepcopy
from game.chipcolors import ChipColors
from game.game import Game
from game.outputable import Outputable
from game.playable import Playable
import game.playables as playables

def _play_game(red_player: Playable, black_player: Playable, starting_color: ChipColors = ChipColors.RED, output_moves: bool = False) -> Game:
    game = Game()
    outputable = Outputable()

    if output_moves:
        print("Welcome to Connect Four!")

    player_next_turn = starting_color

    while game.win_state is None:
        try:
            if player_next_turn == ChipColors.RED:
                game.insert_chip(player_next_turn, red_player.move(deepcopy(game.board_state), Game.open_columns(game.board_state), deepcopy(game.prev_moves)))
            else:
                game.insert_chip(player_next_turn, black_player.move(deepcopy(game.board_state), Game.open_columns(game.board_state), deepcopy(game.prev_moves)))
        except ValueError as e:
            if output_moves:
                print("An invalid move was selected. Game forfeit.")
            game.win_state = Game.WinStates.RED if player_next_turn == ChipColors.RED else Game.WinStates.BLACK
            break

        player_next_turn = ChipColors.BLACK if player_next_turn == ChipColors.RED else ChipColors.RED
        if output_moves:
            print(f"{'Red' if player_next_turn == ChipColors.RED else 'Black'}'s turn:")
            outputable.output_board(game.board_state)
            print()
    
    if output_moves:
        print("Game over!")
        if game.win_state == game.WinStates.TIE:
            print("It's a tie!")
        else:
            print(f"{'Red' if game.win_state == game.WinStates.RED else 'Black'} wins!")
        outputable.output_board(game.board_state)

    return game

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
            results.update(_import_submodules(full_name))
    return results

if __name__ == '__main__':
    # Import all playable classes
    _import_submodules(playables)
    playable_classes = Playable.__subclasses__()
    playable_wins = {_cls: 0 for _cls in playable_classes}

    games = combinations(playable_classes, 2)

    for game in games:
        red_player = game[0](ChipColors.RED)
        black_player = game[1](ChipColors.BLACK)

        total_red_wins = 0
        total_black_wins = 0
        total_ties = 0
        for i in range(1000):
            game_result = _play_game(red_player, black_player, starting_color=ChipColors.get_random()).win_state
            if game_result == Game.WinStates.RED:
                total_red_wins += 1
            elif game_result == Game.WinStates.BLACK:
                total_black_wins += 1
            else:
                total_ties += 1

        playable_wins[game[0]] += total_red_wins + (total_ties/2)
        playable_wins[game[1]] += total_black_wins + (total_ties/2)

        print(f"{red_player.get_name()} vs {black_player.get_name()}:")
        print(f"\t{red_player.get_name()} wins: {total_red_wins}")
        print(f"\t{black_player.get_name()} wins: {total_black_wins}")
        print(f"\tTies: {total_ties}")

    for i, playable_entry in enumerate(dict(sorted(playable_wins.items(), key=lambda item: item[1], reverse=True))):
        print(f"#{i+1}: {playable_entry.get_name()} - {playable_wins[playable_entry]}")
