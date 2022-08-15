import tensorflow as tf
import csv
import os

def get_data(row):
    # TODO: Build board array from first 42 data entries
    # TODO: Convert board array to normalized ints (0 for opp, 0.5 for empty, 1 for player)
    # TODO: Return tuple of board array and optimal move
    pass

def main():
    board_list = []
    move_list = []
    with open(f'{os.getcwd()}/data/connect-4_improved_random.data', 'r') as f:
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

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())

    model.fit(training_board_list, training_move_list, epochs=10)

    model.evaluate(testing_board_list, testing_move_list)

if __name__ == '__main__':
    main()