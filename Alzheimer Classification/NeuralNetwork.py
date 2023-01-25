from skimage import data, io
from matplotlib import pyplot as plt
import pickle
import numpy as np
import tensorflow as tf
import Database

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

class NeuralNetwork:

    def __init__(self, traindata, testdata):

        db = Database()
        db.connection()

        train_images, train_labels = db.get_train_files_from_postgresql()
        test_images, test_labels = db.get_test_files_from_postgresql()

        # in init schon einlesen?
        self.traindata = train_images
        self.traindata_label = train_labels

        self.testdata = test_images
        self.testdata_label = test_labels


    def load_images(self, images):

        return images

    def load_images_to_database(self, database_access):

        # algorithm to upload data

        return database_access

    def get_images_from_database(self, database_access, layer):

        # algorithm to
        t = database_access

        return t, layer


