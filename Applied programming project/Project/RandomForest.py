from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Libraries for code-testing
# from sklearn.metrics import confusion_matrix
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# from daten import Daten
# from feature import FeatureSelection
# from testtrain import TestTrain
# from Resampling import Resample


class RandomForest:

    def __init__(self):
        self.n_estimators = 20  # number of decision trees in the random forest
        self.random_state = 0   # The random seed used to generate the random subsets of features and data.
        self.max_depth = None     # The maximum depth of the tree. If None, then nodes are expanded until all leaves are
        # pure or until all leaves contain less than min_samples_split samples.
        self.max_features = 10
        self.rf_model = None
        self.y_pred = None
        self.report = None

    def random_forest(self, over_X_train, over_y_train):
        self.rf_model = RandomForestClassifier(n_estimators=self.n_estimators,
                                               random_state=self.random_state,
                                               max_depth=self.max_depth,
                                               max_features=self.max_features)
        self.rf_model.fit(over_X_train, over_y_train)
        return self.rf_model

    def accuracy(self, y_test, y_pred):
        self.report = classification_report(y_test, y_pred)
        return self.report


# Einladen der Daten
# data = Daten()
# data = data.data

# Auswahl der gewünschten Feature
# new_data = FeatureSelection()
# new_data = new_data.new_data_frame(data)

# k = TestTrain()
# [X, y] = k.define_target_features(new_data)
# [X_train, X_test, y_train, y_test] = k.define_train_test(X, y)

# r = Resample()
# [X_over, y_over] = r.upsampling_smote(X,y)

# Aufteilen des Datensatzes in Trainings und Testdaten
# [over_X_train, over_X_test, over_y_train, over_y_test] = k.upsampling_Smote_over(X_over, y_over)

# Berechnung des RandomForest
# rf = RandomForest()
# model = rf.random_forest(over_X_train, over_y_train)
# prediction = model.predict(X_test)

# Berechnung der Genauigkeit des Models
# report = rf.accuracy(y_test, prediction)

# print(report)

# Darstellung der Confusion Matrix
# cm = confusion_matrix(y_test, prediction)
# conf_matrix = pd.DataFrame(data=cm, columns=['Predicted:0', 'Predicted:1'], index=['Actual:0', 'Actual:1'])
# plt.figure(figsize=(8, 5))
# sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu")
# plt.title('Confusion Matrix Testdatensatz')
# plt.show()
