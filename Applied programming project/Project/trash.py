features_list = featureScores["Specs"].tolist()[:10]
# feature_list in data frame übergeben und nur die entsprechenden Features behalten --> drop
self.df = self.df[
    ['sysBP', 'glucose', 'age', 'totChol', 'cigsPerDay', 'diaBP', 'prevalentHyp', 'diabetes', 'BPMeds', 'male',
     'TenYearCHD']]