import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)
tests = [(100, 212), (11, 51.8), (102.2, 215.96)]


def _plot_losses(history):
    """ # Print the evolution in the fitting stage
    """
    plt.xlabel("# Epoch")
    plt.ylabel("Loss magnitude")
    plt.plot(history.history["loss"])
    plt.show()


def nn_one_to_one():

    layer = tf.keras.layers.Dense(units=1, input_shape=[1])

    model = tf.keras.Sequential([layer])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.1),
        loss="mean_squared_error"
    )

    print("Starting training...")
    history = model.fit(celsius, fahrenheit, epochs=1000, verbose=False)
    print("Model trained!")
    print()

    print("Internal variables of the model:")
    print("\tlayer weights: {}".format(layer.get_weights()))
    print()

    print("Trying with the tests:")
    for cel, far in tests:
        result = model.predict([cel])
        print("\tcelsius: {} -> fahrenheit: {} (expected {})".format(cel, result, far))
    print()

    print("Plotting losses:")
    _plot_losses(history)


def nn_two_hidden_layers():

    hidden_layer_1 = tf.keras.layers.Dense(units=3, input_shape=[1])
    hidden_layer_2 = tf.keras.layers.Dense(units=3)
    output_layer = tf.keras.layers.Dense(units=1)

    model = tf.keras.Sequential([hidden_layer_1, hidden_layer_2, output_layer])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.1),
        loss="mean_squared_error"
    )

    print("Starting training...")
    history = model.fit(celsius, fahrenheit, epochs=1000, verbose=False)
    print("Model trained!")
    print()

    print("Internal variables of the model:")
    print("\thidden_layer_1 weights: {}".format(hidden_layer_1.get_weights()))
    print("\thidden_layer_2 weights: {}".format(hidden_layer_2.get_weights()))
    print("\toutput_layer weights: {}".format(output_layer.get_weights()))
    print()

    print("Trying with the tests:")
    for cel, far in tests:
        result = model.predict([cel])
        print("\tcelsius: {} -> fahrenheit: {} (expected {})".format(cel, result, far))
    print()

    print("Plotting losses. Close the plot window to end the execution.")
    _plot_losses(history)


if __name__ == '__main__':

    nn_two_hidden_layers()
