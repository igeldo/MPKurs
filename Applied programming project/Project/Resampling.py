import pandas as pd

from daten import Daten
from feature import FeatureSelection


class Resample:

    def __init__(self):
        self.mix_data = None
        self.TenYearCHD = None
        self.none_TenYearCHD = None
        self.new_data = None

    def resample(self, data):
        self.mix_data = data.sample(frac=1, random_state=4)
        self.TenYearCHD = self.mix_data.loc[self.mix_data['TenYearCHD'] == 1]
        self.none_TenYearCHD = self.mix_data.loc[self.mix_data['TenYearCHD'] == 0].sample(n=611,random_state=42)
        self.new_data = pd.concat(self.TenYearCHD, self.none_TenYearCHD)
        return self.new_data

