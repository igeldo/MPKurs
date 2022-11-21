import numpy as np
from skimage import data, io
from matplotlib import pyplot as plt
import tensorflow as tf
import os

def load_images():

    #base_path = "./data"
    #img = io.imread(base_path + "/augmenteddata/MildDemented/0a0a0acd-8bd8-4b79-b724-cc5711e83bc7.jpg")
    #io.imshow(img)
    #io.show()

    #print(np.mean(img))
    print(os.environ.get('USERNAME'))
    if (os.environ.get('USERNAME') == 'kubic'):
        path_alzheimer_folder = 'C:\\Users\\kubic\\Documents\\Alzheimer'
    elif (os.environ.get('USERNAME') == 'ivono'):
        if (os.path.exists('D:\FH\Master Dortmund\Programmierprojekt')):
            path_alzheimer_folder = 'D:\\FH\\Master Dortmund\\Programmierprojekt\\Alzheimer'
        else:
            path_alzheimer_folder = 'C:\\Users\\ivono\\FH\\Programmierkurs\\Alzheimer'
    print(path_alzheimer_folder)

if __name__ == '__main__':

    print("Hello World")

    load_images()