from terminalrunner.outputter import Outputter
from terminalrunner.runner import Runner

if __name__ == '__main__':
    output = Outputter()
    runner = Runner(output)
    stats = runner.run_tournament(runner.get_all_playables(),
                                  rounds_per_match=10)
