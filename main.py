from game.game import ChipColors
from terminalrunner.playables.randombot import RandomBot
from terminalrunner.runner import Runner

if __name__ == '__main__':
    Runner.benchmark(RandomBot(ChipColors.BLACK),
                     RandomBot(ChipColors.RED))
