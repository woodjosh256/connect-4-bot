from connect4.chipcolors import ChipColors
from playables.examplebot.examplebot import ExampleBot
from playables.joshw.basicminimax.basicminimax import BasicMinimax, \
    BasicMinimax2
from terminalrunner.outputter import Outputter
from terminalrunner.runner import Runner

if __name__ == '__main__':
    output = Outputter()
    runner = Runner(output)
    stats = runner.run_match(BasicMinimax2(ChipColors.RED),
                             ExampleBot(ChipColors.BLACK),
                             rounds=2, output_turns=True,
                             output_wins=False)
    output.output_match_stats(stats)

