import numpy as np
from skimage import data, io
from matplotlib import pyplot as plt
#import tensorflow as tf
import os

from Database import Database
from NeuralNetwork import NeuralNetwork

if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    db.connection()
    print("Connection established")
    db.create_table()
    print("Table created")
    db.send_files_to_postgresql()
    print("All files uploaded")

    print("before")
    train_images, train_labels = db.get_train_files_from_postgresql()
    test_images, test_labels = db.get_test_files_from_postgresql()
    print("after")

    # show images
    # plt.figure()
    # plt.imshow(network.train_images[0])
    # print("Label: ", network.train_labels[0])
    # plt.grid(False)
    # plt.show()
    #
    # plt.figure()
    # plt.imshow(network.test_images[0])
    # print("Label: ", network.test_labels[0])
    # plt.grid(False)
    # plt.show()

    network = NeuralNetwork(train_images, train_labels, test_images, test_labels)
    network.define_model_CNN()
    print("model defined")
    history = network.compile_fit_CNN(network.traindata, network.traindata_label)
    network.evaluate()
    print("evaluate done")
    network.predict()
    print("prediction done")