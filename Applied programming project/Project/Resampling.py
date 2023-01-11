from imblearn.over_sampling import SMOTE


class Resample:

    def __init__(self):
        self.oversample = SMOTE()
        self.over_X = None
        self.over_y = None


    def upsampling_smote(self, X, y):
        self.over_X, self.over_y = self.oversample.fit_resample(X, y)

        return self.over_X, self.over_y