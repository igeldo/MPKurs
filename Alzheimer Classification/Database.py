import psycopg2
import psycopg2.extras
import os
from os.path import isfile, join
import numpy as np

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
            "label": [0,1,2,3]
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

        # create table "img" typ is not final
        create_script = ''' CREATE TABLE IF NOT EXISTS alz_schema.img_table (
                                                    image      bytea,
                                                    label_class    int,
                                                    label_train_test  text) '''

        try:
            self.cur.execute(create_script)

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
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


    def send_files_to_postgresql(self, file_names):

        img = np.empty(len(file_names), dtype=object)
        # img = open(file_names, 'rb').read()

        # label_class: 0 - 3 (Klassifikation dement)
        # label_train_test: train oder test
        query = "INSERT INTO alz_schema.img_table(image, label_class, label_train_test) " + "VALUES(%s, %s, %s)"

        # als Schleife programmieren -> alle Bilder werden auf einmal eingepflegt

        try:
            # self.cur.executemany(query, mylist)

            for n in range(0, len(img)):
                img[n] = open(db.path + db.train_folders["mild"] + file_names[n], 'rb').read()
                self.cur.execute(query, (psycopg2.Binary(img[n]), 0, "train"))

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        # for record in self.cur.fetchall():
        #     print(record['image'], record['label_class'])


if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    db.connection()

    db.create_table()

    # "train" + 0
    mypath = db.path + db.train_folders["mild"] # "\\AugmentedAlzheimerDataset\\MildDemented"
    train_data_0 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]

    # img_names = [db.path + '\\OriginalDataset\\MildDemented\\26 (19).jpg', db.path + '\\OriginalDataset\\MildDemented\\26 (20).jpg']

    db.send_files_to_postgresql(train_data_0)

    print("finished")
    # before run -> create database called "alz"
    # Datenbanken sind geil