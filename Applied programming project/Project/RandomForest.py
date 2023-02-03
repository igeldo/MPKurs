from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


class RandomForest:

    def __init__(self):
        self.n_estimators = 20  # number of decision trees in the random forest
        self.random_state = 0   # The random seed used to generate the random subsets of features and data.
        self.max_depth = None     # The maximum depth of the tree. If None, then nodes are expanded until all leaves are
        # pure or until all leaves contain less than min_samples_split samples.
        self.max_features = 10
        self.rf_model = None
        self.report = None

    def random_forest(self, over_Feature_train, over_Target_train):
        self.rf_model = RandomForestClassifier(n_estimators=self.n_estimators,
                                               random_state=self.random_state,
                                               max_depth=self.max_depth,
                                               max_features=self.max_features)
        self.rf_model.fit(over_Feature_train, over_Target_train)
        return self.rf_model

    def accuracy(self, Target_test, Prediction):
        self.report = classification_report(Target_test, Prediction)
        return self.report

