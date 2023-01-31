from skimage import data, io
from matplotlib import pyplot as plt
import pickle
import numpy as np
import tensorflow as tf
from Database import Database

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image

from tensorflow.image import rgb_to_grayscale
from tensorflow.image import grayscale_to_rgb

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras import optimizers, losses
import seaborn as sns
import matplotlib.pyplot as plt

# Metrics
from sklearn.metrics import classification_report, confusion_matrix
import itertools

class NeuralNetwork:

    def __init__(self): #, traindata, testdata):

        db = Database()
        db.connection()

        print("before")
        train_images, train_labels = db.get_train_files_from_postgresql()
        test_images, test_labels = db.get_test_files_from_postgresql()
        print("after")

        # in init schon einlesen? # ja
        self.traindata = self.rescale(train_images)
        self.traindata_label = np.array(train_labels)

        self.testdata = self.rescale(test_images)
        self.testdata_label = np.array(test_labels)


    def define_model_CNN(self):

        model = tf.keras.models.Sequential([
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
        return model

    def compile_fit_CNN(self, model, train_images, train_labels):

        model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
        history = model.fit(train_images, train_labels,
                            epochs=2,
                            batch_size=32,
                            shuffle=True)

        return history


    def rescale(self, images):

        rescaled_images = np.array(images)/255.0

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

        model = network.define_model_CNN()
        history = network.compile_fit_CNN(model, network.traindata, network.traindata_label)

        print(history)

        print("Evaluate model on test data")
        results = model.evaluate(network.testdata, network.testdata_label, batch_size=128)
        print("test loss, test acc:", results)

        # Generate a prediction using model.predict()
        # and calculate it's shape:
        print("Generate a prediction")
        prediction = model.predict(network.testdata[:1])
        print("prediction shape:", prediction.shape)