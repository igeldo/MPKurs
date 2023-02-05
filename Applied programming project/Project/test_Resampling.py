from unittest import TestCase
import numpy as np

from daten import Daten
from feature import FeatureSelection
from testtrain import TestTrain
from Resampling import Resample


class TestResample(TestCase):
    def test_upsampling_smote(self):
        # Zugriff auf die Daten
        data = Daten()
        data = data.data_original
        new_data = FeatureSelection()
        new_data = new_data.new_data_frame(data)

        k = TestTrain()
        [X, y] = k.define_target_features(new_data)
        # Anzahl der Elemente ungleich 0 ohne Resampling
        self.n_y_1 = np.count_nonzero(y)

        r = Resample()
        # [X, y] = r.upsampling_smote(X, y)
        # Anzahl der Elemente ungleich 0 mit SMOTE-Resampling
        self.n_y_2 = np.count_nonzero(y)
        # Anzahl der Elemente gleich 0 mit SMOTE-Resampling
        self.n_y_3 = len(y) - self.n_y_2

        # Anzahl der Elemente ungleich 0 vor dem Resampling sind ungleich der Elemente
        # ungleich 0 nach dem Resampling.
        self.assertNotEqual(self.n_y_1, self.n_y_2, 'Die Anzahl der Elemente ungleich Null'
                                                    ' haben sich nach dem SMOTE-Resampling '
                                                    'nicht verändert.')
        # Anzahl der Elemente ungleich 0 nach dem Resampling sind gleich der Anzahl der Elemente
        # gleich 0 nach dem Resampling. Das SMOTE-Resampling hat funktioniert.
        self.assertEqual(self.n_y_2, self.n_y_3, 'Die Anzahl der Elemente der Klasse "1" ist'
                                                 ' nicht gleich der Elemente der Klasse "0"')
