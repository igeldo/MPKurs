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

    def get_image_path(self):
        print(os.environ.get('USERNAME'))
        if (os.environ.get('USERNAME') == 'kubic'):
            self.path = 'C:\\Users\\kubic\\Documents\\Alzheimer'
        elif (os.environ.get('USERNAME') == 'ivono' or os.environ.get('USERNAME') == None):
            if (os.path.exists('D:\FH\Master Dortmund\Programmierprojekt')):
                self.path = 'D:\\FH\\Master Dortmund\\Programmierprojekt\\Alzheimer'
            else:
                self.path = 'C:\\Users\\ivono\\FH\\Programmierkurs\\Alzheimer'

    def get_binary_array(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b

    def send_files_to_postgresql(self, file_names):
        query_run = "INSERT INTO  test_table (images) VALUES (bytea_import(%s))"
        query = "INSERT INTO table(test_table) VALUES (decode(%s, 'hex'))"
        mylist = []
        for file_name in file_names:
            mylist.append(self.get_binary_array(file_name))

        try:
            self.cur.executemany(query_run, file_names)

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == '__main__':

    db = Database()
    db.get_image_path()
    print(db.path)
    db.connection()

    #conn, cur = db.connect_db.get_connection_cursor_tuple()
    img_names = [db.path + '\\OriginalDataset\\MildDemented\\26 (19).jpg', db.path + '\\OriginalDataset\\MildDemented\\26 (20).jpg']
    db.send_files_to_postgresql(img_names)

    print("test")

    # before run -> create database called "alzheimer"

    # path = 'C:\\Users\\kubic\\Documents\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg'

    #db = Database()
    #db.test()