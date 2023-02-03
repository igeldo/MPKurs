from sklearn.model_selection import train_test_split
# Klasse teilt den Datensatz in einen Trainingsdatensatz und einen Testdatensatz auf.


class TestTrain:

    def __init__(self):
        # Definition der Test und Train Variablen
        self.Feature = None
        self.Target = None
        self.Feature_train = None
        self.Feature_test = None
        self.Target_train = None
        self.Target_test = None
        self.over_Target_train = None
        self.over_Target_test = None
        self.over_Feature_test = None
        self.over_Feature_train = None

    def define_target_features(self, data_original):
        # Funktion definiert die Feature- und die Target-Komponente für den Random Forest
        self.Target = data_original['TenYearCHD']
        self.Feature = data_original.drop(['TenYearCHD'], axis=1)
        return self.Feature, self.Target

    def define_train_test(self, Feature, Target):
        # Funktion splittet die Feature- und die Target-Komponente in einen Trainingssatz und einen Testsatz.
        self.Feature_train, self.Feature_test, self.Target_train, self.Target_test = \
            train_test_split(Feature, Target, test_size=0.3)
        # test size: % 30Testdatensatz, 70% Trainingsdatensatz
        # random_state = Steuert das Shuffling, das auf die Daten vor der Aufteilung angewendet wird.
        return self.Feature_train, self.Feature_test, self.Target_train, self.Target_test

    def upsampling_Smote_over(self, over_Feature, over_Train):
        # Funktion splittet die gesampelte Feature- und die Target-Komponente in einen Trainingssatz und einen Testsatz.
        self.over_Feature_train, self.over_Feature_test, self.over_Target_train, self.over_Target_test = \
            train_test_split(over_Feature, over_Train, test_size=0.3, stratify=over_Train)

        return self.over_Feature_train, self.over_Feature_test, self.over_Target_train, self.over_Target_test
