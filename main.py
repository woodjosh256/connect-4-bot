from game.game import ChipColors
from terminalrunner.playables.randombot import RandomBot
from terminalrunner.runner import Runner

if __name__ == '__main__':
    win_stats = Runner.run_match(RandomBot(ChipColors.BLACK),
                                 RandomBot(ChipColors.RED),
                                 1000, False, False)
    print(win_stats)
