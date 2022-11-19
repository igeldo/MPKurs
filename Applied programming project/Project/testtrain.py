from daten import Daten
from feature import FeatureSelection

from sklearn.model_selection import train_test_split


class TestTrain:

    def __init__(self):
        # Definition der Test und Train Variablen
        # y = Target-Variable
        # X = Features
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def define_target_features(self, data):
        self.X = data['TenYearCHD']
        self.y = data.drop(['TenYearCHD'], axis=1)
        return self.X, self.y

    def define_train_test(self, x, y):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, random_state=29)
        return self.X_train, self.X_test, self.y_train, self. y_test

# Check code
data = Daten()
data = data.data

new_data = FeatureSelection()
new_data = new_data.new_data_frame(data)

k = TestTrain()
[X, y] = k.define_target_features(new_data)

[X_train, X_test, y_train, y_test] = k.define_train_test(X, y)



