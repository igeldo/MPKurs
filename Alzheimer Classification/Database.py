import psycopg2
import psycopg2.extras
import os
from os.path import isfile, join
import numpy as np
import tensorflow as tf
import tempfile
import tensorflow_io as tfio
import pickle
from matplotlib import pyplot as plt


class Database:

    def __init__(self):

        self.hostname = 'localhost'
        self.database = 'alz'
        self.username = 'postgres'
        self.pwd = 'yay_python'
        self.port_id = 5432
        self.conn = None
        self.cur = None
        self.path = None
        self.train_folders = {
            "non": "\\AugmentedAlzheimerDataset\\NonDemented\\",
            "verymild": "\\AugmentedAlzheimerDataset\\VeryMildDemented\\",
            "mild": "\\AugmentedAlzheimerDataset\\MildDemented\\",
            "moderate": "\\AugmentedAlzheimerDataset\\ModerateDemented\\"
        }
        self.test_folders = {
            "non": "\\OriginalDataset\\NonDemented\\",
            "verymild": "\\OriginalDataset\\VeryMildDemented\\",
            "mild": "\\OriginalDataset\\MildDemented\\",
            "moderate": "\\OriginalDataset\\ModerateDemented\\"
        }
        self.im_attributes = {
            "class": ["NonDemented",
                      "VeryMildDemented",
                      "MildDemented",
                      "ModerateDemented"],
            "path_train": ["\\AugmentedAlzheimerDataset\\NonDemented\\",
                           "\\AugmentedAlzheimerDataset\\VeryMildDemented\\",
                           "\\AugmentedAlzheimerDataset\\MildDemented\\",
                           "\\AugmentedAlzheimerDataset\\ModerateDemented\\"],
            "path_test": ["\\OriginalDataset\\NonDemented\\",
                          "\\OriginalDataset\\VeryMildDemented\\",
                          "\\OriginalDataset\\MildDemented\\",
                          "\\OriginalDataset\\ModerateDemented\\"],
            "label": [0, 1, 2, 3]
        }

    def connection(self):

        self.conn = psycopg2.connect(
            host=self.hostname,
            dbname=self.database,
            user=self.username,
            password=self.pwd,
            port=self.port_id)

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create_table(self):

        self.cur.execute('DROP TABLE IF EXISTS alz_schema.img_table')

        create_script = ''' CREATE TABLE IF NOT EXISTS alz_schema.img_table (
                                                    image      bytea,
                                                    label_class    int,
                                                    label_train_test  text) '''

        try:
            self.cur.execute(create_script)
            self.conn.commit()  # commit the changes to the database
            print("Created table")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_image_path(self):
        if (os.environ.get('USERNAME') == 'kubic'):
            self.path = 'C:\\Users\\kubic\\Documents\\Alzheimer'
        elif (os.environ.get('USERNAME') == 'ivono' or os.environ.get('USERNAME') == None):
            if (os.path.exists('D:\FH\Master Dortmund\Programmierprojekt')):
                self.path = 'D:\\FH\\Master Dortmund\\Programmierprojekt\\Alzheimer'
            else:
                self.path = 'C:\\Users\\ivono\\FH\\Programmierkurs\\Alzheimer'

    def send_files_to_postgresql(self):

        # label_class: non, verymild, mild, moderate
        # label_train_test: train oder test
        query = "INSERT INTO alz_schema.img_table(image, label_class, label_train_test) " + "VALUES(%s, %s, %s)"

        try:
            for i in db.im_attributes["path_train"]:

                mypath = db.path + i
                data = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

                img = np.empty(len(data), dtype=object)

                if "NonDemented" in mypath:
                    label_class = self.im_attributes["label"][0]
                elif "VeryMildDemented" in mypath:
                    label_class = self.im_attributes["label"][1]
                elif "MildDemented" in mypath:
                    label_class = self.im_attributes["label"][2]
                elif "ModerateDemented" in mypath:
                    label_class = self.im_attributes["label"][3]

                for n in range(0, len(img)):
                    img[n] = open(mypath + data[n], 'rb').read()
                    self.cur.execute(query, (psycopg2.Binary(img[n]), label_class, "train"))

            for i in db.im_attributes["path_test"]:

                mypath = db.path + i
                data = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

                img = np.empty(len(data), dtype=object)

                if "NonDemented" in mypath:
                    label_class = self.im_attributes["label"][0]
                elif "VeryMildDemented" in mypath:
                    label_class = self.im_attributes["label"][1]
                elif "MildDemented" in mypath:
                    label_class = self.im_attributes["label"][2]
                elif "ModerateDemented" in mypath:
                    label_class = self.im_attributes["label"][3]

                for n in range(0, len(img)):
                    img[n] = open(mypath + data[n], 'rb').read()
                    self.cur.execute(query, (psycopg2.Binary(img[n]), label_class, "test"))

            self.conn.commit()  # commit the changes to the database
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_files_from_postgresql(self, label_class, label_train_test):

        #img = np.empty(2, dtype=object)
        #select_script = """SELECT * from alz_schema.img_table where label_class = %s and label_train_test = %s"""

        # Initialize the numpy arrays
        train_images = np.empty((60000, 180, 180), dtype='uint8')
        train_labels = np.empty((60000), dtype='uint8')

        # Retrieve the training images from the database
        sql = "SELECT image \
                    FROM alz_schema.img_table \
                    WHERE label_train_test = 'train'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        # Populate the numpy arrays. row[2] contains the image index
        for row in result:
            nparray = pickle.loads(row[1])
        train_images[row[2]] = nparray
        train_labels[row[2]] = row[0]

        return train_images, train_labels



if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    db.connection()

    # db.create_table()

    # db.send_files_to_postgresql()

    train_images, train_labels = db.get_files_from_postgresql(0, "train")

    plt.figure()
    plt.imshow(train_images[0])
    print(np.mean(train_images[0]))
    plt.colorbar()
    plt.grid(False)
    plt.show()
    # print(files)

    print("finished")
    # before run -> create database called "alz"
    # Datenbanken sind geil
