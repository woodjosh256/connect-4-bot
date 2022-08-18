from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class StateEval:
    depth: int
    score: float


class TranspositionTable:

    MAX_CACHED_ENTRIES: int = 40000000
    PERCENT_TO_DROP = .2

    def __init__(self):
        self.table: Dict[int, StateEval] = {}
        self.drop_amount = int(self.MAX_CACHED_ENTRIES * self.PERCENT_TO_DROP)

    def get_eval(self, state_hash: int) -> Optional[StateEval]:
        if state_hash in self.table:
            return self.table[state_hash]

        return None

    def cache_eval(self, state_hash: int, score: float, depth: int):
        if state_hash in self.table:
            self.table.pop(state_hash)
        self.table[state_hash] = StateEval(depth=depth, score=score)

        if len(self.table) > self.MAX_CACHED_ENTRIES:
            print("reached max")
            self.table = {key: val
                          for (key, val), i in
                          zip(self.table.items(), range(self.drop_amount))
                          if i > self.drop_amount}
