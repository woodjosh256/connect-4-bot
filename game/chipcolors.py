from enum import Enum
import random

class ChipColors(Enum):
    RED = 0
    BLACK = 1

    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))
