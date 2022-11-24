class Database:

    def __init__(self, traindata, testdata):

        # in init schon einlesen?
        self.traindata = traindata
        self.testdata = testdata

        self.images = []
        self.database_access = []
        self.layer = []