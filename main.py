import importlib
import pkgutil
from game.chipcolors import ChipColors
from game.game import Game
from game.outputable import Outputable
from game.playable import Playable
import game.playables as playables
from game.playables.BennettW_Random.BennettW_Random import BennettW_Random

def _play_game(red_player: Playable, black_player: Playable, starting_color: ChipColors = ChipColors.RED, output_moves: bool = False) -> Game:
    game = Game()
    outputable = Outputable()

    if output_moves:
        print("Welcome to Connect Four!")

    player_next_turn = starting_color

    while game.win_state is None:
        game.insert_chip(player_next_turn, black_player.move(game.board_state, game.open_columns()))
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
    player_classes = Playable.__subclasses__()
    print(player_classes)

    # TODO: Add matchmaking or bracket logic here
    red_player = BennettW_Random(ChipColors.RED)
    black_player = BennettW_Random(ChipColors.BLACK)

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

    print(f"Red wins: {total_red_wins}")
    print(f"Black wins: {total_black_wins}")
    print(f"Ties: {total_ties}")
