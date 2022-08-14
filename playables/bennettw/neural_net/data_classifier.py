import csv 
import os

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
        return value

def get_data(row):
    return BoardData([[row[5], row[11], row[17], row[23], row[29], row[35], row[41]],
                      [row[4], row[10], row[16], row[22], row[28], row[34], row[40]],
                      [row[3], row[9], row[15], row[21], row[27], row[33], row[39]],
                      [row[2], row[8], row[14], row[20], row[26], row[32], row[38]],
                      [row[1], row[7], row[13], row[19], row[25], row[31], row[37]],
                      [row[0], row[6], row[12], row[18], row[24], row[30], row[36]]], row[42])

board_list = []

with open(f'{os.getcwd()}/data/connect-4.data', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        board_list.append(get_data(row))

print(board_list[0])

# TODO: Classify boards by obtaining best move