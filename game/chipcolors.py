from enum import Enum
import random

class ChipColors(Enum):
    RED = 0
    BLACK = 1

    @classmethod
    def get_random(cls):
        return random.choice(list(cls.__members__.values()))

    @classmethod
    def get_opposite(cls, color):
        if color == ChipColors.RED:
            return ChipColors.BLACK
        else:
            return ChipColors.RED