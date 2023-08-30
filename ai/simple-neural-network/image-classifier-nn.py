"""

Source:

    https://www.youtube.com/watch?v=j6eGHROLKP8

"""

import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
import tensorflow as tf
import numpy as np
import math


# Get dataset with cloth images and 10 labels to classify them
# This dataset provides 60000 training images and 10000 testing images
dataset, metadata = tfds.load("fashion_mnist", as_supervised=True, with_info=True)
classifying_labels = metadata.features['label'].names

# Define a size to split dataset into batches during training
BATCH_SIZE = 32

print("Labels for the classifier: {}".format(classifying_labels))
print("Metadata of the dataset:")
print(metadata)
print()


def _normalize_pixels(image, labels):
    """ Normalize image data (from 0-255 to 0-1).

    NOTES:

        - 'image' is an instance of <class 'tensorflow.python.framework.ops.Tensor'>. This class represents an
            n-dimensional array of values

        - The function 'cast' transforms all the values in a Tensor according to the output type provided (in that
            case, 'float32')

    """
    image_casted = tf.cast(image, tf.float32)
    image_casted /= 255  # Transformation
    return image_casted, labels


def _plot_losses(train_history):
    """ Plot the evolution in the fitting stage. This function plots the evolution of the loss count as the training
    process progresses.

    NOTES:

        - This information is returned by the function 'fit' (training function).

    """
    plt.xlabel("# Epoch")
    plt.ylabel("Loss magnitude")
    plt.plot(train_history.history["loss"])
    plt.show()


def _plot_images(tensor_images, n=25):
    """ Plot the first 'n' images of the array provided (with its corresponding label).
    """
    plt.figure(figsize=(10, 10))
    for idx, (image, label) in enumerate(tensor_images.take(n)):
        image = image.numpy().reshape((n+3, n+3))
        plt.subplot(5, 5, idx + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(image, cmap=plt.cm.binary)
        plt.xlabel(classifying_labels[label])
    plt.show()


def _plot_predicts(input_images, test_labels, predicts, rows=5, cols=5):
    """ Plot a table with 'rows*cols' images and their corresponding predicts (after being provided by the model
    already trained). Each table cell contains an image, its predicted label, its confidence percentage, its actual
    label and a chart measuring the success of the prediction.
    """

    def plot_image(idx, arr_predicts, actual_labels, images):
        arr_predict, actual_label, img = arr_predicts[idx], actual_labels[idx], images[idx]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(img[..., 0], cmap=plt.cm.binary)

        predicted_label = np.argmax(arr_predict)
        color = "blue" if predicted_label == actual_label else "red"

        plt.xlabel("{} {:2.0f}% ({})".format(
            classifying_labels[predicted_label], 100 * np.max(arr_predict), classifying_labels[actual_label]), color=color)

    def plot_chart(idx, arr_predicts, actual_labels):
        arr_predict, actual_label = arr_predicts[idx], actual_labels[idx]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        chart = plt.bar(range(10), arr_predict, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(arr_predict)

        chart[predicted_label].set_color("red")
        chart[actual_label].set_color("blue")

    num_imagenes = rows * cols
    plt.figure(figsize=(2 * 2 * cols, 2 * rows))
    for i in range(num_imagenes):
        plt.subplot(rows, 2 * cols, 2 * i + 1)
        plot_image(i, predicts, test_labels, input_images)
        plt.subplot(rows, 2 * cols, 2 * i + 2)
        plot_chart(i, predicts, test_labels)
    plt.show()


def _preprocess_training_data(training, testing, num_training_examples, num_testing_examples):
    """ Prepare the provided data to the training and testing proceses. This function executes three transformations:

        1. Normalize the image data. The value of each pixel (0-255) is set between 0 and 1 instead.

        2. Cache all data to be ready for training.

        3. TODO

    """
    # Normalize data (from 0-255 to 0-1)
    training_normalized = training.map(_normalize_pixels)
    testing_normalized = testing.map(_normalize_pixels)

    # Add dataset to cache
    training_normalized_cached = training_normalized.cache()
    testing_normalized_cached = testing_normalized.cache()

    # Split data into batches randomly
    training_normalized_cached_batched = training_normalized_cached.repeat().shuffle(num_training_examples).batch(BATCH_SIZE)
    testing_normalized_cached_batched = testing_normalized_cached.batch(BATCH_SIZE)

    return training_normalized_cached_batched, testing_normalized_cached_batched


def two_hidden_relu():

    training_data, testing_data = dataset["train"], dataset["test"]
    num_training_examples = metadata.splits["train"].num_examples
    num_testing_examples = metadata.splits["test"].num_examples

    # Preprocess dataset
    training_data, testing_data = _preprocess_training_data(training_data, testing_data, num_training_examples, num_testing_examples)

    # Create the model
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=[28, 28, 1]),  # 1 = black and white
        tf.keras.layers.Dense(units=50, activation=tf.nn.relu),
        tf.keras.layers.Dense(units=50, activation=tf.nn.relu),
        tf.keras.layers.Dense(units=10, activation=tf.nn.softmax),  # To classifiers. Outputs values always sum 1
    ])

    # Compile the model
    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"]
    )

    # Training
    print("Training model...")
    history = model.fit(training_data, epochs=5, steps_per_epoch=math.ceil(num_training_examples/BATCH_SIZE))

    # Predict testing data
    print("Predicting first batch of testing data...")
    for test_image, test_label in testing_data.take(1):
        test_image = test_image.numpy()
        test_label = test_label.numpy()
        predict = model.predict(test_image)

    print("Plotting results... (Close the plot window to end the execution)")
    _plot_predicts(test_image, test_label, predict)


if __name__ == '__main__':
    two_hidden_relu()
