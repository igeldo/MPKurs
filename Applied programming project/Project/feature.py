import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


# Klasse wählt die besten Features für das supervised learning mittels des Random Forest aus.


class FeatureSelection:

    def __init__(self):
        self.best_features = None
        self.fit = None
        self.scores = None
        self.columns = None
        self.Scores = None
        self.features_list = None
        self.data_best_features = None

    def selection(self, Feature, Target):
        # Search after the best features:
        # SelektKBest = Select features according to the k-highest scores
        # SelektKBest(score_func = chi2, k = 10)
        # chi2 =  chi-squared stats between each non-negative feature and class
        # select the n_features features with the highest values for the test chi-squared statistic from X
        self.best_features = SelectKBest(score_func=chi2, k=10)

        # Anpassung der SelektKBest-Funktion an das Merkmal X und die Zielvariable
        self.fit = self.best_features.fit(Feature, Target)

        self.scores = pd.DataFrame(self.fit.scores_)
        self.columns = pd.DataFrame(Feature.columns)

        # Erstellung eines Vektors mit dem Ergebnis. Zeigt, dass sysB das beste Merkmal ist
        # gefolgt von Glukose, Alter, totChol...
        self.Scores = pd.concat([self.columns, self.scores], axis=1)
        self.Scores.columns = ['Specs', 'Score']

        # Sortieren der Einträge nach ihrem Ergebnis
        self.Scores = self.Scores.sort_values(by='Score', ascending=False)

        # Auswahl der 10 besten Merkmale
        self.features_list = self.Scores["Specs"].tolist()[:10]

    def new_data_frame(self, data_original):
        # Erstellung eines neuen Datensatzes mit den 10 besten Merkmalen
        self.data_best_features = data_original[
            ['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds', 'male',
             'TenYearCHD']]
        return self.data_best_features
