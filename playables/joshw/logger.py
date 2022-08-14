from typing import Dict, List


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):

    ENABLED = True

    def __init__(self):
        self.logs: Dict[str, List[str]] = {}
        self.buffer = ""

    def log(self, category: str, log_msg: str):
        if category in self.logs:
            self.logs[category].append(log_msg)
        else:
            self.logs[category] = [log_msg]

    def log_buffer(self, log_msg: object = "", newline: str = "\n"):
        self.buffer += str(log_msg) + newline
