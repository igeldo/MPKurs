from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample


class RandomForest:

    def __init__(self):
        self.n_estimators = 100  # number of decision trees in the random forest
        self.random_state = 0   # The random seed used to generate the random subsets of features and data.
        self.max_depth = None     # The maximum depth of the tree. If None, then nodes are expanded until all leaves are
        # pure or until all leaves contain less than min_samples_split samples.
        self.max_features = 10
        self.rf_model = None
        self.accuracy_value = None
        self.y_pred = None

    def random_forest(self, X_train, y_train):
        self.rf_model = RandomForestClassifier(n_estimators=self.n_estimators, random_state=self.random_state, max_depth=self.max_depth,
                                               max_features=self.max_features)
        self.rf_model.fit(X_train, y_train)
        return self.rf_model

    def accuracy(self, y_test, y_pred):
        self.accuracy_value = metrics.accuracy_score(y_test, y_pred)
        return self.accuracy_value


# Einladen der Daten
data = Daten()
data = data.data

# Auswahl der gewünschten Feature
new_data = FeatureSelection()
new_data = new_data.new_data_frame(data)

# r sampling der Daten
r = Resample()
new_data = r.resample(new_data)

# Aufteilen des Datensatzes in Trainings und Testdaten
k = TestTrain()
[X, y] = k.define_target_features(new_data)
[X_train, X_test, y_train, y_test] = k.define_train_test(X, y)

# Berechnung des RandomForest
rf = RandomForest()
model = rf.random_forest(X_train, y_train)
prediction = model.predict(X_test)

# Berechnung der Genauigkeit des Models
accuracy = rf.accuracy(y_test, prediction)
print("The accuracy of the model with test data is:", accuracy)

# Darstellung der Confusion Matrix
cm = confusion_matrix(y_test, prediction)
conf_matrix = pd.DataFrame(data=cm, columns=['Predicted:0', 'Predicted:1'], index=['Actual:0', 'Actual:1'])
plt.figure(figsize=(8, 5))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu")
plt.title('Confusion Matrix Testdatensatz')
plt.show()

rf = RandomForest()
model = rf.random_forest(X_train, y_train)
prediction = model.predict(X_train)

accuracy = rf.accuracy(y_train, prediction)

print("The accuracy of the model with the train data is:", accuracy)

cm = confusion_matrix(y_train, prediction)
conf_matrix = pd.DataFrame(data=cm, columns=['Predicted:0', 'Predicted:1'], index=['Actual:0', 'Actual:1'])
plt.figure(figsize=(8, 5))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="YlGnBu")
plt.title('Confusion Matrix Trainingsdatensatz')
plt.show()
