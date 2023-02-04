import numpy as np
from matplotlib import pyplot as plt

from Database import Database
from NeuralNetwork import NeuralNetwork

if __name__ == '__main__':
    # create class Database
    db = Database()
    db.get_image_path()
    db.connection()
    db.create_table()
    db.send_files_to_postgresql()

    train_images, train_labels = db.get_train_files_from_postgresql()
    test_images, test_labels = db.get_test_files_from_postgresql()

    # show images
    plt.figure()
    plt.imshow(train_images[0])
    print("Label: ", train_labels[0])
    plt.grid(False)
    plt.show()

    plt.figure()
    plt.imshow(test_images[0])
    print("Label: ", test_labels[0])
    plt.grid(False)
    plt.show()

    # create class NeuralNetwork
    network = NeuralNetwork(train_images, train_labels, test_images, test_labels)
    network.define_model_CNN()
    history = network.compile_fit_CNN(network.traindata, network.traindata_label)
    network.evaluate()
    network.predict()
