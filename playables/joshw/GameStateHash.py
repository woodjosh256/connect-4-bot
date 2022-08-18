import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GameStateHash:
    # note - all references to game_state are of type MutableGameState.
    # Could not include for type hinting due to circular import

    # stores 2 matrixes holding random ints.
    # Matrix 0 - BLACK, Matrix 1 - RED
    table: List[List[List[int]]]
    is_black_next_bitstring: int
    cur_hash: int

    Z_BITS: int = 64
    SEED: int = 0

    @staticmethod
    def generate(game_state):
        generator = random.Random(GameStateHash.SEED)
        z_table = GameStateHash.make_table(game_state, generator)
        is_black_next_bitstring = generator.getrandbits(GameStateHash.Z_BITS)
        cur_hash = GameStateHash.calc_hash(z_table, is_black_next_bitstring,
                                           game_state)

        return GameStateHash(
            table=z_table,
            is_black_next_bitstring=is_black_next_bitstring,
            cur_hash=cur_hash
        )

    @staticmethod
    def make_table(state, generator: random.Random):
        z_table: List[List[List[int]]] = []
        for player in range(2):
            z_table.append([])
            for row in range(state.rows):
                z_table[player].append([])
                for col in range(state.columns):
                    z_table[player][row].append(
                        generator.getrandbits(GameStateHash.Z_BITS))
        return z_table

    @staticmethod
    def calc_hash(z_table: List[List[List[int]]], is_black_next_bitstring: int,
                  state) -> int:
        cur_hash = 0

        if state.is_black_next:
            cur_hash ^= is_black_next_bitstring

        for row in range(state.rows):
            for col in range(state.columns):
                if state.state[row][col] is True:  # red
                    cur_hash ^= z_table[1][row][col]
                elif state.state[row][col] is False:  # black
                    cur_hash ^= z_table[0][row][col]

        return cur_hash

    def _undo_last(self, row: int, col: int, last_val: bool):
        if last_val is True:
            self.cur_hash ^= self.table[1][row][col]
        elif last_val is False:
            self.cur_hash ^= self.table[0][row][col]

    def update_hash(self, row: int, col: int, last_val: Optional[bool],
                    new_val: Optional[bool]):
        self._undo_last(row, col, last_val)

        if new_val is True:
            self.cur_hash ^= self.table[1][row][col]
        elif new_val is False:
            self.cur_hash ^= self.table[0][row][col]
