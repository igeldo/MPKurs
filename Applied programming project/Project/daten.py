import pandas as pd

# Klasse soll die Daten des Datensatzes einlesen
class Daten():

    def __init__(self, data):
        self.data = pd.read_csv(data)

d = Daten('framingham.csv')
data = d.data
