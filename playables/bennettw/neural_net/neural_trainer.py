import tensorflow as tf

def main():
    # TODO: add the dataset/game logic
    # TODO: Normalize the input data (convert to -1 for opp, 0 for empty, 1 for player) (then normalize to 0-1)

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(6,7)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(7)
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError())

    # model.fit(x, y, epochs=10)

    # model.evaluate(x, y)

if __name__ == '__main__':
    main()