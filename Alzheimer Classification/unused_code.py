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
                image_url = self.path + '\\Alzheimer\\OriginalDataset\\MildDemented\\26 (19).jpg'

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