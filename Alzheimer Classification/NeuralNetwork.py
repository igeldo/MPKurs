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

        train_images, train_labels = db.get_train_files_from_postgresql()
        test_images, test_labels = db.get_test_files_from_postgresql()

        # in init schon einlesen? # ja
        self.traindata = self.rescale(train_images)
        self.traindata_label = train_labels

        self.testdata = self.rescale(test_images)
        self.testdata_label = test_labels


    def define_model_CNN(self):

        model = tf.keras.models.Sequential([
            Conv2D(16, (3, 3), activation='relu', input_shape=(208, 176, 1)),  # 224, 224, 3
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
            Dense(4, activation='softmax')
        ])
        return model

    def compile_fit_CNN(self, model, train_images, train_labels):

        model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
        history = model.fit(train_images, train_labels, epochs=10)


    def rescale(self, images):
        datagen = ImageDataGenerator(rescale=1.0/255)
        rescaled_images = datagen.flow(images,
                            batch_size=1)
        return rescaled_images


if __name__ == '__main__':

        network = NeuralNetwork()

        model = network.define_model_CNN()
        network.compile_fit_CNN(model, network.traindata, network.traindata_label)
