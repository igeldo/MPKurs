import pandas as pd
# Klasse soll die Daten des Datensatzes einlesen


class Daten:
    def __init__(self):
        self.filename = 'framingham.csv'                    # filename der CSV-Datei
        self.data = pd.read_csv(self.filename)              # liest die Daten ein
        self.data = self.data.drop(['education'], axis=1)   # entfernt das Feature 'Education', da nicht benötigt
        self.data = self.data.dropna()                      # entfernt alle Zeilen fehlenden Daten
