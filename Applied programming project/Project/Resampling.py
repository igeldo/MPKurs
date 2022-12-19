import pandas as pd


# Klasse soll den Datensatz anpassen, sodass es zu keinem Undersampling kommt


class Resample:

    def __init__(self):
        self.mix_data = None
        self.TenYearCHD = None
        self.none_TenYearCHD = None
        self.new_data = None
        self.X_train = None
        self.y_train = None

    def resample(self, data):
        # übernimmmt das Resampeln der Daten
        self.mix_data = data.sample(frac=1, random_state=4)
        self.TenYearCHD = self.mix_data.loc[self.mix_data['TenYearCHD'] == 1]
        self.none_TenYearCHD = self.mix_data.loc[self.mix_data['TenYearCHD'] == 0].sample(n=611, random_state=42)
        self.new_data = pd.concat([self.TenYearCHD, self.none_TenYearCHD])
        return self.new_data

   # def split_test_train(self, data):
    #    self.y_train = data['TenYearCHD']
     #   self.X_train = data.drop('TenYearCHD', axis=1)
      #  return self.X_train, self.y_train
