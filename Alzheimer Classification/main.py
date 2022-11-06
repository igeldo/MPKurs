import numpy as np
from skimage import data, io
from matplotlib import pyplot as plt
import tensorflow as tf

def load_images():

    base_path = "./data"
    img = io.imread(base_path + "/augmenteddata/MildDemented/0a0a0acd-8bd8-4b79-b724-cc5711e83bc7.jpg")
    io.imshow(img)
    io.show()

    print(np.mean(img))


if __name__ == '__main__':

    print("Hello World")

    load_images()