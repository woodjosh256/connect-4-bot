from copy import copy
import random
from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from connect4.playable import Playable
import tensorflow as tf
import os

class NeuralPlayer(Playable):

    def __init__(self, color: ChipColors):
        super().__init__(color)
        module_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.normpath(os.path.join(module_path, 'data', 'connect-4_improved_random_10000.h5'))
        self.model = tf.keras.models.load_model(model_path)

    def move(self, game_state: GameState) -> int:
        converted_data = self._convert_board_data(game_state)
        prediction = self.model.predict([converted_data], verbose=0)[0].argmax()
        return prediction if prediction in game_state.open_columns() else random.choice(game_state.open_columns())

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Neural Net"

    def _convert_board_data(self, game_state: GameState) -> list:
        board_data = copy(game_state.state)
        board_data = list([list(le) for le in board_data])
        for i, row in enumerate(board_data):
            for j, entry in enumerate(row):
                if entry == ChipColors.RED:
                    board_data[i][j] = 1
                elif entry == ChipColors.BLACK:
                    board_data[i][j] = 0
                else:
                    board_data[i][j] = 0.5
        return board_data
