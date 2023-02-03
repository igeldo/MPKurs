import pandas as pd
# Klasse soll die Daten des Datensatzes einlesen


class Daten:
    def __init__(self):
        self.filename = 'framingham.csv'                             # filename der CSV-Datei
        self.data_original = pd.read_csv(self.filename)              # liest die Daten ein
        # entfernt das Feature 'Education', da nicht benötigt
        self.data_original = self.data_original.drop(['education'], axis=1)
        # entfernt alle Zeilen mit fehlenden Daten
        self.data_original = self.data_original.dropna()
