from imblearn.over_sampling import SMOTE


class Resample:
    # Klasse soll die SMOTE_Methode auf den Datensatz anwenden, um die Minderheitsgruppe an die Mehrheit anzupassen.
    def __init__(self):
        self.oversample = SMOTE()
        self.over_Feature = None
        self.over_Target = None

    def upsampling_smote(self, Feature, Target):
        self.over_Feature, self.over_Target = self.oversample.fit_resample(Feature, Target)

        return self.over_Feature, self.over_Target
