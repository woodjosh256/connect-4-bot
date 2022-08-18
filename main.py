from connect4.chipcolors import ChipColors
from playables.examplebot.examplebot import ExampleBot
from playables.joshw.basicminimax.basicminimax import BasicMinimax, \
    BasicMinimax2
from playables.bennettw.neural_net.neural_player import NeuralPlayer
from playables.bennettw.improvedrandom import ImprovedRandom
from terminalrunner.outputter import Outputter
from terminalrunner.runner import Runner

if __name__ == '__main__':
    output = Outputter()
    runner = Runner(output)
    stats = runner.run_match(NeuralPlayer(ChipColors.RED),
                             ImprovedRandom(ChipColors.BLACK),
                             rounds=100, output_turns=True,
                             output_wins=False)
    output.output_match_stats(stats)

