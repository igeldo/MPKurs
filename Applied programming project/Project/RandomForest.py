from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample


class RandomForest:

    def __init__(self):
        self.n_estimators = 10
        self.random_state = 44
        self.rf_model = None
        self.accuracy_value = None
        self.y_pred = None

    def random_forest(self, X_train, y_train):
        self.rf_model = RandomForestClassifier(n_estimators=self.n_estimators, max_features="sqrt",
                                               random_state=self.random_state)
        self.rf_model.fit(X_train, y_train)
        return self.rf_model

    def accuracy(self, y_test, y_pred):
        self.accuracy_value = metrics.accuracy_score(y_test, y_pred)
        return self.accuracy_value



data = Daten()
data = data.data

new_data = FeatureSelection()
new_data = new_data.new_data_frame(data)

k = TestTrain()
[X, y] = k.define_target_features(new_data)
[X_train, X_test, y_train, y_test] = k.define_train_test(X, y)

rf = RandomForest()
model = rf.random_forest(X_train, y_train)