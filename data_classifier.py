import csv 
import os
from typing import List, AnyStr

from connect4.chipcolors import ChipColors
from connect4.gamestate import GameState
from playables.bennettw.improvedrandom import ImprovedRandom

class BoardData():
    def __init__(self, board, win):
        self.board = board
        self.optimal_move = None
        self.win = win

    def __str__(self):
        value = ""
        for row in self.board:
            value += str(row) + '\n'
        value += "Win: " + str(self.win)
        value += "Move: " + str(self.optimal_move)
        return value

    def get_output_char(self, color: ChipColors) -> AnyStr:
        if color == ChipColors.RED:
            return "R"
        elif color == ChipColors.BLACK:
            return "B"
        else:
            return "X"

    def get_output_line(self):
        output = []
        for row in self.board:
            for col in row:
                output.append(self.get_output_char(col))
        output.extend([self.win, self.optimal_move])
        return output

def get_chip_color(letter: AnyStr, player_color: ChipColors) -> ChipColors:
    if(letter == 'x'):
        return player_color
    elif(letter == 'o'):
        return player_color.get_opposing_color()
    else:
        return None

def convert_data_format(data: List[List[ChipColors]], player_color: ChipColors):
    """
    Convert the data from the dataset to use the ChipColors class
    """
    return [[get_chip_color(data[i][j], player_color) for j in range(len(data[i]))] for i in range(len(data))]

def convert_list_to_tuple(data: List[List[ChipColors]]):
    return tuple([tuple(le) for le in data])

def get_data(row, player_color: ChipColors):
    board_data = [[row[5], row[11], row[17], row[23], row[29], row[35], row[41]],
                      [row[4], row[10], row[16], row[22], row[28], row[34], row[40]],
                      [row[3], row[9], row[15], row[21], row[27], row[33], row[39]],
                      [row[2], row[8], row[14], row[20], row[26], row[32], row[38]],
                      [row[1], row[7], row[13], row[19], row[25], row[31], row[37]],
                      [row[0], row[6], row[12], row[18], row[24], row[30], row[36]]]
    return BoardData(convert_list_to_tuple(convert_data_format(board_data, player_color)), row[42])

def build_game_state(board_data: BoardData) -> GameState:
    return GameState(
            rows=len(board_data.board),
            columns=len(board_data.board[0]),
            winning_number=4,
            state=board_data.board,
            moves=()
        )

def write_to_csv(data: List[BoardData], file_name: str):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row.get_output_line())

board_list = []

color = ChipColors.RED

with open(f'{os.getcwd()}/playables/bennettw/neural_net/data/connect-4.data', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        board_list.append(get_data(row, color))

bot = ImprovedRandom(ChipColors.RED)

for i, board in enumerate(board_list):
    if(i % 100 == 0):
        print(i)
    board.optimal_move = bot.move(build_game_state(board))

write_to_csv(board_list, f'{os.getcwd()}/playables/bennettw/neural_net/data/connect-4_improved_random.data')