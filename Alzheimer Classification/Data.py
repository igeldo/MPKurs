import Database
class Data:

    def __init__(self):

        # database superuser pw: yay_python

        db = Database()
        db.connection()

        train_images, train_labels = db.get_train_files_from_postgresql()
        test_images, test_labels = db.get_test_files_from_postgresql()

        # in init schon einlesen?
        self.traindata = train_images
        self.traindata_label = train_labels

        self.testdata = test_images
        self.testdata_label = test_labels


    def load_images(self, images):

        return images

    def load_images_to_database(self, database_access):

        # algorithm to upload data

        return database_access

    def get_images_from_database(self, database_access, layer):

        # algorithm to
        t = database_access

        return t, layer

if __name__ == '__main__':

        data = Data()
        print(data.traindata)
        print(data.traindata_label)


