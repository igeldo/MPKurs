import psycopg2
import psycopg2.extras
import os

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


    def connection(self):

        self.conn = psycopg2.connect(
            host=self.hostname,
            dbname=self.database,
            user=self.username,
            password=self.pwd,
            port=self.port_id)

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # def create_table(self):
    #
    #     self.cur.execute('DROP TABLE IF EXISTS image')
    #
    #     # create table "img" typ is not final
    #     create_script = ''' CREATE TABLE IF NOT EXISTS image (
    #                                                 image      bytea,
    #                                                 label_class    int,
    #                                                 label_train_test  text) '''
    #     self.cur.execute(create_script)

    def get_image_path(self):
        if (os.environ.get('USERNAME') == 'kubic'):
            self.path = 'C:\\Users\\kubic\\Documents\\Alzheimer'
        elif (os.environ.get('USERNAME') == 'ivono' or os.environ.get('USERNAME') == None):
            if (os.path.exists('D:\FH\Master Dortmund\Programmierprojekt')):
                self.path = 'D:\\FH\\Master Dortmund\\Programmierprojekt\\Alzheimer'
            else:
                self.path = 'C:\\Users\\ivono\\FH\\Programmierkurs\\Alzheimer'


    def send_files_to_postgresql(self, file_names):

        img = open(file_names[1], 'rb').read()

        # label_class: 0 - 3 (Klassifikation dement)
        # label_train_test: train oder test
        query = "INSERT INTO test.test_table(image, label_class, label_train_test) " + "VALUES(%s, %s, %s)"

        # als Schleife programmieren -> alle Bilder werden auf einmal eingepflegt

        try:
            # self.cur.executemany(query, mylist)

            self.cur.execute(query, (psycopg2.Binary(img), 0, "train"))

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

    # db.create_table()

    img_names = [db.path + '\\OriginalDataset\\MildDemented\\26 (19).jpg', db.path + '\\OriginalDataset\\MildDemented\\26 (20).jpg']
    db.send_files_to_postgresql(img_names)

    print("finished")
    # before run -> create database called "alz"