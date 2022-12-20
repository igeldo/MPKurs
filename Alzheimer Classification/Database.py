import psycopg2
import psycopg2.extras
import os
from os.path import isfile, join
import numpy as np
import tempfile

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
                                                    label_class    text,
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


    def send_files_to_postgresql(self, file_names, label_class, label_train_test):

        img = np.empty(len(file_names), dtype=object)
        # img = open(file_names, 'rb').read()

        # label_class: non, verymild, mild, moderate
        # label_train_test: train oder test
        query = "INSERT INTO alz_schema.img_table(image, label_class, label_train_test) " + "VALUES(%s, %s, %s)"

        try:
            # self.cur.executemany(query, mylist)

            for n in range(0, len(img)):
                img[n] = open(db.path + db.train_folders[label_class] + file_names[n], 'rb').read()
                self.cur.execute(query, (psycopg2.Binary(img[n]), label_class, label_train_test))

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_files_from_postgresql(self, label_class, label_train_test):

        img = np.empty(2, dtype=object)
        select_script = """SELECT * from alz_schema.img_table where label_class = %s and label_train_test = %s"""

        try:
            # self.cur.executemany(query, mylist)
            self.cur.execute(select_script, [label_class, label_train_test])

            for n in range(0, 2):

                mypic = self.cur.fetchone()
                img[n] = open(db.path + db.train_folders[label_class], 'rb').write(str(mypic[0]))
                self.cur.execute(select_script, label_class, label_train_test)

            # img = self.cur.fetchall()

            print(img)

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
            print("in try")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return img

if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    db.connection()


    db.create_table()

    # load data to database
    mypath = db.path + db.train_folders["non"]
    train_data_0 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    db.send_files_to_postgresql(train_data_0, "non", "train")

    mypath = db.path + db.train_folders["verymild"]
    train_data_1 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    db.send_files_to_postgresql(train_data_1, "verymild", "train")

    mypath = db.path + db.train_folders["mild"]
    train_data_2 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    db.send_files_to_postgresql(train_data_2, "mild", "train")

    mypath = db.path + db.train_folders["moderate"]
    train_data_3 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    db.send_files_to_postgresql(train_data_3, "moderate", "train")


    # files = db.get_files_from_postgresql("verymild", "train")
    # print(files)

    print("finished")
    # before run -> create database called "alz"
    # Datenbanken sind geil