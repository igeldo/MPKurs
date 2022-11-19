import pandas as pd

from daten import Daten
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


class FeatureSelection:

    def __init__(self):
        self.best_features = None
        self.fit = None
        self.scores = None
        self.columns = None
        self.Scores = None
        self.features_list = None
        self.data_new = None

    def selection(self, X, y):
        # Search after the best features:
        # SelektKBest = Select features according to the k-highest scores
        # SelektKBest(score_func = chi2, k = 10)
        # chi2 =  chi-squared stats between each non-negative feature and class
        # select the n_features features with the highest values for the test chi-squared statistic from X
        self.best_features = SelectKBest(score_func=chi2, k=10)

        # fit the SelektKBest accordingt to the feature X and the target variable
        self.fit = self.best_features.fit(X, y)

        self.scores = pd.DataFrame(self.fit.scores_)
        self.columns = pd.DataFrame(X.columns)

        # Build vector with the Score. Shows that sysB ist the best feature
        # Followed by glucose, age, totChol...
        self.Scores = pd.concat([self.columns, self.scores], axis=1)
        self.Scores.columns = ['Specs', 'Score']

        # Sorting the score after value
        self.Scores = self.Scores.sort_values(by='Score', ascending=False)

        # Choose top 10 features
        self.features_list = self.Scores["Specs"].tolist()[:10]

    def new_data_frame(self, data):
        # new data frame with the best 10 features
        # try converting feature_list into data_frame
        self.data_new = data[['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds', 'male',
             'TenYearCHD']]
        return self.data_new


# Code for testing
# X = Daten()
# X = X.data.iloc[:, 0:14]
# y  = Daten()
# y = y.data.iloc[:, -1]
# z = Daten()
# z = z.data.iloc[:, 0:15   ]

# s = FeatureSelection()
# s.selection(X, y)
# s.new_data_frame(z)

# scores = s.Scores
# list = s.features_list
# data = s.daten

