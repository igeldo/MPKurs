from sklearn.model_selection import train_test_split
# Klasse teilt den Datensatz in einen Trainingsdatensatz und einen Testdatensatz auf.


class TestTrain:

    def __init__(self):
        # Definition der Test und Train Variablen
        # y = Target-Variable
        # X = Features
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.over_y_train = None
        self.over_y_test = None
        self.over_X_test = None
        self.over_X_train = None

    def define_target_features(self, data):
        # Funktion definiert die x und die y Komponente für den Random Forest
        self.y = data['TenYearCHD']
        self.X = data.drop(['TenYearCHD'], axis=1)
        return self.X, self.y

    def define_train_test(self, x, y):
        # Funktion splittet die x und y Komponente in einen Trainingssatz und einen Testsatz.
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.3)
        # test size: % 30Testdatensatz, 70% Trainingsdatensatz
        # random_state = Steuert das Shuffling, das auf die Daten vor der Aufteilung angewendet wird.
        return self.X_train, self.X_test, self.y_train, self.y_test

    def upsampling_Smote_over(self, over_x, over_y):
        self.over_X_train, self.over_X_test, self.over_y_train, self.over_y_test = train_test_split(over_x, over_y,
                                                                                                    test_size=0.3,
                                                                                                    stratify=over_y)

        return self.over_X_train, self.over_X_test, self.over_y_train, self.over_y_test
