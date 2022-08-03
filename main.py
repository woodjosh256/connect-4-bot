from game.game import ChipColors
from terminalrunner.playables.randombot import RandomBot
from terminalrunner.runner import Runner
from terminalrunner.outputter import Outputter

if __name__ == '__main__':
    tournament_stats = Runner.run_tournament(1000, False, False)

    Outputter.output_tournament_stats(tournament_stats)
