from connect4.chipcolors import ChipColors
from playables.examplebot.examplebot import ExampleBot
from playables.joshw.smarterminimax.smarterminimax import SmarterMinimax
from playables.joshw.smartminimax.smartminimax import SmartMinimax
from terminalrunner.outputter import Outputter
from terminalrunner.runner import Runner

if __name__ == '__main__':
    output = Outputter()
    runner = Runner(output)
    stats = runner.run_tournament([
        SmartMinimax,
        SmarterMinimax,
        ExampleBot
    ],
    )
    # stats = runner.run_match(SmartMinimax(ChipColors.RED),
    #                          SmarterMinimax(ChipColors.BLACK),
    #                          rounds=10, output_turns=True,
    #                          output_wins=False)
