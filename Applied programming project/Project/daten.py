import pandas as pd
# Klasse soll die Daten des Datensatzes einlesen


class Daten:
    def __init__(self):
        self.filename = 'framingham.csv'
        self.data = pd.read_csv(self.filename)  # liest die Daten ein
        self.data = self.data.drop(['education'], axis=1)  # entfernt das Feature 'Education'
        self.data = self.data.dropna()  # entfernt alle fehlenden Daten


# Code for testing
#d = Daten()
#data = d.data
