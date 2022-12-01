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


    def connection(self):

        self.conn = psycopg2.connect(
            host=self.hostname,
            dbname=self.database,
            user=self.username,
            password=self.pwd,
            port=self.port_id)

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    def get_binary_array(self, path):
        with open(path, "rb") as image:
            f = image.read()
            b = bytes(f).hex()
            return b

    def send_files_to_postgresql(self, file_names):

        query = "INSERT INTO table(image) VALUES (decode(%s, 'hex'))"
        mylist = []
        for file_name in file_names:
            mylist.append(self.get_binary_array(file_name))

        try:
            self.cur.executemany(query, mylist)

            self.conn.commit()  # commit the changes to the database is advised for big files, see documentation
            count = self.cur.rowcount  # check that the images were all successfully added
            print(count, "Records inserted successfully into table")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_connection_cursor_tuple(self):
        self.conn = None
        try:
            params = self.config()
            print('Connecting to the PostgreSQL database...')
            connection = psycopg2.connect(**params)
            self.cur = connection.self.cur()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return self.conn, self.cur



    def test(self):

        try:
            with psycopg2.connect(
                    host=self.hostname,
                    dbname=self.database,
                    user=self.username,
                    password=self.pwd,
                    port=self.port_id) as self.conn:

                with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                    cur.execute('DROP TABLE IF EXISTS employee')

                    create_script = ''' CREATE TABLE IF NOT EXISTS employee (
                                            id      int PRIMARY KEY,
                                            name    varchar(40) NOT NULL,
                                            salary  int,
                                            dept_id varchar(30)) '''
                    cur.execute(create_script)


                    # test to load image
                    """
                    cur.execute('DROP TABLE IF EXISTS images')

                    create_script = ''' CREATE TABLE IF NOT EXISTS images (
                                                                img     bytea,
                                                                name    varchar(40) NOT NULL,
                                                                dept_id varchar(30)) '''
                    cur.execute(create_script)
                    """
                    image_url = 'C:\\Users\\kubic\\Documents\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg'


                    # end test







                    insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
                    insert_values = [(1, 'James', 12000, 'D1'), (2, 'Robin', 15000, 'D1'), (3, 'Xavier', 20000, 'D2')]
                    for record in insert_values:
                        cur.execute(insert_script, record)

                    update_script = 'UPDATE employee SET salary = salary + (salary * 0.5)'
                    cur.execute(update_script)

                    delete_script = 'DELETE FROM employee WHERE name = %s'
                    delete_record = ('James',)
                    cur.execute(delete_script, delete_record)

                    cur.execute('SELECT * FROM EMPLOYEE')
                    for record in cur.fetchall():
                        print(record['name'], record['salary'])
        except Exception as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()


if __name__ == '__main__':

    db = Database()

    db.connection()

    #conn, cur = db.connect_db.get_connection_cursor_tuple()
    img_names = ['C:\\Users\\kubic\\Documents\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg', 'C:\\Users\\kubic\\Documents\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg']
    db.send_files_to_postgresql(img_names)

    print("test")

    # before run -> create database called "alzheimer"

    # path = 'C:\\Users\\kubic\\Documents\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg'

    #db = Database()
    #db.test()