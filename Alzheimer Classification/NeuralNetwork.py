# import other class
from Database import Database

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras import optimizers, losses

class NeuralNetwork:

    def __init__(self, train_images, train_labels, test_images, test_labels):

        self.traindata = self.rescale(train_images)
        self.traindata_label = np.array(train_labels)

        self.testdata = self.rescale(test_images)
        self.testdata_label = np.array(test_labels)

        self.model = None

    def define_model_CNN(self):
        """
        define model with different layer
        """
        self.model = tf.keras.models.Sequential([
            Conv2D(16, (3, 3), activation='relu', input_shape=(180, 180, 1)),  # 224, 224, 3
            MaxPooling2D(2, 2),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.2),
            Dense(1, activation='softmax')
        ])

    def compile_fit_CNN(self, train_images, train_labels):
        """
        compile and fit model with train data
        """
        self.model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
        history = self.model.fit(train_images, train_labels,
                            epochs=1,
                            batch_size=32,
                            shuffle=True)

        return history

    def evaluate(self):
        """
        evaluate model on test data
        """
        print("Evaluate model on test data")
        results = self.model.evaluate(self.testdata, self.testdata_label, batch_size=128)
        print("test loss, test acc:", results)

    def predict(self):
        """
        Generate a prediction using model.predict() and calculate it's shape:
        """
        print("Generate a prediction")
        prediction = self.model.predict(self.testdata[:1])
        print("prediction shape:", prediction.shape)

    def rescale(self, images):
        """
        rescale (norm) images to 0 - 1
        """
        rescaled_images = np.array(images) / 255.0

        return rescaled_images


if __name__ == '__main__':
    network = NeuralNetwork()

    # plt.figure()
    # plt.imshow(network.traindata[0])
    # print(np.mean(network.traindata[0]))
    # print("Label: ", network.traindata_label[0])
    # plt.grid(False)
    # plt.show()
    #
    # plt.figure()
    # plt.imshow(network.testdata[0])
    # print(np.mean(network.testdata[0]))
    # print("Label: ", network.testdata_label[0])
    # plt.grid(False)
    # plt.show()

    network.define_model_CNN()
    history = network.compile_fit_CNN(network.traindata, network.traindata_label)
    network.evaluate()
    network.predict()

    print(history)



