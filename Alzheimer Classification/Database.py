import io

import psycopg2
import psycopg2.extras
import os
from os.path import isfile, join
import numpy as np
import tensorflow as tf
import tempfile
import tensorflow_io as tfio
from matplotlib import pyplot as plt
import PIL.Image as Image


class Database:

    def __init__(self):

        self._hostname = 'localhost'
        self._database = 'alz'
        self._username = 'postgres'
        self._pwd = 'yay_python'
        self._port_id = 5432

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
        """
        extend connection with the database
        """

        self.conn = psycopg2.connect(
            host=self._hostname,
            dbname=self._database,
            user=self._username,
            password=self._pwd,
            port=self._port_id)

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def create_table(self):
        """
        create table in database with the columns: image, label_class and label_train_test
        """

        self.cur.execute('DROP TABLE IF EXISTS alz_schema.img_table')
        print("Dropped table")
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
        """
        get local image path
        """

        if (os.environ.get('USERNAME') == 'kubic'):
            self.path = 'C:\\Users\\kubic\\Documents\\Alzheimer'
        elif (os.environ.get('USERNAME') == 'ivono' or os.environ.get('USERNAME') == None):
            if (os.path.exists('D:\FH\Master Dortmund\Programmierprojekt')):
                self.path = 'D:\\FH\\Master Dortmund\\Programmierprojekt\\Alzheimer'
            else:
                self.path = 'C:\\Users\\ivono\\FH\\Programmierkurs\\Alzheimer'

    def send_files_to_postgresql(self):
        """
        send files to database from the local directory
        """

        # label_class: non, verymild, mild, moderate
        # label_train_test: train oder test
        query = "INSERT INTO alz_schema.img_table(image, label_class, label_train_test) " + "VALUES(%s, %s, %s)"

        try:
            for i in self.im_attributes["path_train"]:

                mypath = self.path + i
                data = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

                if "NonDemented" in mypath:
                    label_class = self.im_attributes["label"][0]
                elif "VeryMildDemented" in mypath:
                    label_class = self.im_attributes["label"][1]
                elif "MildDemented" in mypath:
                    label_class = self.im_attributes["label"][2]
                elif "ModerateDemented" in mypath:
                    label_class = self.im_attributes["label"][3]

                for file in data:
                    temp_img = Image.open(mypath + file).resize((180, 180)).convert('L')
                    resized_img = io.BytesIO()
                    temp_img.save(resized_img, format='JPEG')
                    img_value = resized_img.getvalue()
                    self.cur.execute(query, (psycopg2.Binary(img_value), label_class, "train"))

            for i in self.im_attributes["path_test"]:

                mypath = self.path + i
                data = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

                if "NonDemented" in mypath:
                    label_class = self.im_attributes["label"][0]
                elif "VeryMildDemented" in mypath:
                    label_class = self.im_attributes["label"][1]
                elif "MildDemented" in mypath:
                    label_class = self.im_attributes["label"][2]
                elif "ModerateDemented" in mypath:
                    label_class = self.im_attributes["label"][3]

                for file in data:
                    temp_img = Image.open(mypath + file).resize((180, 180)).convert('L')
                    resized_img = io.BytesIO()
                    temp_img.save(resized_img, format='JPEG')
                    img_value = resized_img.getvalue()
                    self.cur.execute(query, (psycopg2.Binary(img_value), label_class, "test"))

            # load assert image
            temp_img = Image.open(self.path + "\\test_image.jfif").resize((180, 180)).convert('L')
            resized_img = io.BytesIO()
            temp_img.save(resized_img, format='JPEG')
            img_value = resized_img.getvalue()
            self.cur.execute(query, (psycopg2.Binary(img_value), 4, "assert_image"))

            self.conn.commit()  # commit the changes to the database
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_assert_files_from_postgresql(self):
        """
        get train files from database
        """

        # Initialize the numpy arrays
        train_images = []
        train_labels = []

        # Retrieve the training images from the database
        sql = "SELECT image, label_class \
                    FROM alz_schema.img_table \
                    WHERE label_train_test = 'assert_image'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        # Populate the numpy arrays. row[0] contains the image, row[1] contains label_class
        for row in result:

            # IMAGE:
            binary_img = row[0] # result[0][0]  # or row[0] <- wenn in Schleife
            img = Image.open(io.BytesIO(binary_img))

            train_images.append(np.array(img))
            train_labels.append(row[1])

        return train_images, train_labels

    def get_train_files_from_postgresql(self):
        """
        get train files from database
        """

        # Initialize the numpy arrays
        train_images = []
        train_labels = []

        # Retrieve the training images from the database
        sql = "SELECT image, label_class \
                    FROM alz_schema.img_table \
                    WHERE label_train_test = 'train'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        # Populate the numpy arrays. row[0] contains the image, row[1] contains label_class
        for row in result:

            # IMAGE:
            binary_img = row[0] # result[0][0]  # or row[0] <- wenn in Schleife
            img = Image.open(io.BytesIO(binary_img))

            train_images.append(np.array(img))
            train_labels.append(row[1])

        return train_images, train_labels


    def get_test_files_from_postgresql(self):
        """
        get test files from database
        """

        # Initialize the numpy arrays
        test_images = []
        test_labels = []

        # Retrieve the training images from the database
        sql = "SELECT image, label_class \
                    FROM alz_schema.img_table \
                    WHERE label_train_test = 'test'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        # Populate the numpy arrays. row[0] contains the image, row[1] contains label_class
        for row in result:

            binary_img = row[0]
            img = Image.open(io.BytesIO(binary_img))

            test_images.append(np.array(img))
            test_labels.append(row[1])

        return test_images, test_labels



if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    db.connection()
    print("Connection established")
    db.create_table()
    print("Table created")
    db.send_files_to_postgresql()
    print("All files uploaded")

    # train_images, train_labels = db.get_train_files_from_postgresql()
    # test_images, test_labels = db.get_test_files_from_postgresql()
    #
    # # show third train image
    # pic = 2
    # plt.figure()
    # plt.imshow(train_images[pic])
    # print(np.mean(train_images[pic]))
    # print("Label: ", train_labels[pic])
    # plt.colorbar()
    # plt.grid(False)
    # plt.show()
    #
    # # show 2001 train image
    # pic_test = 2000
    # plt.figure()
    # plt.imshow(train_images[pic_test])
    # print(np.mean(train_images[pic_test]))
    # print("Label: ", train_labels[pic_test])
    # plt.colorbar()
    # plt.grid(False)
    # plt.show()

    print("finished")
    # before run -> create database called "alz"

    # Notizen:
    # print Ausgabe implementieren -> als Backlog 18.01
    # Blockgrafik erstellen für den Datenfluss -> als Backlog 18.01
    # vielleicht auch Unittests?
