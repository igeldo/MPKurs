from imblearn.over_sampling import SMOTE
# Klasse soll die SMOTE_Methode auf den Datensatz anwenden, um die Minderheitsgruppe an die Mehrheit anzupassen.


class Resample:

    def __init__(self):
        self.oversample = SMOTE()
        self.over_Feature = None
        self.over_Target = None

    def upsampling_smote(self, Feature, Target):
        # Methode führt das synthetische Oversampling durch
        self.over_Feature, self.over_Target = self.oversample.fit_resample(Feature, Target)

        return self.over_Feature, self.over_Target
