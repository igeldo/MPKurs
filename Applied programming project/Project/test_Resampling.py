from unittest import TestCase
import numpy as np
import pandas as pd

from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample


class TestResample(TestCase):
    def test_upsampling_smote(self):
        data = Daten()
        self.data = data.data

        # Auswahl der gewünschten Feature
        new_data = FeatureSelection()
        self.new_data = new_data.new_data_frame(self.data)

        k = TestTrain()
        [self.X, self.y] = k.define_target_features(self.new_data)

        self.n_y_1 = np.count_nonzero(self.y)

        r = Resample()
        [X, y] = r.upsampling_smote(self.X, self.y)
        self.n_y_2 = np.count_nonzero(y)
        self.n_y_3 = len(y) - self.n_y_2

        self.assertEqual(len(X), 6358)
        self.assertEqual(len(y), 6358)
        self.assertNotEqual(self.n_y_1, self.n_y_2)
        self.assertEqual(self.n_y_2, self.n_y_3)



