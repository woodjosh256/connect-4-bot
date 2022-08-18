import tensorflow as tf
import csv
import os

def get_data(row):
    board = []
    board.append(row[:7])
    board.append(row[7:14])
    board.append(row[14:21])
    board.append(row[21:28])
    board.append(row[28:35])
    board.append(row[35:42])
    for i, board_row in enumerate(board):
        for j, entry in enumerate(board_row):
            if entry == 'R':
                board[i][j] = 1
            elif entry == 'B':
                board[i][j] = 0
            else:
                board[i][j] = 0.5
    return (board, int(row[43]))

def main():
    board_list = []
    move_list = []
    with open(f'{os.getcwd()}/playables/bennettw/neural_net/data/connect-4_improved_random.data', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            board_data = get_data(row)
            board_list.append(board_data[0])
            move_list.append(board_data[1])

    training_board_list = board_list[:60000]
    training_move_list = move_list[:60000]
    testing_board_list = board_list[60000:]
    testing_move_list = move_list[60000:]

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(6,7)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(7)
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])

    model.fit(training_board_list, training_move_list, epochs=10000, verbose=2)

    model.evaluate(testing_board_list, testing_move_list)

    model.save(f'{os.getcwd()}/playables/bennettw/neural_net/data/connect-4_improved_random_10.h5')

if __name__ == '__main__':
    main()